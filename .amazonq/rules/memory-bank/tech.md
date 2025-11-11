# QR Certificate Validator - Technology Stack

## Programming Language
- **Python 3.8+**: Core language with modern features and security updates

## Core Dependencies

### PDF Processing
- **PyMuPDF (>=1.24.0)**: Primary PDF parsing and rendering
- **pikepdf (>=8.15.0)**: PDF manipulation and security handling
- **Pillow (>=10.2.0)**: Image processing for QR extraction

### QR Code Detection
- **opencv-python (>=4.9.0)**: Computer vision algorithms for QR detection
- **pyzbar (>=0.1.9)**: Barcode and QR code decoding library
- **numpy (>=1.24.0)**: Numerical operations for image processing

### Web Scraping & Validation
- **selenium (>=4.17.0)**: Browser automation for certificate validation
- **beautifulsoup4 (>=4.12.2)**: HTML parsing and data extraction
- **lxml (>=4.9.3)**: XML/HTML processing engine
- **urllib3 (>=2.0.0)**: HTTP client with security features

### Data Processing & Output
- **pandas (>=2.2.0)**: Data manipulation and analysis
- **openpyxl (>=3.1.2)**: Excel file generation and formatting

### Configuration & Utilities
- **python-dotenv (>=1.0.0)**: Environment variable management
- **click (>=8.1.7)**: Command-line interface framework
- **tqdm (>=4.66.1)**: Progress bar and user feedback

### Security
- **cryptography (>=41.0.0)**: Cryptographic operations and security

### Development & Testing
- **pytest (>=7.4.3)**: Testing framework
- **black (>=23.12.0)**: Code formatting
- **flake8 (>=6.1.0)**: Code linting
- **mypy (>=1.7.1)**: Static type checking

## System Requirements

### Operating System
- **Primary**: Fedora/Linux (development environment)
- **Supported**: Ubuntu, Debian, macOS, Windows

### Browser Dependencies
- **Chrome/Chromium**: Required for Selenium web scraping
- **WebDriver**: Automatically managed by Selenium

### System Libraries
```bash
# Fedora/RHEL
sudo dnf install libxml2-devel libxslt-devel

# Ubuntu/Debian  
sudo apt-get install libxml2-dev libxslt-dev

# macOS
brew install libxml2 libxslt
```

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Development Workflow
```bash
# Code formatting
black .

# Linting
flake8 .

# Type checking
mypy .

# Run tests
pytest tests/ -v

# Security check
python security_check.py
```

### Application Execution
```bash
# Basic usage
python main.py /path/to/pdfs output.xlsx

# With configuration
python main.py --config config.py /path/to/pdfs output.xlsx

# Batch processing
python main.py --workers 4 /path/to/pdfs output.xlsx
```

## Configuration Management

### Environment Variables
- **DEFAULT_INPUT_PATH**: Default PDF input directory
- **DEFAULT_OUTPUT_PATH**: Default report output directory
- **SELENIUM_TIMEOUT_***: Web scraping timeout configurations
- **MAX_WORKERS**: Parallel processing thread count
- **LOG_LEVEL**: Logging verbosity level

### Configuration Files
- **`.env`**: Environment-specific settings
- **`config.py`**: Application configuration with validation
- **`requirements.txt`**: Python dependencies with versions

## Build & Deployment

### Installation Script
```bash
# Automated setup
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Docker Support (Future)
- Containerized deployment capability
- Isolated environment with all dependencies
- Scalable processing infrastructure

## Performance Considerations

### Processing Optimization
- **Multi-threading**: Configurable worker threads (1-8)
- **Batch Processing**: Efficient memory usage for large PDF sets
- **Zoom Levels**: Configurable QR detection parameters (2,3,4,5,6)
- **DPI Settings**: Adjustable image resolution (150,200,300)

### Memory Management
- **Streaming PDF Processing**: Avoid loading entire files in memory
- **Garbage Collection**: Explicit cleanup of large objects
- **Resource Limits**: Configurable timeouts and limits

## Security Features

### Dependency Security
- **Version Pinning**: Specific versions to avoid known vulnerabilities
- **Security Updates**: Regular dependency updates
- **Vulnerability Scanning**: Automated security checks

### Runtime Security
- **Input Validation**: All file paths and URLs validated
- **Sandboxing**: Selenium runs in controlled environment
- **Logging**: Security events tracked and auditable