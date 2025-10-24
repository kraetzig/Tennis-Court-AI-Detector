# Diagnóstico: Tennis Court AI Detector

## 🔍 Problema Identificado

A aplicação está retornando o erro "Erro na classificação: Erro na classificação" porque a função Lambda está falhando com erro 502 (Bad Gateway).

## 📊 Testes Realizados

1. **API Gateway**: ✅ Funcionando (CORS configurado corretamente)
2. **Função Lambda**: ❌ Falhando (erro 502 para qualquer requisição POST)
3. **Frontend**: ✅ Funcionando (código JavaScript correto)

## 🚨 Causa Raiz

A função Lambda `tennis-court-detector` está com problemas internos, possivelmente:

- Erro no código Python da função
- Dependências faltando (boto3, PIL, etc.)
- Timeout da função
- Problemas de permissões IAM
- Erro na configuração do Amazon Rekognition

## 🛠️ Soluções Recomendadas

### 1. Verificar Logs da Lambda
```bash
# Comando para verificar logs (requer permissões)
aws logs describe-log-streams --log-group-name "/aws/lambda/tennis-court-detector" --region us-east-1
aws logs get-log-events --log-group-name "/aws/lambda/tennis-court-detector" --log-stream-name "STREAM_NAME" --region us-east-1
```

### 2. Código Lambda Corrigido (Python)
```python
import json
import base64
import boto3
from PIL import Image
import io

def lambda_handler(event, context):
    try:
        # Parse do body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
            
        # Validar se tem imagem
        if 'image' not in body or not body['image']:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'erro': 'Campo image é obrigatório'})
            }
        
        # Decodificar imagem
        image_data = base64.b64decode(body['image'])
        
        # Validar se é uma imagem válida
        try:
            img = Image.open(io.BytesIO(image_data))
            img.verify()
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'erro': 'Imagem inválida'})
            }
        
        # Usar Amazon Rekognition
        rekognition = boto3.client('rekognition', region_name='us-east-1')
        
        response = rekognition.detect_labels(
            Image={'Bytes': image_data},
            MaxLabels=10,
            MinConfidence=70
        )
        
        # Lógica de classificação da quadra
        tipo_quadra = 'rapida'  # default
        confianca = 75.0
        
        # Analisar labels para determinar tipo
        for label in response['Labels']:
            name = label['Name'].lower()
            confidence = label['Confidence']
            
            if 'clay' in name or 'dirt' in name or 'sand' in name:
                tipo_quadra = 'saibro'
                confianca = confidence
                break
            elif 'grass' in name or 'lawn' in name:
                tipo_quadra = 'grama'
                confianca = confidence
                break
            elif 'court' in name or 'tennis' in name:
                tipo_quadra = 'rapida'
                confianca = confidence
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'tipo_quadra': tipo_quadra,
                'confianca': confianca
            })
        }
        
    except Exception as e:
        print(f"Erro na função Lambda: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'erro': f'Erro interno: {str(e)}'})
        }
```

### 3. Permissões IAM Necessárias
A função Lambda precisa das seguintes permissões:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectLabels",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

### 4. Configurações da Lambda
- **Runtime**: Python 3.9 ou superior
- **Timeout**: 30 segundos
- **Memory**: 512 MB
- **Layers**: Adicionar layer com PIL/Pillow se necessário

### 5. Teste Local da Função
```python
# test_lambda_local.py
import json
import base64

# Simular evento do API Gateway
event = {
    "body": json.dumps({
        "image": "base64_image_data_here"
    })
}

# Testar função
result = lambda_handler(event, {})
print(json.dumps(result, indent=2))
```

## 🔧 Próximos Passos

1. **Imediato**: Verificar logs da Lambda para erro específico
2. **Correção**: Atualizar código da função Lambda
3. **Teste**: Validar funcionamento com imagem de teste
4. **Deploy**: Atualizar aplicação web se necessário

## 📱 Versão Corrigida do Frontend

Criei uma versão melhorada em `tennis_app_fixed.html` com:
- Melhor tratamento de erros
- Validação de arquivos
- Feedback visual aprimorado
- Logs de debug no console
- Suporte a drag & drop

## 🎯 Resultado Esperado

Após as correções, a aplicação deve:
1. Aceitar upload de imagens
2. Processar com Amazon Rekognition
3. Retornar tipo de quadra (saibro/grama/rápida)
4. Mostrar nível de confiança
5. Exibir mensagens de erro claras
