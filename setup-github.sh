#!/bin/bash

# Substitua 'SEU_USUARIO' pelo seu username do GitHub
GITHUB_USERNAME="SEU_USUARIO"
REPO_NAME="tennis-court-classifier"

echo "Configurando repositório remoto..."
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

echo "Renomeando branch para main..."
git branch -M main

echo "Fazendo push inicial..."
git push -u origin main

echo "Repositório configurado! Acesse:"
echo "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
