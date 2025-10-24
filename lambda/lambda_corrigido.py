import json
import boto3
import base64

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': ''
        }

    try:
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event

        if 'image' in body:
            image_data = base64.b64decode(body['image'])
        elif 'file' in body:
            image_data = base64.b64decode(body['file'])
        else:
            raise ValueError("Imagem não encontrada")

        response = rekognition.detect_labels(
            Image={'Bytes': image_data},
            MaxLabels=50,
            MinConfidence=40
        )

        court_type, confidence = classify_court_type_improved(response['Labels'])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'surface': court_type,
                'confidence': confidence,
                'labels_detectados': [f"{label['Name']}({label['Confidence']:.1f}%)" for label in response['Labels'][:10]]
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'erro': str(e)})
        }

def classify_court_type_improved(labels):
    label_dict = {}
    for label in labels:
        label_dict[label['Name'].lower()] = label['Confidence']

    scores = {'saibro': 0, 'grama': 0, 'rapida': 0}

    saibro_indicators = {'red': 15, 'orange': 12, 'brown': 10, 'clay': 20, 'dirt': 15}
    grama_indicators = {'grass': 20, 'green': 10, 'lawn': 18, 'vegetation': 12}
    rapida_indicators = {'blue': 15, 'concrete': 18, 'court': 12, 'hard': 10}

    for label_name, confidence in label_dict.items():
        conf_factor = confidence / 100.0

        if label_name in saibro_indicators:
            scores['saibro'] += saibro_indicators[label_name] * conf_factor
        if label_name in grama_indicators:
            scores['grama'] += grama_indicators[label_name] * conf_factor
        if label_name in rapida_indicators:
            scores['rapida'] += rapida_indicators[label_name] * conf_factor

    if max(scores.values()) < 3:
        return 'rapida', 50

    winner = max(scores, key=scores.get)
    confidence = min(95, 50 + max(scores.values()) * 5)

    return winner, confidence
