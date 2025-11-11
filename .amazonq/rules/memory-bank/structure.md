# QR Certificate Validator - Project Structure

## Directory Organization

### Core Processing Modules (`/core/`)
- **`pdf_processor.py`**: PDF parsing and QR extraction logic
- **`qr_detector.py`**: Multi-algorithm QR code detection
- **`validator.py`**: Certificate validation orchestration
- **`web_scraper.py`**: Online certificate verification via Selenium

### Utility Modules (`/utils/`)
- **`security_validator.py`**: Security validations (path traversal, SSRF protection)
- **`structured_logger.py`**: Structured logging for security events
- **`logger.py`**: General application logging
- **`file_handler.py`**: Safe file operations
- **`progress_bar.py`**: User interface progress tracking

### Output Generation (`/output/`)
- **`report_generator.py`**: Main report generation logic
- **`excel_formatter.py`**: Excel-specific formatting and export

### Testing Suite (`/tests/`)
- **`test_security.py`**: Security validation tests
- **`test_pdf_processor.py`**: PDF processing unit tests
- **`test_qr_detector.py`**: QR detection algorithm tests
- **`test_validator.py`**: Validation workflow tests

### Configuration & Documentation
- **`config.py`**: Centralized configuration management
- **`main.py`**: Application entry point and CLI interface
- **`security_check.py`**: Security verification script
- **`.env.example`**: Environment configuration template

## Architectural Patterns

### Modular Design
- **Separation of Concerns**: Each module handles specific functionality
- **Dependency Injection**: Configuration passed through modules
- **Interface Abstraction**: Clear APIs between components

### Security-First Architecture
- **Input Validation Layer**: All inputs validated before processing
- **Security Validator**: Centralized security checks
- **Structured Logging**: Security events tracked and auditable

### Processing Pipeline
```
PDF Input → QR Detection → Online Validation → Report Generation
     ↓           ↓              ↓                    ↓
Security    Multi-algo     Web Scraping        Excel/CSV
Validation  Detection      (Selenium)          Output
```

## Core Components Relationships

### Processing Flow
1. **`main.py`** orchestrates the entire workflow
2. **`pdf_processor.py`** extracts QR codes from PDFs
3. **`qr_detector.py`** applies multiple detection algorithms
4. **`web_scraper.py`** validates certificates online
5. **`report_generator.py`** compiles results into reports

### Security Layer
- **`security_validator.py`** validates all file paths and URLs
- **`structured_logger.py`** logs security events
- All modules integrate security checks before operations

### Configuration Management
- **`config.py`** provides centralized settings
- **`.env`** file for environment-specific values
- Validation and defaults for all configuration options

## Data Flow Architecture

### Input Processing
```
PDF Files → Security Validation → QR Extraction → Multi-Algorithm Detection
```

### Validation Pipeline
```
QR Codes → URL Validation → Web Scraping → Certificate Verification
```

### Output Generation
```
Validation Results → Data Aggregation → Excel Formatting → Report Export
```

## Design Principles

### Security by Design
- All file operations go through security validation
- URL validation prevents SSRF attacks
- Structured logging for security monitoring

### Error Handling Strategy
- Specific exception types for different error categories
- Graceful degradation when validation fails
- Comprehensive logging for troubleshooting

### Scalability Considerations
- Configurable worker threads for parallel processing
- Batch processing capabilities
- Memory-efficient PDF processing

### Maintainability Features
- Clear module boundaries and responsibilities
- Comprehensive test coverage
- Configuration-driven behavior
- Detailed documentation and logging