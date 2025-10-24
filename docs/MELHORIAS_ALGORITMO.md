# 🎾 Melhorias no Algoritmo de Detecção de Quadras de Tênis

## 🚀 Principais Melhorias Implementadas

### 1. **Análise Multi-Dimensional**
- **Cor Dominante**: Análise aprimorada em espaços RGB e HSV
- **Textura**: Filtros de Gabor e análise de variância local
- **Padrões Visuais**: Detecção de linhas, contornos e uniformidade

### 2. **Otimizações de Performance**
- Redimensionamento inteligente de imagens
- Análise focada na região central da imagem
- Processamento otimizado para Lambda

### 3. **Maior Precisão**
- Combinação ponderada de múltiplos fatores
- Pesos otimizados para cada tipo de superfície
- Análise de região de interesse (ROI)

## 🎯 Características Detectadas por Superfície

### 🟤 **Saibro (Clay Court)**
- **Cor**: Tons terrosos/avermelhados (RGB: ~180,120,80)
- **Textura**: Rugosidade moderada, irregular
- **Padrões**: Poucos contornos definidos, superfície granular

### 🟢 **Grama (Grass Court)**  
- **Cor**: Tons verdes dominantes (Hue: ~60°)
- **Textura**: Alta variação, muito irregular
- **Padrões**: Muitos contornos pequenos, textura orgânica

### 🔵 **Rápida (Hard Court)**
- **Cor**: Tons azuis/cinzas uniformes
- **Textura**: Lisa, baixa variação
- **Padrões**: Linhas bem definidas, alta uniformidade

## 📊 Algoritmo de Scoring

```
Score Final = (Cor × 0.4) + (Textura × 0.35) + (Padrões × 0.25)
```

### Pesos Ajustados por Superfície:
- **Saibro**: Cor (40%) + Textura (35%) + Padrões (25%)
- **Grama**: Cor (45%) + Textura (30%) + Padrões (25%)  
- **Rápida**: Cor (35%) + Textura (40%) + Padrões (25%)

## 🔧 Como Fazer o Deploy

1. **Ajustar nome da função**:
   ```bash
   # Edite o arquivo deploy_lambda.sh
   FUNCTION_NAME="seu-nome-da-funcao"
   ```

2. **Executar deployment**:
   ```bash
   ./deploy_lambda.sh
   ```

3. **Testar aplicação**:
   - Acesse: https://tennis-court.kraetzig-cloud.com.br
   - Faça upload de imagens de teste

## 📈 Melhorias de Performance Esperadas

- **Precisão**: +25-30% em condições variadas de iluminação
- **Robustez**: Melhor detecção em ângulos diferentes
- **Velocidade**: Otimizada para execução em Lambda
- **Confiabilidade**: Análise multi-fatorial reduz falsos positivos

## 🧪 Testes Recomendados

Teste com imagens de:
- Diferentes ângulos de câmera
- Condições de iluminação variadas
- Quadras com marcações/linhas
- Imagens com qualidade baixa/alta

## 🔍 Debug e Monitoramento

O algoritmo retorna detalhes completos dos scores:
```json
{
  "tipo_quadra": "saibro",
  "confianca": 87.5,
  "detalhes": {
    "scores_cor": {...},
    "scores_textura": {...},
    "scores_padrao": {...},
    "scores_finais": {...}
  }
}
```
