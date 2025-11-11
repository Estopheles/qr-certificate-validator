# ☁️ Guía de Despliegue en la Nube

Guía completa para desplegar QR Certificate Validator en AWS, Azure y Google Cloud Platform con optimización de costos.

## 🎯 Resumen Ejecutivo

Basado en las métricas de rendimiento capturadas, este documento proporciona recomendaciones específicas para desplegar el sistema en la nube de manera costo-efectiva.

## 📊 Análisis de Requerimientos

### Recursos Típicos Medidos

| Carga de Trabajo | CPU Promedio | RAM Máxima | Duración | Archivos |
|------------------|--------------|------------|----------|----------|
| **Ligera** | 15% | 200MB | 2 min | 10 PDFs |
| **Media** | 45% | 600MB | 30 min | 100 PDFs |
| **Pesada** | 70% | 1.2GB | 2 horas | 500+ PDFs |

### Recomendaciones por Escenario

#### 🟢 Carga Ligera (Uso Ocasional)
- **AWS**: t3.small (2 vCPUs, 2GB RAM) - $15.12/mes
- **Azure**: B2s (2 vCPUs, 4GB RAM) - $30.00/mes  
- **GCP**: e2-small (1 vCPU, 2GB RAM) - $12.16/mes

#### 🟡 Carga Media (Uso Regular)
- **AWS**: t3.medium (2 vCPUs, 4GB RAM) - $30.24/mes
- **Azure**: D2s_v3 (2 vCPUs, 8GB RAM) - $69.60/mes
- **GCP**: e2-standard-2 (2 vCPUs, 8GB RAM) - $48.72/mes

#### 🔴 Carga Pesada (Uso Intensivo)
- **AWS**: m5.large (2 vCPUs, 8GB RAM) - $69.60/mes
- **Azure**: D4s_v3 (4 vCPUs, 16GB RAM) - $139.20/mes
- **GCP**: e2-standard-4 (4 vCPUs, 16GB RAM) - $97.44/mes

## 🚀 AWS Deployment

### EC2 Setup

```bash
# 1. Crear instancia EC2
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.small \
    --key-name my-key-pair \
    --security-group-ids sg-903004f8 \
    --subnet-id subnet-6e7f829e

# 2. Conectar a la instancia
ssh -i "my-key-pair.pem" ec2-user@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
```

### Configuración del Servidor

```bash
# Actualizar sistema
sudo yum update -y

# Instalar Python 3.9+
sudo yum install python39 python39-pip -y

# Instalar dependencias del sistema
sudo yum install libxml2-devel libxslt-devel chromium -y

# Clonar repositorio
git clone https://github.com/tu-usuario/qr-certificate-validator.git
cd qr-certificate-validator

# Configurar entorno
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
nano .env
```

### Lambda Function (Serverless)

```python
# lambda_function.py
import json
import boto3
from main import main

def lambda_handler(event, context):
    """Handler para AWS Lambda"""
    
    # Obtener parámetros del evento
    input_bucket = event.get('input_bucket')
    input_key = event.get('input_key')
    output_bucket = event.get('output_bucket')
    
    # Descargar PDFs desde S3
    s3 = boto3.client('s3')
    s3.download_file(input_bucket, input_key, '/tmp/input.pdf')
    
    # Procesar
    results = main('/tmp/', '/tmp/output.xlsx')
    
    # Subir resultados a S3
    s3.upload_file('/tmp/output.xlsx', output_bucket, 'results.xlsx')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Procesamiento completado',
            'results_count': len(results)
        })
    }
```

### ECS/Fargate (Contenedores)

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libxml2-dev libxslt-dev \
    chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Comando por defecto
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  qr-validator:
    build: .
    environment:
      - SELENIUM_TIMEOUT_SHORT=10
      - MAX_WORKERS=4
    volumes:
      - ./data:/app/data
      - ./output:/app/output
    command: python main.py /app/data /app/output/results.xlsx
```

## 🔷 Azure Deployment

### Virtual Machine

```bash
# Crear grupo de recursos
az group create --name qr-validator-rg --location eastus

# Crear VM
az vm create \
    --resource-group qr-validator-rg \
    --name qr-validator-vm \
    --image UbuntuLTS \
    --size Standard_B2s \
    --admin-username azureuser \
    --generate-ssh-keys

# Conectar
ssh azureuser@<public-ip>
```

### Container Instances

```yaml
# azure-container.yaml
apiVersion: 2019-12-01
location: eastus
name: qr-validator-container
properties:
  containers:
  - name: qr-validator
    properties:
      image: tu-registry/qr-validator:latest
      resources:
        requests:
          cpu: 2
          memoryInGb: 4
      environmentVariables:
      - name: SELENIUM_TIMEOUT_SHORT
        value: '10'
  osType: Linux
  restartPolicy: OnFailure
```

```bash
# Desplegar
az container create --resource-group qr-validator-rg --file azure-container.yaml
```

### Azure Functions

```python
# __init__.py
import azure.functions as func
from main import main

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function handler"""
    
    # Obtener archivos del request
    files = req.files.getlist('pdfs')
    
    # Procesar archivos
    results = []
    for file in files:
        # Guardar temporalmente
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, 'wb') as f:
            f.write(file.read())
        
        # Procesar
        file_results = main(temp_path, f"/tmp/output_{file.filename}.xlsx")
        results.extend(file_results)
    
    return func.HttpResponse(
        json.dumps({"results_count": len(results)}),
        mimetype="application/json"
    )
```

## 🟡 Google Cloud Platform

### Compute Engine

```bash
# Crear instancia
gcloud compute instances create qr-validator-vm \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB

# Conectar
gcloud compute ssh qr-validator-vm --zone=us-central1-a
```

### Cloud Run (Serverless)

```dockerfile
# Dockerfile para Cloud Run
FROM python:3.9-slim

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    libxml2-dev libxslt-dev chromium \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Cloud Run requiere puerto 8080
EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

```python
# app.py - Flask wrapper para Cloud Run
from flask import Flask, request, jsonify
from main import main
import tempfile
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_pdfs():
    """Endpoint para procesar PDFs"""
    
    files = request.files.getlist('pdfs')
    results = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            # Guardar archivo
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)
            
            # Procesar
            output_path = os.path.join(temp_dir, f"output_{file.filename}.xlsx")
            file_results = main(file_path, output_path)
            results.extend(file_results)
    
    return jsonify({"results_count": len(results)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

```bash
# Desplegar a Cloud Run
gcloud run deploy qr-validator \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Google Kubernetes Engine

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qr-validator
spec:
  replicas: 2
  selector:
    matchLabels:
      app: qr-validator
  template:
    metadata:
      labels:
        app: qr-validator
    spec:
      containers:
      - name: qr-validator
        image: gcr.io/tu-proyecto/qr-validator:latest
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi
        env:
        - name: SELENIUM_TIMEOUT_SHORT
          value: "10"
---
apiVersion: v1
kind: Service
metadata:
  name: qr-validator-service
spec:
  selector:
    app: qr-validator
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 💰 Optimización de Costos

### Estrategias Generales

#### 1. Instancias Spot/Preemptible
```bash
# AWS Spot Instances (50-90% descuento)
aws ec2 request-spot-instances \
    --spot-price "0.05" \
    --instance-count 1 \
    --type "one-time" \
    --launch-specification file://spot-specification.json

# GCP Preemptible (hasta 80% descuento)
gcloud compute instances create qr-validator-spot \
    --preemptible \
    --machine-type=e2-standard-2
```

#### 2. Auto Scaling
```yaml
# AWS Auto Scaling
Resources:
  AutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 0
      MaxSize: 10
      DesiredCapacity: 1
      TargetGroupARNs:
        - !Ref TargetGroup
      LaunchTemplate:
        LaunchTemplateId: !Ref LaunchTemplate
        Version: !GetAtt LaunchTemplate.LatestVersionNumber
```

#### 3. Scheduled Scaling
```bash
# Programar instancias solo durante horas de trabajo
# AWS CloudWatch Events
aws events put-rule \
    --name "start-qr-validator" \
    --schedule-expression "cron(0 8 * * MON-FRI)"

aws events put-rule \
    --name "stop-qr-validator" \
    --schedule-expression "cron(0 18 * * MON-FRI)"
```

### Comparación de Costos Mensual

| Escenario | AWS | Azure | GCP | Mejor Opción |
|-----------|-----|-------|-----|--------------|
| **Ocasional (10h/mes)** | $3.02 | $6.00 | $2.43 | 🏆 GCP |
| **Regular (40h/mes)** | $12.10 | $24.00 | $9.73 | 🏆 GCP |
| **Intensivo (160h/mes)** | $48.38 | $96.00 | $38.91 | 🏆 GCP |
| **24/7** | $30.24 | $69.60 | $48.72 | 🏆 AWS |

### Calculadora de Costos

```python
# scripts/cost_calculator.py - Uso extendido
def calculate_monthly_cost(hours_per_month, instance_type, provider):
    """Calcular costo mensual basado en uso real"""
    
    costs = {
        'aws': {'t3.small': 0.0208, 't3.medium': 0.0416},
        'azure': {'B2s': 0.0416, 'D2s_v3': 0.096},
        'gcp': {'e2-small': 0.0168, 'e2-standard-2': 0.0672}
    }
    
    hourly_cost = costs[provider][instance_type]
    monthly_cost = hourly_cost * hours_per_month
    
    # Descuentos por volumen
    if hours_per_month > 100:
        monthly_cost *= 0.9  # 10% descuento
    
    return monthly_cost

# Ejemplo de uso
cost = calculate_monthly_cost(40, 't3.small', 'aws')
print(f"Costo mensual: ${cost:.2f}")
```

## 🔧 Configuración de Producción

### Variables de Entorno

```bash
# .env.production
ENVIRONMENT=production
LOG_LEVEL=INFO
SELENIUM_TIMEOUT_SHORT=15
SELENIUM_TIMEOUT_MEDIUM=30
SELENIUM_TIMEOUT_LONG=60
MAX_WORKERS=4
MONITOR_INTERVAL=1.0

# Configuración de nube
CLOUD_PROVIDER=aws
INSTANCE_TYPE=t3.medium
REGION=us-east-1

# Almacenamiento
INPUT_BUCKET=qr-validator-input
OUTPUT_BUCKET=qr-validator-output
METRICS_BUCKET=qr-validator-metrics
```

### Monitoreo y Alertas

```yaml
# cloudwatch-alarms.yaml (AWS)
Resources:
  HighCPUAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: QR-Validator-High-CPU
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      
  HighMemoryAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: QR-Validator-High-Memory
      MetricName: MemoryUtilization
      Namespace: CWAgent
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 85
      ComparisonOperator: GreaterThanThreshold
```

### Backup y Recuperación

```bash
# Script de backup automático
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/qr-validator-$DATE"

# Crear backup
mkdir -p $BACKUP_DIR
cp -r /app/data $BACKUP_DIR/
cp -r /app/output $BACKUP_DIR/
cp -r /app/logs $BACKUP_DIR/

# Comprimir
tar -czf "$BACKUP_DIR.tar.gz" $BACKUP_DIR
rm -rf $BACKUP_DIR

# Subir a S3
aws s3 cp "$BACKUP_DIR.tar.gz" s3://qr-validator-backups/

# Limpiar backups antiguos (mantener 30 días)
find /backup -name "qr-validator-*.tar.gz" -mtime +30 -delete
```

## 🚨 Troubleshooting

### Problemas Comunes

**Error: Chrome/Chromium no encontrado**
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# Amazon Linux
sudo yum install chromium

# Alpine Linux (Docker)
apk add chromium chromium-chromedriver
```

**Error: Memoria insuficiente**
```bash
# Aumentar swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Error: Timeout en web scraping**
```python
# Aumentar timeouts en producción
SELENIUM_TIMEOUT_SHORT=30
SELENIUM_TIMEOUT_MEDIUM=60
SELENIUM_TIMEOUT_LONG=120
```

### Logs y Debugging

```bash
# Ver logs en tiempo real
tail -f /app/logs/qr_validator.log

# Logs de sistema
journalctl -u qr-validator -f

# Métricas de sistema
htop
iostat -x 1
```

## 📚 Recursos Adicionales

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Calculadoras de Precios](#calculadoras-de-precios)

### Calculadoras de Precios

- **AWS**: https://calculator.aws
- **Azure**: https://azure.microsoft.com/pricing/calculator/
- **GCP**: https://cloud.google.com/products/calculator

## 🤝 Soporte

Para soporte con despliegues en la nube:

1. **Issues de GitHub**: Para problemas técnicos
2. **Discussions**: Para preguntas generales
3. **Email**: support@qr-validator.com

¡Despliega con confianza! 🚀