#!/bin/bash

echo "Cole seu token de acesso pessoal do GitHub:"
read -s TOKEN

echo "Fazendo push para o repositório..."
git push https://kraetzig:$TOKEN@github.com/kraetzig/Tennis-Court-AI-Detector.git main

echo "Push concluído! Acesse: https://github.com/kraetzig/Tennis-Court-AI-Detector"
