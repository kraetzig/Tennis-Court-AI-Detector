import json
import boto3
import base64
import time

def lambda_handler(event, context):
    """
    Lambda otimizada para detectar superfícies de quadra com maior precisão
    """
    
    rekognition = boto3.client('rekognition')
    MODEL_ARN = "arn:aws:rekognition:us-east-1:213899361839:project/tennis-court-detector/version/tennis-court-detector.2025-10-20T14.38.19/1760981900018"
    
    try:
        # Decodificar imagem
        if 'body' in event:
            body = json.loads(event['body'])
            image_data = base64.b64decode(body['image'])
        else:
            image_data = base64.b64decode(event['image'])
        
        # Verificar e iniciar modelo se necessário
        ensure_model_running(rekognition, MODEL_ARN)
        
        # Detectar com confiança mais baixa para capturar mais detalhes
        response = rekognition.detect_custom_labels(
            ProjectVersionArn=MODEL_ARN,
            Image={'Bytes': image_data},
            MinConfidence=30  # Reduzido para capturar mais detecções
        )
        
        # Processar com lógica melhorada
        result = enhanced_detection_logic(response)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(result, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'detected': False
            }, ensure_ascii=False)
        }

def ensure_model_running(rekognition, model_arn):
    """Garante que o modelo está rodando"""
    try:
        project_arn = model_arn.split('/version/')[0]
        response = rekognition.describe_project_versions(ProjectArn=project_arn)
        
        for version in response['ProjectVersionDescriptions']:
            if version['ProjectVersionArn'] == model_arn:
                if version['Status'] == 'STOPPED':
                    rekognition.start_project_version(
                        ProjectVersionArn=model_arn,
                        MinInferenceUnits=1
                    )
                    # Aguardar inicialização
                    for i in range(30):
                        time.sleep(10)
                        status_response = rekognition.describe_project_versions(ProjectArn=project_arn)
                        for v in status_response['ProjectVersionDescriptions']:
                            if v['ProjectVersionArn'] == model_arn and v['Status'] == 'RUNNING':
                                return
                break
    except Exception as e:
        print(f"Erro ao verificar modelo: {e}")

def enhanced_detection_logic(response):
    """Lógica melhorada para processar detecções"""
    
    surface_keywords = {
        'saibro': ['clay', 'saibro', 'terra', 'red', 'vermelho'],
        'grama': ['grass', 'grama', 'green', 'verde'],
        'rapida': ['hard', 'rapida', 'rápida', 'blue', 'azul', 'concrete']
    }
    
    if not response['CustomLabels']:
        return {
            'surface': 'não identificada',
            'confidence': 0,
            'detected': False,
            'message': 'Nenhuma superfície detectada',
            'suggestions': 'Tente uma imagem mais clara da quadra'
        }
    
    # Agrupar detecções por tipo
    detections_by_type = {'saibro': [], 'grama': [], 'rapida': []}
    
    for detection in response['CustomLabels']:
        label_name = detection['Name'].lower()
        confidence = detection['Confidence']
        
        # Classificar por palavras-chave
        for surface_type, keywords in surface_keywords.items():
            if any(keyword in label_name for keyword in keywords):
                detections_by_type[surface_type].append({
                    'name': detection['Name'],
                    'confidence': confidence
                })
                break
    
    # Encontrar melhor detecção
    best_surface = None
    best_confidence = 0
    
    for surface_type, detections in detections_by_type.items():
        if detections:
            # Usar a maior confiança do tipo
            max_confidence = max(d['confidence'] for d in detections)
            if max_confidence > best_confidence:
                best_confidence = max_confidence
                best_surface = surface_type
    
    if best_surface and best_confidence > 40:  # Confiança mínima
        return {
            'surface': best_surface,
            'confidence': round(best_confidence, 2),
            'detected': True,
            'all_detections': [
                {
                    'surface': get_surface_type(label['Name']),
                    'confidence': round(label['Confidence'], 2),
                    'raw_name': label['Name']
                }
                for label in response['CustomLabels']
            ],
            'detection_count': len(response['CustomLabels'])
        }
    else:
        return {
            'surface': 'incerta',
            'confidence': round(best_confidence, 2) if best_confidence > 0 else 0,
            'detected': False,
            'message': f'Detecção com baixa confiança ({best_confidence:.1f}%)',
            'all_detections': [
                {
                    'surface': get_surface_type(label['Name']),
                    'confidence': round(label['Confidence'], 2),
                    'raw_name': label['Name']
                }
                for label in response['CustomLabels']
            ]
        }

def get_surface_type(label_name):
    """Mapeia nome do label para tipo de superfície"""
    label_lower = label_name.lower()
    
    if any(word in label_lower for word in ['clay', 'saibro', 'terra', 'red']):
        return 'saibro'
    elif any(word in label_lower for word in ['grass', 'grama', 'green']):
        return 'grama'
    elif any(word in label_lower for word in ['hard', 'rapida', 'rápida', 'blue', 'concrete']):
        return 'rapida'
    else:
        return label_name
