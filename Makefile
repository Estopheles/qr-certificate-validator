.PHONY: help install install-dev test test-unit test-integration test-security test-coverage lint format security clean setup-dev run-example build

# Default target
help:
	@echo "🔧 QR Certificate Validator - Comandos Disponibles"
	@echo "=================================================="
	@echo "📦 Instalación:"
	@echo "  install      - Instalar paquete en modo producción"
	@echo "  install-dev  - Instalar con dependencias de desarrollo"
	@echo "  setup-dev    - Configurar entorno completo de desarrollo"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test         - Ejecutar todos los tests"
	@echo "  test-unit    - Ejecutar solo tests unitarios"
	@echo "  test-integration - Ejecutar tests de integración"
	@echo "  test-security    - Ejecutar tests de seguridad"
	@echo "  test-coverage    - Ejecutar tests con cobertura"
	@echo ""
	@echo "🔍 Calidad de Código:"
	@echo "  lint         - Verificar código con flake8 y mypy"
	@echo "  format       - Formatear código con black e isort"
	@echo "  security     - Verificar seguridad con bandit"
	@echo ""
	@echo "🛠️ Utilidades:"
	@echo "  clean        - Limpiar archivos temporales"
	@echo "  build        - Construir paquete para distribución"
	@echo "  run-example  - Ejecutar ejemplo de uso"

# Instalación
install:
	@echo "📦 Instalando paquete..."
	pip install -e .

install-dev:
	@echo "📦 Instalando con dependencias de desarrollo..."
	pip install -e ".[dev]"

setup-dev:
	@echo "🔧 Configurando entorno de desarrollo completo..."
	./scripts/setup_dev_env.sh

# Testing
test:
	@echo "🧪 Ejecutando todos los tests..."
	python -m pytest tests/ -v

test-unit:
	@echo "📋 Ejecutando tests unitarios..."
	python -m pytest tests/unit/ -v -m "not slow"

test-integration:
	@echo "🔗 Ejecutando tests de integración..."
	python -m pytest tests/integration/ -v

test-security:
	@echo "🔒 Ejecutando tests de seguridad..."
	python -m pytest tests/unit/test_security.py -v
	python scripts/security_check.py

test-coverage:
	@echo "📊 Ejecutando tests con cobertura..."
	python -m pytest tests/ --cov=src/qr_validator --cov-report=html --cov-report=term

# Calidad de código
lint:
	@echo "🔍 Verificando código..."
	flake8 src/ tests/
	mypy src/

format:
	@echo "✨ Formateando código..."
	black src/ tests/
	isort src/ tests/

security:
	@echo "🛡️ Verificando seguridad..."
	bandit -r src/
	python scripts/security_check.py

# Utilidades
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/temp/*
	rm -rf build/logs/*
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf *.egg-info/

build:
	@echo "📦 Construyendo paquete..."
	python -m build

run-example:
	@echo "🚀 Ejecutando ejemplo..."
	@echo "📁 Verificando archivos en data/examples/sample_certificates/"
	@ls -la data/examples/sample_certificates/ 2>/dev/null || echo "⚠️  No hay archivos PDF en data/examples/sample_certificates/"
	python -m qr_validator.main data/examples/sample_certificates/ build/reports/example_output.xlsx

# Desarrollo
dev-install: install-dev
	@echo "🔧 Instalando hooks de pre-commit..."
	pre-commit install

dev-test: format lint test-security test
	@echo "✅ Verificación completa de desarrollo completada"

# CI/CD
ci-test: lint test-security test-coverage
	@echo "✅ Tests de CI/CD completados"