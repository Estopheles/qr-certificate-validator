"""
Analizador de seguridad para archivos PDF
Detecta contenido embebido, JavaScript, formularios y otros elementos de riesgo
"""
import os
import hashlib
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import fitz  # PyMuPDF
import re

from utils.structured_logger import StructuredLogger

logger = logging.getLogger(__name__)
structured_logger = StructuredLogger(__name__)


class PDFSecurityAnalyzer:
    """Analizador de seguridad para archivos PDF"""
    
    # Elementos de riesgo en PDFs
    RISKY_ELEMENTS = {
        '/JavaScript': 'CRITICAL',
        '/JS': 'CRITICAL', 
        '/OpenAction': 'HIGH',
        '/AA': 'HIGH',  # Automatic Actions
        '/Launch': 'CRITICAL',
        '/EmbeddedFile': 'MEDIUM',
        '/XFA': 'MEDIUM',  # XML Forms Architecture
        '/RichMedia': 'HIGH',
        '/3D': 'MEDIUM',
        '/Sound': 'LOW',
        '/Movie': 'MEDIUM',
        '/SubmitForm': 'HIGH',
        '/ImportData': 'HIGH',
        '/GoToR': 'MEDIUM',  # Go to Remote
        '/URI': 'LOW'
    }
    
    def __init__(self):
        self.results = {}
    
    def analyze_pdf_security(self, pdf_path: str) -> Dict:
        """Análisis completo de seguridad del PDF"""
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                return self._create_error_result("Archivo no encontrado")
            
            # Información básica del archivo
            file_info = self._get_file_info(pdf_path)
            
            # Análisis con PyMuPDF
            pymupdf_analysis = self._analyze_with_pymupdf(pdf_path)
            
            # Análisis de contenido raw
            raw_analysis = self._analyze_raw_content(pdf_path)
            
            # Análisis de metadatos
            metadata_analysis = self._analyze_metadata(pdf_path)
            
            # Evaluación de riesgo
            risk_assessment = self._assess_risk(pymupdf_analysis, raw_analysis)
            
            result = {
                'file_info': file_info,
                'pymupdf_analysis': pymupdf_analysis,
                'raw_analysis': raw_analysis,
                'metadata_analysis': metadata_analysis,
                'risk_assessment': risk_assessment,
                'timestamp': file_info['timestamp']
            }
            
            # Log del análisis
            structured_logger.log_security_event("PDF_SECURITY_SCAN", {
                "file": str(pdf_path),
                "risk_level": risk_assessment['overall_risk'],
                "threats_found": len(risk_assessment['threats'])
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error analizando PDF {pdf_path}: {e}")
            return self._create_error_result(f"Error en análisis: {str(e)}")
    
    def _get_file_info(self, pdf_path: Path) -> Dict:
        """Obtiene información básica del archivo"""
        stat = pdf_path.stat()
        
        # Calcular hash del archivo
        with open(pdf_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        return {
            'filename': pdf_path.name,
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'sha256': file_hash,
            'timestamp': stat.st_mtime
        }
    
    def _analyze_with_pymupdf(self, pdf_path: Path) -> Dict:
        """Análisis usando PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            
            analysis = {
                'page_count': len(doc),
                'is_encrypted': doc.is_encrypted,
                'needs_password': doc.needs_pass,
                'is_pdf': doc.is_pdf,
                'metadata': doc.metadata,
                'has_links': False,
                'has_annotations': False,
                'has_forms': False,
                'links_found': [],
                'annotations_found': [],
                'form_fields': []
            }
            
            # Analizar cada página
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Buscar enlaces
                links = page.get_links()
                if links:
                    analysis['has_links'] = True
                    for link in links:
                        if 'uri' in link:
                            analysis['links_found'].append({
                                'page': page_num,
                                'uri': link['uri'],
                                'type': link.get('kind', 'unknown')
                            })
                
                # Buscar anotaciones
                annotations = page.annots()
                if annotations:
                    analysis['has_annotations'] = True
                    for annot in annotations:
                        annot_dict = annot.info
                        analysis['annotations_found'].append({
                            'page': page_num,
                            'type': annot_dict.get('type', 'unknown'),
                            'content': annot_dict.get('content', '')[:100]  # Limitar contenido
                        })
                
                # Buscar campos de formulario
                widgets = page.widgets()
                if widgets:
                    analysis['has_forms'] = True
                    for widget in widgets:
                        analysis['form_fields'].append({
                            'page': page_num,
                            'field_name': widget.field_name,
                            'field_type': widget.field_type_string
                        })
            
            doc.close()
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis PyMuPDF: {e}")
            return {'error': str(e)}
    
    def _analyze_raw_content(self, pdf_path: Path) -> Dict:
        """Análisis del contenido raw del PDF"""
        try:
            with open(pdf_path, 'rb') as f:
                content = f.read()
            
            # Convertir a string para búsquedas (ignorar errores de encoding)
            content_str = content.decode('latin-1', errors='ignore')
            
            analysis = {
                'risky_elements_found': {},
                'suspicious_patterns': [],
                'external_references': [],
                'embedded_files': []
            }
            
            # Buscar elementos de riesgo
            for element, risk_level in self.RISKY_ELEMENTS.items():
                count = content_str.count(element)
                if count > 0:
                    analysis['risky_elements_found'][element] = {
                        'count': count,
                        'risk_level': risk_level
                    }
            
            # Buscar patrones sospechosos
            suspicious_patterns = [
                (r'eval\s*\(', 'JavaScript eval()'),
                (r'document\.write', 'JavaScript document.write'),
                (r'unescape\s*\(', 'JavaScript unescape()'),
                (r'fromCharCode', 'JavaScript fromCharCode'),
                (r'ActiveXObject', 'ActiveX Object'),
                (r'WScript\.Shell', 'Windows Script Host'),
                (r'cmd\.exe', 'Command Execution'),
                (r'powershell', 'PowerShell'),
                (r'http[s]?://[^\s<>"\']+', 'External URLs')
            ]
            
            for pattern, description in suspicious_patterns:
                matches = re.findall(pattern, content_str, re.IGNORECASE)
                if matches:
                    analysis['suspicious_patterns'].append({
                        'pattern': description,
                        'matches': len(matches),
                        'samples': matches[:3]  # Primeras 3 coincidencias
                    })
            
            # Buscar referencias externas
            url_pattern = r'http[s]?://[^\s<>"\'\\)\\]\\}]+'
            urls = re.findall(url_pattern, content_str, re.IGNORECASE)
            if urls:
                # Filtrar URLs únicas
                unique_urls = list(set(urls))
                analysis['external_references'] = unique_urls[:10]  # Máximo 10
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis raw: {e}")
            return {'error': str(e)}
    
    def _analyze_metadata(self, pdf_path: Path) -> Dict:
        """Análisis de metadatos del PDF"""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            doc.close()
            
            analysis = {
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'creation_date': metadata.get('creationDate', ''),
                'modification_date': metadata.get('modDate', ''),
                'suspicious_metadata': []
            }
            
            # Detectar metadatos sospechosos
            suspicious_creators = [
                'malware', 'virus', 'trojan', 'exploit', 'hack',
                'shell', 'payload', 'backdoor'
            ]
            
            creator_lower = analysis['creator'].lower()
            producer_lower = analysis['producer'].lower()
            
            for suspicious in suspicious_creators:
                if suspicious in creator_lower or suspicious in producer_lower:
                    analysis['suspicious_metadata'].append(f"Suspicious creator/producer: {suspicious}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis de metadatos: {e}")
            return {'error': str(e)}
    
    def _assess_risk(self, pymupdf_analysis: Dict, raw_analysis: Dict) -> Dict:
        """Evalúa el riesgo general del PDF"""
        threats = []
        risk_score = 0
        
        # Evaluar elementos de riesgo encontrados
        risky_elements = raw_analysis.get('risky_elements_found', {})
        for element, info in risky_elements.items():
            risk_level = info['risk_level']
            count = info['count']
            
            if risk_level == 'CRITICAL':
                risk_score += 50 * count
                threats.append(f"CRÍTICO: {element} encontrado {count} veces")
            elif risk_level == 'HIGH':
                risk_score += 25 * count
                threats.append(f"ALTO: {element} encontrado {count} veces")
            elif risk_level == 'MEDIUM':
                risk_score += 10 * count
                threats.append(f"MEDIO: {element} encontrado {count} veces")
            elif risk_level == 'LOW':
                risk_score += 5 * count
                threats.append(f"BAJO: {element} encontrado {count} veces")
        
        # Evaluar patrones sospechosos
        suspicious_patterns = raw_analysis.get('suspicious_patterns', [])
        for pattern in suspicious_patterns:
            risk_score += 15
            threats.append(f"Patrón sospechoso: {pattern['pattern']}")
        
        # Evaluar características del PDF
        if pymupdf_analysis.get('is_encrypted'):
            risk_score += 20
            threats.append("PDF encriptado")
        
        if pymupdf_analysis.get('has_forms'):
            risk_score += 10
            threats.append("Contiene formularios")
        
        if len(raw_analysis.get('external_references', [])) > 0:
            risk_score += 15
            threats.append("Referencias externas encontradas")
        
        # Determinar nivel de riesgo
        if risk_score >= 100:
            overall_risk = 'CRITICAL'
            recommendation = 'BLOQUEAR - Archivo altamente peligroso'
        elif risk_score >= 50:
            overall_risk = 'HIGH'
            recommendation = 'CUARENTENA - Revisar manualmente'
        elif risk_score >= 25:
            overall_risk = 'MEDIUM'
            recommendation = 'PRECAUCIÓN - Monitorear'
        elif risk_score > 0:
            overall_risk = 'LOW'
            recommendation = 'PERMITIR - Riesgo mínimo'
        else:
            overall_risk = 'SAFE'
            recommendation = 'SEGURO - Sin amenazas detectadas'
        
        return {
            'overall_risk': overall_risk,
            'risk_score': risk_score,
            'threats': threats,
            'recommendation': recommendation,
            'threat_count': len(threats)
        }
    
    def _create_error_result(self, error_msg: str) -> Dict:
        """Crea un resultado de error"""
        return {
            'error': error_msg,
            'risk_assessment': {
                'overall_risk': 'UNKNOWN',
                'risk_score': -1,
                'threats': [f"Error en análisis: {error_msg}"],
                'recommendation': 'REVISAR MANUALMENTE - Error en análisis'
            }
        }
    
    def is_safe_pdf(self, analysis_result: Dict) -> bool:
        """Determina si un PDF es seguro basado en el análisis"""
        if 'error' in analysis_result:
            return False
        
        risk_level = analysis_result.get('risk_assessment', {}).get('overall_risk', 'UNKNOWN')
        return risk_level in ['SAFE', 'LOW']
    
    def should_quarantine(self, analysis_result: Dict) -> bool:
        """Determina si un PDF debe ir a cuarentena"""
        if 'error' in analysis_result:
            return True
        
        risk_level = analysis_result.get('risk_assessment', {}).get('overall_risk', 'UNKNOWN')
        return risk_level in ['CRITICAL', 'HIGH']