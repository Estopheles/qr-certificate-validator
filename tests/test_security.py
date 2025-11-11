"""
Tests de seguridad
"""
import pytest
import tempfile
import os
from pathlib import Path
from utils.security_validator import SecurityValidator

class TestSecurityValidator:
    
    def test_path_traversal_prevention(self):
        """Test prevención de path traversal"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Casos maliciosos
            malicious_paths = [
                "../../../etc/passwd",
                "..\\..\\windows\\system32",
                "/etc/passwd",
                "C:\\Windows\\System32",
                "../../sensitive_file.txt",
                "../config/database.conf"
            ]
            
            for path in malicious_paths:
                full_path = os.path.join(temp_dir, path)
                assert not SecurityValidator.validate_file_path(full_path, temp_dir), f"Path malicioso no bloqueado: {path}"
    
    def test_safe_path_validation(self):
        """Test validación de paths seguros"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Crear archivo de prueba
            safe_file = os.path.join(temp_dir, "test.pdf")
            Path(safe_file).touch()
            
            # Paths seguros - el directorio no tiene extensión válida, solo validar archivo
            assert SecurityValidator.validate_file_path(safe_file, temp_dir)
            # No validar directorio ya que no tiene extensión permitida
    
    def test_url_validation(self):
        """Test validación de URLs"""
        # URLs válidas
        valid_urls = [
            "https://siged.sep.gob.mx/certificado/123",
            "http://www.siged.sep.gob.mx/cert/456",
            "https://siged.sep.gob.mx/path/to/certificate"
        ]
        
        for url in valid_urls:
            assert SecurityValidator.validate_url(url), f"URL válida rechazada: {url}"
        
        # URLs maliciosas
        malicious_urls = [
            "http://localhost:8080/admin",
            "https://192.168.1.1/config",
            "ftp://malicious.com/data",
            "javascript:alert('xss')",
            "https://evil.com/redirect",
            "http://127.0.0.1/internal",
            "https://10.0.0.1/private"
        ]
        
        for url in malicious_urls:
            assert not SecurityValidator.validate_url(url), f"URL maliciosa no bloqueada: {url}"
    
    def test_filename_sanitization(self):
        """Test sanitización de nombres de archivo"""
        dangerous_names = [
            "../../etc/passwd",
            "file<script>alert('xss')</script>.pdf",
            "file|rm -rf /.pdf",
            "CON.pdf",
            "PRN.txt",
            "file?.pdf",
            "file*.pdf"
        ]
        
        for name in dangerous_names:
            sanitized = SecurityValidator.sanitize_filename(name)
            assert not any(char in sanitized for char in '<>:"/\\|?*'), f"Caracteres peligrosos no removidos: {sanitized}"
            # Verificar que nombres reservados sean manejados (deben tener prefijo)
            base_name = sanitized.split('.')[0].upper()
            if base_name in {'CON', 'PRN', 'AUX', 'NUL'}:
                assert sanitized.startswith('file_'), f"Nombre reservado no manejado correctamente: {sanitized}"
    
    def test_safe_join_path(self):
        """Test unión segura de paths"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Casos seguros
            safe_result = SecurityValidator.safe_join_path(temp_dir, "safe_file.pdf")
            assert safe_result.startswith(temp_dir)
            
            # Casos maliciosos
            with pytest.raises(ValueError):
                SecurityValidator.safe_join_path(temp_dir, "../../../etc/passwd")
            
            with pytest.raises(ValueError):
                SecurityValidator.safe_join_path(temp_dir, "")
            
            with pytest.raises(ValueError):
                SecurityValidator.safe_join_path(temp_dir, "..")
    
    def test_file_extension_validation(self):
        """Test validación de extensiones de archivo"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extensiones permitidas
            allowed_files = ["test.pdf", "report.xlsx", "data.csv", "config.json", "log.txt"]
            for filename in allowed_files:
                filepath = os.path.join(temp_dir, filename)
                Path(filepath).touch()
                assert SecurityValidator.validate_file_path(filepath, temp_dir)
            
            # Extensiones no permitidas
            dangerous_files = ["script.exe", "malware.bat", "virus.scr", "hack.js"]
            for filename in dangerous_files:
                filepath = os.path.join(temp_dir, filename)
                Path(filepath).touch()
                assert not SecurityValidator.validate_file_path(filepath, temp_dir), f"Extensión peligrosa no bloqueada: {filename}"
    
    def test_file_size_validation(self):
        """Test validación de tamaño de archivo"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Archivo pequeño (permitido)
            small_file = os.path.join(temp_dir, "small.pdf")
            with open(small_file, 'wb') as f:
                f.write(b'0' * 1024)  # 1KB
            assert SecurityValidator.validate_file_path(small_file, temp_dir)
            
            # Archivo muy grande (no permitido)
            large_file = os.path.join(temp_dir, "large.pdf")
            with open(large_file, 'wb') as f:
                f.write(b'0' * (SecurityValidator.MAX_FILE_SIZE + 1))
            assert not SecurityValidator.validate_file_path(large_file, temp_dir)

class TestStructuredLogger:
    
    def test_security_event_logging(self):
        """Test logging de eventos de seguridad"""
        from utils.structured_logger import StructuredLogger
        
        logger = StructuredLogger("test_security")
        
        # No debe lanzar excepciones
        logger.log_security_event("BLOCKED_URL", {"url": "http://malicious.com", "reason": "Domain not allowed"})
        logger.log_processing_event("test.pdf", "SUCCESS", {"qr_count": 1})

if __name__ == "__main__":
    pytest.main([__file__])