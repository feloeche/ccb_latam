#!/usr/bin/env python3
"""
Aplicación Flask simple para generar archivos Excel CCB
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import tempfile
import logging
import os
from ccb import CCBDataExtractor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Permitir llamadas desde cualquier origen (para GitHub Pages)
CORS(app)

# Variables de entorno
AUTH_TOKEN = os.getenv('HILOS_API_TOKEN')
FLOW_ID = os.getenv('HILOS_FLOW_ID', '0684111b-3948-7ce2-8000-b20bbb1bd564')

# Validar que las variables requeridas estén configuradas
if not AUTH_TOKEN:
    logger.error("HILOS_API_TOKEN no está configurado. Configura esta variable de entorno.")
    raise ValueError("HILOS_API_TOKEN es requerido")

logger.info("Variables de entorno configuradas correctamente")

# Variable global para almacenar resultados de trabajos
job_results = {}

@app.route('/')
def index():
    """Servir la página principal"""
    return send_file('index.html')


@app.route('/api/status')
def status():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({
        'status': 'ok',
        'message': 'Servicio CCB talento latam funcionando correctamente'
    })

@app.route('/api/generate-excel', methods=['POST'])
def generate_excel():
    """
    Endpoint para generar el archivo Excel
    """
    try:
        logger.info("Solicitud recibida para generar archivo Excel")

        # Crear instancia del extractor
        extractor = CCBDataExtractor(AUTH_TOKEN)

        # Procesar todos los contactos
        logger.info("Iniciando procesamiento de contactos...")
        processed_data = extractor.process_all_contacts()

        if not processed_data:
            return jsonify({
                'success': False,
                'error': 'No se encontraron datos para procesar'
            }), 400

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            temp_filename = tmp_file.name

        # Generar Excel
        logger.info("Generando archivo Excel con %d registros...", len(processed_data))
        extractor.generate_excel(processed_data, temp_filename)

        # Enviar archivo como respuesta
        logger.info("Enviando archivo Excel...")
        return send_file(
            temp_filename,
            as_attachment=True,
            download_name='ccb_data.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        logger.error("Error al generar archivo Excel: %s", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-excel-async', methods=['POST'])
def generate_excel_async():
    """
    Endpoint para generar el archivo Excel de forma asíncrona
    Retorna un ID de trabajo que puede usarse para verificar el progreso
    """
    try:
        import uuid
        import threading

        job_id = str(uuid.uuid4())

        # Iniciar procesamiento en segundo plano
        def process_data():
            try:
                extractor = CCBDataExtractor(AUTH_TOKEN)
                processed_data = extractor.process_all_contacts()

                if processed_data:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                        temp_filename = tmp_file.name
                    extractor.generate_excel(processed_data, temp_filename)

                    # Guardar resultado (en producción usar Redis o similar)
                    job_results[job_id] = {
                        'status': 'completed',
                        'filename': temp_filename,
                        'record_count': len(processed_data)
                    }
                else:
                    job_results[job_id] = {
                        'status': 'error',
                        'error': 'No se encontraron datos'
                    }
            except Exception as e:
                job_results[job_id] = {
                    'status': 'error',
                    'error': str(e)
                }

        job_results[job_id] = {'status': 'processing'}

        # Iniciar hilo
        thread = threading.Thread(target=process_data)
        thread.start()

        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Procesamiento iniciado'
        })

    except Exception as e:
        logger.error("Error al iniciar procesamiento asíncrono: %s", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/job-status/<job_id>')
def job_status(job_id):
    """Verificar el estado de un trabajo"""
    if job_id not in job_results:
        return jsonify({'error': 'Trabajo no encontrado'}), 404

    return jsonify(job_results[job_id])


@app.route('/api/download/<job_id>')
def download_file(job_id):
    """Descargar archivo completado"""
    if job_id not in job_results:
        return jsonify({'error': 'Trabajo no encontrado'}), 404

    job = job_results[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'Trabajo no completado'}), 400

    try:
        return send_file(
            job['filename'],
            as_attachment=True,
            download_name='ccb_data.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        logger.error("Error al descargar archivo: %s", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info("Iniciando aplicación Flask CCB Excel Generator")
    app.run(debug=True, host='0.0.0.0', port=8080)
