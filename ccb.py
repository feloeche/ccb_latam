#!/usr/bin/env python3
"""
Script para obtener datos de usuarios que han pasado por un flujo específico
y generar un archivo Excel con la información requerida.
"""

import requests
import pandas as pd
import json
import time
from typing import List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CCBDataExtractor:
    def __init__(self, auth_token: str):
        """
        Inicializar el extractor con el token de autorización.
        
        Args:
            auth_token: Token de autorización para la API
        """
        self.auth_token = auth_token
        self.base_url = "https://api.hilos.io/api"
        self.headers = {
            'Authorization': f'Token {auth_token}',
            'Content-Type': 'application/json'
        }
        
        # ID del flujo específico
        self.flow_id = "0684111b-3948-7ce2-8000-b20bbb1bd564"
        
        # Columnas requeridas para el Excel
        self.required_columns = [
            'phone', 'ccb_init', 'ccb_adult', 'ccb_question_1', 'ccb_question_2', 'ccb_question_3', 
            'ccb_otro_question_3', 'ccb_question_4', 'ccb_pais_question_4', 'ccb_otra_question_4',
            'ccb_question_5', 'ccb_question_6', 'ccb_otro_question_6', 'ccb_question_6-1', 
            'ccb_otro_question_6-1', 'ccb_question_7', 'ccb_otro_question_7', 'ccb_question_7-1',
            'ccb_other_question_7-1', 'ccb_question_8', 'ccb_question_8-1', 'ccb_question_8-2',
            'ccb_question_9', 'ccb_question_10', 'ccb_question_11', 'ccb_gender_question_11',
            'ccb_question_12', 'ccb_question_12-1', 'ccb_otro_question_12-1', 'ccb_question_12-2',
            'ccb_cual_question_12-2', 'ccb_question_13', 'ccb_question_14', 'ccb_cual_question_14',
            'ccb_question_15', 'ccb_cual_question_15', 'ccb_question_16', 'ccb_cual_question_16'
        ]
        
        # Cargar mapeo de campos a encabezados
        self.field_mapping = self.load_field_mapping()

    def load_field_mapping(self) -> Dict[str, str]:
        """
        Cargar el mapeo de campos a encabezados desde el archivo campos.json.
        
        Returns:
            Diccionario con el mapeo de campo -> encabezado
        """
        try:
            with open('campos.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            logger.info(f"Cargado mapeo de campos: {len(mapping)} entradas")
            return mapping
        except FileNotFoundError:
            logger.error("Archivo campos.json no encontrado")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear campos.json: {e}")
            return {}

    def get_flow_execution_contacts(self) -> List[Dict[str, Any]]:
        """
        Obtener todos los contactos que han pasado por el flujo específico.
        Maneja la paginación para obtener todos los resultados.
        
        Returns:
            Lista de contactos con sus IDs
        """
        url = f"{self.base_url}/flow-execution-contact?flow={self.flow_id}"
        all_contacts = []
        next_url = None
        
        try:
            logger.info(f"Obteniendo contactos del flujo {self.flow_id}")
            
            # Primera llamada
            params = {
                'flow': self.flow_id
            }
            
            while True:
                if next_url:
                    # Usar la URL de la siguiente página
                    logger.info(f"Obteniendo siguiente página: {next_url}")
                    response = requests.get(next_url, headers=self.headers)
                else:
                    # Primera llamada o llamada con parámetros
                    logger.info(f"Obteniendo página inicial...")
                    response = requests.get(url, headers=self.headers, params=params)
                
                response.raise_for_status()
                data = response.json()
                
                # Verificar estructura de respuesta
                if not isinstance(data, dict) or 'results' not in data:
                    logger.error(f"Formato de respuesta inesperado: {data}")
                    break
                
                contacts = data['results']
                total_count = data.get('count', 0)
                next_url = data.get('next')
                
                logger.info(f"Página actual: {len(contacts)} contactos de {total_count} total")
                
                if not contacts:
                    logger.info("No hay más contactos en esta página")
                    break
                
                all_contacts.extend(contacts)
                
                # Si no hay siguiente página, terminamos
                if not next_url:
                    logger.info("Última página alcanzada")
                    break
                
                # Pequeña pausa entre páginas
                time.sleep(0.2)
            
            logger.info(f"Total de contactos encontrados: {len(all_contacts)}")
            return all_contacts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener contactos del flujo: {e}")
            raise

    def get_contact_details(self, contact_id: str) -> Dict[str, Any]:
        """
        Obtener información detallada de un contacto específico.
        
        Args:
            contact_id: ID del contacto
            
        Returns:
            Información detallada del contacto
        """
        url = f"{self.base_url}/contact/{contact_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Log de debug para entender la estructura de datos
            logger.debug(f"Respuesta del contacto {contact_id}: {json.dumps(data, indent=2)[:500]}...")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener detalles del contacto {contact_id}: {e}")
            return {}

    def extract_contact_data(self, contact_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extraer los campos específicos requeridos de los detalles del contacto.
        
        Args:
            contact_details: Información completa del contacto
            
        Returns:
            Diccionario con los campos requeridos
        """
        # Inicializar diccionario con valores vacíos para todas las columnas
        extracted_data = {col: '' for col in self.required_columns}
        
        def extract_value(data, key):
            """Función auxiliar para extraer valores de manera segura"""
            if isinstance(data, dict):
                return data.get(key, '')
            elif isinstance(data, list):
                # Si es una lista, buscar en cada elemento
                for item in data:
                    if isinstance(item, dict) and key in item:
                        return item[key]
            return ''
        
        # Extraer datos básicos del contacto
        extracted_data['phone'] = extract_value(contact_details, 'phone')
        
        # Buscar en diferentes estructuras de datos posibles
        search_locations = [
            contact_details,  # Nivel raíz
            contact_details.get('fields', {}),  # Campo fields
            contact_details.get('custom_fields', {}),  # Campo custom_fields
            contact_details.get('responses', {}),  # Campo responses
            contact_details.get('data', {}),  # Campo data
            contact_details.get('attributes', {}),  # Campo attributes
            contact_details.get('meta', {}),  # Campo meta (importante para este API)
        ]
        
        # Buscar cada campo requerido en todas las ubicaciones posibles
        for field_name in self.required_columns:
            if field_name == 'phone':  # Ya procesado arriba
                continue
                
            for location in search_locations:
                if isinstance(location, dict):
                    value = extract_value(location, field_name)
                    if value:  # Si encontramos un valor no vacío
                        extracted_data[field_name] = value
                        break
        
        # Buscar también en arrays o estructuras anidadas
        for key, value in contact_details.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        for field_name in self.required_columns:
                            if field_name in item and not extracted_data[field_name]:
                                extracted_data[field_name] = item[field_name]
        
        # Buscar específicamente en el campo 'meta' que parece contener datos importantes
        meta_data = contact_details.get('meta', {})
        if isinstance(meta_data, dict):
            for field_name in self.required_columns:
                if field_name in meta_data and not extracted_data[field_name]:
                    extracted_data[field_name] = meta_data[field_name]
        
        return extracted_data

    def analyze_duplicates(self, flow_contacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analizar los duplicados en la lista de contactos del flujo.
        
        Args:
            flow_contacts: Lista de contactos del flujo
            
        Returns:
            Diccionario con estadísticas de duplicados
        """
        contact_counts = {}
        duplicate_details = {}
        
        for contact in flow_contacts:
            contact_info = contact.get('contact', {})
            contact_id = contact_info.get('id')
            
            if contact_id:
                if contact_id in contact_counts:
                    contact_counts[contact_id] += 1
                    if contact_id not in duplicate_details:
                        duplicate_details[contact_id] = []
                    duplicate_details[contact_id].append(contact.get('id', 'N/A'))
                else:
                    contact_counts[contact_id] = 1
        
        # Calcular estadísticas
        total_contacts = len(flow_contacts)
        unique_contacts = len(contact_counts)
        duplicates = sum(1 for count in contact_counts.values() if count > 1)
        total_duplicate_instances = sum(count - 1 for count in contact_counts.values() if count > 1)
        
        stats = {
            'total_contacts': total_contacts,
            'unique_contacts': unique_contacts,
            'duplicate_contacts': duplicates,
            'total_duplicate_instances': total_duplicate_instances,
            'duplicate_details': duplicate_details
        }
        
        return stats

    def process_all_contacts(self) -> List[Dict[str, Any]]:
        """
        Procesar todos los contactos del flujo y extraer la información requerida.
        Garantiza que cada contacto aparezca solo una vez en el resultado final.
        
        Returns:
            Lista de diccionarios con los datos extraídos (sin duplicados)
        """
        # Obtener lista de contactos del flujo
        flow_contacts = self.get_flow_execution_contacts()
        
        # Analizar duplicados antes del procesamiento
        logger.info("Analizando duplicados en el flujo...")
        duplicate_stats = self.analyze_duplicates(flow_contacts)
        
        logger.info(f"Análisis de duplicados:")
        logger.info(f"  - Total de registros en el flujo: {duplicate_stats['total_contacts']}")
        logger.info(f"  - Contactos únicos: {duplicate_stats['unique_contacts']}")
        logger.info(f"  - Contactos con duplicados: {duplicate_stats['duplicate_contacts']}")
        logger.info(f"  - Instancias duplicadas totales: {duplicate_stats['total_duplicate_instances']}")
        
        # Set para rastrear contactos únicos procesados
        processed_contact_ids = set()
        processed_data = []
        duplicate_count = 0
        
        for i, contact in enumerate(flow_contacts, 1):
            # Extraer el ID del contacto desde contact.id
            contact_info = contact.get('contact', {})
            contact_id = contact_info.get('id')
            
            if not contact_id:
                logger.warning(f"Contacto {i} no tiene ID válido. Datos: {contact}")
                continue
            
            # Verificar si ya procesamos este contacto
            if contact_id in processed_contact_ids:
                duplicate_count += 1
                logger.debug(f"Contacto duplicado omitido: {contact_id}")
                continue
            
            # Marcar como procesado
            processed_contact_ids.add(contact_id)
            
            logger.info(f"Procesando contacto único {len(processed_contact_ids)}/{duplicate_stats['unique_contacts']}: {contact_id}")
            
            # Obtener detalles del contacto
            contact_details = self.get_contact_details(contact_id)
            if not contact_details:
                logger.warning(f"No se pudieron obtener detalles para el contacto {contact_id}")
                continue
            
            # Extraer datos requeridos
            extracted_data = self.extract_contact_data(contact_details)
            processed_data.append(extracted_data)
            
            # Pequeña pausa para no sobrecargar la API
            time.sleep(0.1)
        
        logger.info(f"Procesamiento completado:")
        logger.info(f"  - Total de registros en el flujo: {duplicate_stats['total_contacts']}")
        logger.info(f"  - Contactos únicos procesados: {len(processed_data)}")
        logger.info(f"  - Duplicados omitidos: {duplicate_count}")
        
        return processed_data

    def generate_excel(self, data: List[Dict[str, Any]], filename: str = "ccb_data.xlsx"):
        """
        Generar archivo Excel con los datos procesados.
        
        Args:
            data: Lista de diccionarios con los datos
            filename: Nombre del archivo Excel
        """
        try:
            # Crear DataFrame
            df = pd.DataFrame(data)
            
            # Asegurar que todas las columnas requeridas estén presentes
            for col in self.required_columns:
                if col not in df.columns:
                    df[col] = ''
            
            # Reordenar columnas según el orden requerido
            df = df[self.required_columns]
            
            # Verificar duplicados en el DataFrame final (por si acaso)
            initial_count = len(df)
            df_unique = df.drop_duplicates(subset=['phone'], keep='first')
            final_count = len(df_unique)
            
            if initial_count != final_count:
                logger.warning(f"Se encontraron {initial_count - final_count} duplicados adicionales en el DataFrame final")
                df = df_unique
            
            # Crear mapeo de nombres de columnas a encabezados
            column_headers = {}
            for col in df.columns:
                if col in self.field_mapping:
                    column_headers[col] = self.field_mapping[col]
                    logger.debug(f"Mapeo de columna: {col} -> {self.field_mapping[col]}")
                else:
                    # Si no hay mapeo, usar el nombre original de la columna
                    column_headers[col] = col
                    logger.warning(f"No se encontró mapeo para la columna: {col}")
            
            # Renombrar las columnas con los encabezados
            df_renamed = df.rename(columns=column_headers)
            
            # Guardar en Excel
            df_renamed.to_excel(filename, index=False)
            logger.info(f"Archivo Excel generado: {filename}")
            logger.info(f"Total de registros únicos: {len(df_renamed)}")
            logger.info(f"Total de columnas: {len(df_renamed.columns)}")
            
            # Mostrar algunos encabezados como confirmación
            logger.info("Primeros 5 encabezados de columnas:")
            for i, header in enumerate(df_renamed.columns[:5]):
                logger.info(f"  {i+1}. {header}")
            
        except Exception as e:
            logger.error(f"Error al generar archivo Excel: {e}")
            raise

    def test_api_response(self):
        """
        Método de prueba para entender la estructura de las respuestas de la API.
        """
        logger.info("=== PRUEBA DE ESTRUCTURA DE API ===")
        
        # Probar endpoint de flow-execution-contact
        try:
            url = f"{self.base_url}/flow-execution-contact"
            params = {'flow': self.flow_id}
            
            logger.info("Probando endpoint flow-execution-contact...")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Estructura de flow-execution-contact:")
            logger.info(f"  - Count: {data.get('count', 'N/A')}")
            logger.info(f"  - Next: {data.get('next', 'N/A')}")
            logger.info(f"  - Previous: {data.get('previous', 'N/A')}")
            logger.info(f"  - Results count: {len(data.get('results', []))}")
            
            # Mostrar estructura del primer contacto
            if data.get('results'):
                first_contact = data['results'][0]
                logger.info(f"Estructura del primer contacto:")
                logger.info(f"  - ID raíz: {first_contact.get('id', 'N/A')}")
                
                # Mostrar información del objeto contact
                contact_info = first_contact.get('contact', {})
                logger.info(f"  - Contact ID: {contact_info.get('id', 'N/A')}")
                logger.info(f"  - Contact keys: {list(contact_info.keys())}")
                
                # Mostrar estructura del campo meta
                meta_info = contact_info.get('meta', {})
                if meta_info:
                    logger.info(f"  - Meta keys: {list(meta_info.keys())}")
                
                # Probar obtener detalles del contacto usando el ID correcto
                contact_id = contact_info.get('id')
                if contact_id:
                    logger.info(f"Probando contacto: {contact_id}")
                    contact_details = self.get_contact_details(contact_id)
                    logger.info(f"Estructura de contacto detallado:")
                    logger.info(f"  - Keys principales: {list(contact_details.keys())}")
                    
                    # Mostrar algunos campos específicos
                    for field in ['phone', 'first_name', 'last_name', 'email']:
                        if field in contact_details:
                            logger.info(f"  - {field}: {contact_details[field]}")
            
        except Exception as e:
            logger.error(f"Error en prueba de API: {e}")

    def run(self, output_filename: str = "ccb_data.xlsx", test_mode: bool = False):
        """
        Ejecutar el proceso completo.
        
        Args:
            output_filename: Nombre del archivo de salida
            test_mode: Si es True, solo ejecuta pruebas sin generar Excel
        """
        try:
            logger.info("Iniciando proceso de extracción de datos CCB")
            
            if test_mode:
                self.test_api_response()
                return
            
            # Procesar todos los contactos
            processed_data = self.process_all_contacts()
            
            if not processed_data:
                logger.warning("No se encontraron datos para procesar")
                return
            
            # Generar archivo Excel
            self.generate_excel(processed_data, output_filename)
            
            logger.info("Proceso completado exitosamente")
            
        except Exception as e:
            logger.error(f"Error durante la ejecución: {e}")
            raise


def main():
    """
    Función principal del script.
    """
    import sys
    
    # Token de autorización (debería venir de variables de entorno o configuración)
    AUTH_TOKEN = "4bc07ce70ba1bddb115d50bd54690140a3b73f96"
    
    # Crear instancia del extractor
    extractor = CCBDataExtractor(AUTH_TOKEN)
    
    # Verificar si se solicita modo de prueba
    test_mode = len(sys.argv) > 1 and sys.argv[1] == "--test"
    
    if test_mode:
        logger.info("Ejecutando en modo de prueba...")
        extractor.run("ccb_data.xlsx", test_mode=True)
    else:
        logger.info("Ejecutando proceso completo...")
        extractor.run("ccb_data.xlsx")


if __name__ == "__main__":
    main()
