#!/bin/bash

echo "🎾 Deploy Completo - Detector de Superfícies Econômico"
echo "=================================================="

# Variáveis
ACCOUNT_ID="213899361839"
REGION="us-east-1"
ROLE_NAME="lambda-rekognition-economic-role"

# Passo 1: Verificar modelo
echo "📋 Passo 1: Verificando status do modelo..."
python3 check_model_status.py

if [ ! -f "model_arn.txt" ]; then
    echo "❌ ARN do modelo não encontrado!"
    echo "💡 Execute primeiro: python3 check_model_status.py"
    exit 1
fi

MODEL_ARN=$(cat model_arn.txt)
echo "✅ Modelo encontrado: $MODEL_ARN"

# Passo 2: Criar role IAM se não existir
echo "📋 Passo 2: Configurando permissões IAM..."

cat > trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

cat > lambda-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectCustomLabels",
                "rekognition:StartProjectVersion",
                "rekognition:StopProjectVersion",
                "rekognition:DescribeProjectVersions"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "events:PutRule",
                "events:PutTargets",
                "events:RemoveTargets",
                "events:DeleteRule"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "*"
        }
    ]
}
EOF

# Criar role
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document file://trust-policy.json \
    --region $REGION 2>/dev/null || echo "Role já existe"

aws iam put-role-policy \
    --role-name $ROLE_NAME \
    --policy-name LambdaRekognitionPolicy \
    --policy-document file://lambda-policy.json \
    --region $REGION

ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME"
echo "✅ Role configurada: $ROLE_ARN"

# Passo 3: Atualizar ARN no código
echo "📋 Passo 3: Atualizando código com ARN do modelo..."
sed -i "s|SEU_MODEL_ARN_AQUI|$MODEL_ARN|g" lambda_economic_tennis.py
echo "✅ ARN atualizado no código"

# Passo 4: Criar pacotes Lambda
echo "📋 Passo 4: Criando pacotes Lambda..."
zip -r tennis-economic-lambda.zip lambda_economic_tennis.py
zip -r stop-model-lambda.zip lambda_stop_model.py

# Passo 5: Deploy das funções
echo "📋 Passo 5: Fazendo deploy das funções Lambda..."

# Função principal
aws lambda create-function \
    --function-name tennis-surface-economic \
    --runtime python3.9 \
    --role $ROLE_ARN \
    --handler lambda_economic_tennis.lambda_handler \
    --zip-file fileb://tennis-economic-lambda.zip \
    --timeout 300 \
    --memory-size 512 \
    --region $REGION 2>/dev/null || \
aws lambda update-function-code \
    --function-name tennis-surface-economic \
    --zip-file fileb://tennis-economic-lambda.zip \
    --region $REGION

# Função para parar modelo
aws lambda create-function \
    --function-name stop-rekognition-model \
    --runtime python3.9 \
    --role $ROLE_ARN \
    --handler lambda_stop_model.lambda_handler \
    --zip-file fileb://stop-model-lambda.zip \
    --timeout 60 \
    --memory-size 128 \
    --region $REGION 2>/dev/null || \
aws lambda update-function-code \
    --function-name stop-rekognition-model \
    --zip-file fileb://stop-model-lambda.zip \
    --region $REGION

echo "✅ Funções Lambda criadas!"

# Passo 6: Configurar API Gateway
echo "📋 Passo 6: Configurando API Gateway..."

API_ID=$(aws apigateway create-rest-api \
    --name tennis-surface-api \
    --region $REGION \
    --query 'id' --output text 2>/dev/null || \
aws apigateway get-rest-apis \
    --query 'items[?name==`tennis-surface-api`].id' \
    --output text --region $REGION)

echo "API Gateway ID: $API_ID"

# Obter root resource
ROOT_ID=$(aws apigateway get-resources \
    --rest-api-id $API_ID \
    --region $REGION \
    --query 'items[?path==`/`].id' --output text)

# Criar resource /detect
RESOURCE_ID=$(aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_ID \
    --path-part detect \
    --region $REGION \
    --query 'id' --output text 2>/dev/null || \
aws apigateway get-resources \
    --rest-api-id $API_ID \
    --region $REGION \
    --query 'items[?pathPart==`detect`].id' --output text)

# Criar método POST
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method POST \
    --authorization-type NONE \
    --region $REGION 2>/dev/null || echo "Método já existe"

# Integrar com Lambda
LAMBDA_ARN="arn:aws:lambda:$REGION:$ACCOUNT_ID:function:tennis-surface-economic"

aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method POST \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations" \
    --region $REGION

# Dar permissão para API Gateway invocar Lambda
aws lambda add-permission \
    --function-name tennis-surface-economic \
    --statement-id api-gateway-invoke \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/*/*" \
    --region $REGION 2>/dev/null || echo "Permissão já existe"

# Deploy da API
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod \
    --region $REGION

API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/prod/detect"

echo "=================================================="
echo "✅ DEPLOY CONCLUÍDO COM SUCESSO!"
echo "=================================================="
echo "🔗 URL da API: $API_URL"
echo "🎾 Função Lambda: tennis-surface-economic"
echo "💰 Modo Econômico: Modelo inicia/para automaticamente"
echo "⏰ Auto-stop: 2 minutos após uso"
echo ""
echo "📝 Próximos passos:"
echo "1. Teste a API com: curl -X POST $API_URL -d '{\"image\":\"BASE64_DA_IMAGEM\"}'"
echo "2. Atualize o frontend com a nova URL"
echo "3. Monitore custos no CloudWatch"

# Limpar arquivos temporários
rm -f trust-policy.json lambda-policy.json tennis-economic-lambda.zip stop-model-lambda.zip
