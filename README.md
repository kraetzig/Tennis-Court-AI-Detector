# Tennis Court Classifier

Aplicação web para classificação de quadras de tênis usando AWS Rekognition Custom Labels.

## Arquitetura

- **Frontend**: HTML/JS hospedado no S3 + CloudFront
- **Backend**: AWS Lambda + API Gateway
- **Storage**: S3 para imagens
- **ML**: AWS Rekognition Custom Labels

## Estrutura do Projeto

```
tennis-court-app/
├── frontend/          # Arquivos web (HTML, JS, CSS)
├── lambda/           # Funções Lambda
├── scripts/          # Scripts de deploy
├── docs/            # Documentação
└── infrastructure/   # Configurações AWS (CloudFormation/CDK)
```

## Deploy

1. Configure suas credenciais AWS
2. Execute o script de deploy: `./scripts/deploy_complete.sh`
3. Acesse a aplicação via CloudFront

## URL da Aplicação

https://tennis-court.kraetzig-cloud.com.br/
