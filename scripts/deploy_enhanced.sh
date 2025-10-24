#!/bin/bash

echo "🚀 Fazendo deploy da detecção melhorada..."

# Criar pacote
zip -r lambda_enhanced.zip lambda_enhanced_detection.py

# Atualizar função Lambda
aws lambda update-function-code \
    --function-name tennis-court-detector \
    --zip-file fileb://lambda_enhanced.zip

echo "✅ Deploy concluído!"
echo "🎾 Testando detecção melhorada..."

# Limpar
rm lambda_enhanced.zip

echo "💡 A detecção agora:"
echo "   - Usa confiança mínima de 30% para capturar mais detalhes"
echo "   - Agrupa detecções por tipo de superfície"
echo "   - Usa lógica de palavras-chave para melhor classificação"
echo "   - Retorna mais informações sobre as detecções"
