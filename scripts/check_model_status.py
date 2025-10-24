#!/usr/bin/env python3
import boto3
import json

def check_rekognition_status():
    """Verifica status do modelo e obtém ARN"""
    
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    
    print("🔍 Verificando projetos do Rekognition...")
    
    try:
        # Listar projetos
        projects = rekognition.describe_projects()
        
        if not projects['ProjectDescriptions']:
            print("❌ Nenhum projeto encontrado")
            return
            
        for project in projects['ProjectDescriptions']:
            project_name = project['ProjectArn'].split('/')[-1]
            print(f"\n📁 Projeto: {project_name}")
            print(f"   ARN: {project['ProjectArn']}")
            print(f"   Status: {project['Status']}")
            
            # Verificar versões do modelo
            try:
                versions = rekognition.describe_project_versions(
                    ProjectArn=project['ProjectArn']
                )
                
                for version in versions['ProjectVersionDescriptions']:
                    version_name = version['ProjectVersionArn'].split('/')[-1]
                    print(f"\n   🤖 Modelo: {version_name}")
                    print(f"      ARN: {version['ProjectVersionArn']}")
                    print(f"      Status: {version['Status']}")
                    
                    if 'EvaluationResult' in version:
                        eval_result = version['EvaluationResult']
                        print(f"      F1 Score: {eval_result.get('F1Score', 'N/A')}")
                        print(f"      Precisão: {eval_result.get('Summary', {}).get('S3Object', 'N/A')}")
                    
                    # Se está TRAINING_COMPLETED, mostrar como iniciar
                    if version['Status'] == 'TRAINING_COMPLETED':
                        print(f"      ✅ Modelo pronto para uso!")
                        print(f"      💡 Para iniciar: aws rekognition start-project-version --project-version-arn {version['ProjectVersionArn']} --min-inference-units 1")
                        
                        # Salvar ARN para uso posterior
                        with open('/home/ec2-user/model_arn.txt', 'w') as f:
                            f.write(version['ProjectVersionArn'])
                        print(f"      📝 ARN salvo em model_arn.txt")
                    
                    elif version['Status'] == 'RUNNING':
                        print(f"      🟢 Modelo está RODANDO (cobrando $4/hora)")
                        print(f"      💰 Para parar: aws rekognition stop-project-version --project-version-arn {version['ProjectVersionArn']}")
                        
                    elif version['Status'] == 'STOPPED':
                        print(f"      🔴 Modelo parado (modo econômico)")
                        
            except Exception as e:
                print(f"   ❌ Erro ao verificar versões: {e}")
                
    except Exception as e:
        print(f"❌ Erro ao acessar Rekognition: {e}")
        print("💡 Verifique suas permissões AWS")

if __name__ == "__main__":
    check_rekognition_status()
