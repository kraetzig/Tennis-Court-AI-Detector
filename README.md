# Tennis Court Classifier

Aplicação web para classificação de quadras de tênis usando AWS Rekognition Custom Labels.

## Arquitetura

- **Frontend**: HTML/JS hospedado no S3 + CloudFront
- **Backend**: AWS Lambda + API Gateway
- **Storage**: S3 para imagens
- **ML**: AWS Rekognition Custom Labels
- **DNS**: Route 53 para gerenciamento de domínio
- **SSL/TLS**: ACM (AWS Certificate Manager)

## Estrutura do Projeto

```
tennis-court-app/
├── frontend/          # Arquivos web (HTML, JS, CSS)
├── lambda/           # Funções Lambda
├── scripts/          # Scripts de deploy
├── docs/            # Documentação
└── infrastructure/   # Configurações AWS (Route 53, ACM, CloudFront)
```

## Deploy Completo

### 1. Configurar DNS e SSL
```bash
./scripts/deploy-dns-ssl.sh
```

### 2. Deploy da aplicação
```bash
./scripts/deploy_complete.sh
```

### 3. Configurar registros DNS
- Aponte os nameservers do seu domínio para o Route 53
- Aguarde propagação DNS (até 48h)

## Serviços AWS Utilizados

- **S3**: Hospedagem do frontend e armazenamento de imagens
- **CloudFront**: CDN global com domínio customizado
- **Lambda**: Processamento serverless das imagens
- **API Gateway**: REST API para comunicação
- **Rekognition**: Machine Learning para classificação
- **Route 53**: Gerenciamento DNS
- **ACM**: Certificados SSL/TLS gratuitos

## URL da Aplicação

https://tennis-court.kraetzig-cloud.com.br/
