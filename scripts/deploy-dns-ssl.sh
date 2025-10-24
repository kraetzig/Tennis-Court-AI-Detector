#!/bin/bash

# Deploy DNS and SSL for Tennis Court AI Detector
# Run this script to set up Route 53 and ACM certificate

set -e

DOMAIN="kraetzig-cloud.com.br"
SUBDOMAIN="tennis-court.kraetzig-cloud.com.br"
REGION="us-east-1"

echo "🚀 Setting up DNS and SSL for Tennis Court AI Detector..."

# 1. Create Route 53 Hosted Zone
echo "📡 Creating Route 53 hosted zone..."
HOSTED_ZONE_ID=$(aws route53 create-hosted-zone \
  --name $DOMAIN \
  --caller-reference "tennis-court-$(date +%s)" \
  --hosted-zone-config Comment="Tennis Court AI Detector DNS" \
  --query 'HostedZone.Id' \
  --output text \
  --region $REGION)

echo "✅ Hosted Zone created: $HOSTED_ZONE_ID"

# 2. Request ACM Certificate
echo "🔒 Requesting SSL certificate..."
CERT_ARN=$(aws acm request-certificate \
  --domain-name $SUBDOMAIN \
  --subject-alternative-names "*.$DOMAIN" \
  --validation-method DNS \
  --region $REGION \
  --query 'CertificateArn' \
  --output text)

echo "✅ Certificate requested: $CERT_ARN"

# 3. Get certificate validation records
echo "📋 Getting DNS validation records..."
aws acm describe-certificate \
  --certificate-arn $CERT_ARN \
  --region $REGION \
  --query 'Certificate.DomainValidationOptions[0].ResourceRecord' \
  --output table

echo ""
echo "🎯 Next steps:"
echo "1. Add the DNS validation record to your domain registrar"
echo "2. Wait for certificate validation (5-30 minutes)"
echo "3. Update CloudFront distribution with the certificate"
echo "4. Create A record pointing to CloudFront distribution"
echo ""
echo "📝 Save these values:"
echo "Hosted Zone ID: $HOSTED_ZONE_ID"
echo "Certificate ARN: $CERT_ARN"
