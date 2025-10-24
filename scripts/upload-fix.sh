#!/bin/bash

# Upload do arquivo corrigido para o S3
aws s3 cp /home/ec2-user/index-fixed.html s3://tennis-court-web/index.html --content-type "text/html"

# Invalidar cache do CloudFront
aws cloudfront create-invalidation --distribution-id E2991UZQ5WBEC6 --paths "/*"

echo "Upload concluído e cache invalidado!"
