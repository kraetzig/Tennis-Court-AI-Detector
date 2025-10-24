import json
import base64
import boto3
from PIL import Image
import io

def lambda_handler(event, context):
    try:
        # Parse do body da requisição
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
            
        # Extrair dados da imagem
        image_data = body.get('image')
        
        if not image_data:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'erro': 'Imagem não encontrada'})
            }
        
        # Decodificar base64
        image_bytes = base64.b64decode(image_data)
        
        # Usar Rekognition para detectar labels
        rekognition = boto3.client('rekognition')
        
        response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=50
        )
        
        # Extrair labels detectados
        labels = []
        for label in response['Labels']:
            labels.append(f"{label['Name']}({label['Confidence']:.1f}%)")
        
        # Lógica simples para classificar tipo de quadra baseado nas cores/labels
        tipo_quadra = "rapida"  # default
        confianca = 75
        
        # Verificar se há predominância de verde (grama)
        for label in response['Labels']:
            if label['Name'].lower() in ['green', 'grass', 'lawn'] and label['Confidence'] > 80:
                tipo_quadra = "grama"
                confianca = min(95, label['Confidence'])
                break
            elif label['Name'].lower() in ['brown', 'clay', 'dirt', 'soil'] and label['Confidence'] > 70:
                tipo_quadra = "saibro"
                confianca = min(90, label['Confidence'])
                break
            elif label['Name'].lower() in ['blue', 'court', 'asphalt'] and label['Confidence'] > 70:
                tipo_quadra = "rapida"
                confianca = min(85, label['Confidence'])
                break
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'surface': tipo_quadra,
                'confidence': confianca
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'erro': str(e)})
        }
