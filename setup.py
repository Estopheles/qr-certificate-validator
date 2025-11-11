from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qr-certificate-validator",
    version="2.0.0",
    description="Sistema automatizado para extraer y validar códigos QR de certificados PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Christhian Rodríguez",
    author_email="christhian057@gmail.com",
    url="https://github.com/christhianrodriguez/qr-certificate-validator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "PyMuPDF>=1.24.0",
        "pikepdf>=8.15.0",
        "opencv-python>=4.9.0",
        "pyzbar>=0.1.9",
        "pillow>=10.2.0",
        "selenium>=4.17.0",
        "beautifulsoup4>=4.12.2",
        "lxml>=4.9.3",
        "urllib3>=2.0.0",
        "pandas>=2.2.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.2",
        "tqdm>=4.66.1",
        "python-dotenv>=1.0.0",
        "click>=8.1.7",
        "cryptography>=41.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
            "bandit>=1.7.5",
            "pre-commit>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "qr-validator=qr_validator.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="qr-code pdf certificate validation security automation",
    project_urls={
        "Bug Reports": "https://github.com/christhianrodriguez/qr-certificate-validator/issues",
        "Source": "https://github.com/christhianrodriguez/qr-certificate-validator",
        "Documentation": "https://github.com/christhianrodriguez/qr-certificate-validator/docs",
    },
)