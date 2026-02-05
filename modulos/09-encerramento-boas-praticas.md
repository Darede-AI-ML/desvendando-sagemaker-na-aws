# Módulo 9: Encerramento e Boas Práticas

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:
- Encerrar corretamente todos os recursos ativos
- Implementar boas práticas de segurança
- Gerenciar custos eficientemente
- Organizar projetos ML de forma profissional
- Identificar próximos passos no aprendizado

## Duração Estimada
20 minutos

---

## 1. Checklist de Limpeza de Recursos

### Por que é Importante?

⚠️ **Recursos não encerrados continuam gerando custos!**

Um notebook `ml.m5.xlarge` rodando 24/7:
- Custo/hora: $0.23
- Custo/dia: $5.52
- **Custo/mês: $165.60**

### Ordem de Limpeza

```mermaid
graph TD
    Start[Início da Limpeza]
    
    Stop1[1. Parar Apps]
    Stop2[2. Parar Notebooks]
    Stop3[3. Deletar Endpoints]
    Stop4[4. Deletar User Profiles*]
    Stop5[5. Deletar Domain*]
    Stop6[6. Deletar Buckets S3*]
    Stop7[7. Deletar CloudFormation Stacks*]
    
    Start --> Stop1
    Stop1 --> Stop2
    Stop2 --> Stop3
    Stop3 --> Stop4
    Stop4 --> Stop5
    Stop5 --> Stop6
    Stop6 --> Stop7
    
    Note1[* Apenas se necessário]
    
    style Stop1 fill:#ff9999
    style Stop2 fill:#ff9999
    style Stop3 fill:#ff9999
    style Stop4 fill:#ffeb99
    style Stop5 fill:#ffeb99
    style Stop6 fill:#ffeb99
    style Stop7 fill:#ffeb99
```

---

## 2. Parar Apps e Kernels

### Via SageMaker Studio

**Método 1: Interface do Studio**

1. No Studio, menu **File** → **Manage Apps and Terminals**
2. Visualize todas as apps rodando:
   - JupyterServer (system)
   - KernelGateway apps (ml.t3.medium, ml.m5.xlarge, etc.)
3. Para cada KernelGateway:
   - Clique em **Shut down**
   - Confirme a ação
4. Aguarde status mudar para `Deleted`

**⚠️ IMPORTANTE:** JupyterServer não gera custo significativo, mas KernelGateway apps sim!

### Via Console AWS

1. Console AWS → **SageMaker**
2. Menu lateral → **Domains**
3. Clique no seu domain
4. Selecione seu **User profile**
5. Aba **Apps**
6. Para cada app:
   - Selecione a app
   - **Actions** → **Delete**
   - Confirme

### Via AWS CLI

```bash
# Listar apps ativas
aws sagemaker list-apps \
  --region eu-central-1 \
  --query 'Apps[?Status==`InService`].[DomainId,UserProfileName,AppType,AppName]' \
  --output table

# Deletar app específica
aws sagemaker delete-app \
  --domain-id d-xxxxxxxxxxxx \
  --user-profile-name default-user \
  --app-type KernelGateway \
  --app-name datascience-1-0-ml-m5-xlarge-xxxxxxxxxxxx \
  --region eu-central-1

# Script para deletar TODAS as KernelGateway apps
#!/bin/bash
DOMAIN_ID="d-xxxxxxxxxxxx"
USER_PROFILE="default-user"

aws sagemaker list-apps \
  --domain-id-equals $DOMAIN_ID \
  --user-profile-name-equals $USER_PROFILE \
  --region eu-central-1 \
  --query 'Apps[?AppType==`KernelGateway` && Status==`InService`].AppName' \
  --output text | \
while read app_name; do
  echo "Deletando app: $app_name"
  aws sagemaker delete-app \
    --domain-id $DOMAIN_ID \
    --user-profile-name $USER_PROFILE \
    --app-type KernelGateway \
    --app-name $app_name \
    --region eu-central-1
done
```

### Via Python (Notebook)

```python
import boto3
import sagemaker

session = sagemaker.Session()
sm_client = boto3.client('sagemaker', region_name='eu-central-1')

domain_id = 'd-xxxxxxxxxxxx'
user_profile = 'default-user'

# Listar apps
response = sm_client.list_apps(
    DomainIdEquals=domain_id,
    UserProfileNameEquals=user_profile
)

print(f"Apps encontradas: {len(response['Apps'])}")

# Deletar KernelGateway apps
for app in response['Apps']:
    if app['AppType'] == 'KernelGateway' and app['Status'] == 'InService':
        print(f"Deletando: {app['AppName']}")
        sm_client.delete_app(
            DomainId=domain_id,
            UserProfileName=user_profile,
            AppType='KernelGateway',
            AppName=app['AppName']
        )

print("Limpeza concluída!")
```

---

## 3. Parar Endpoints (Se Criados)

### O que são Endpoints?

Endpoints são modelos em produção que ficam ativos 24/7 esperando requisições.

**Custo exemplo:**
- ml.m5.large endpoint: $0.115/hora = $82.80/mês

### Listar e Deletar Endpoints

```bash
# Listar endpoints ativos
aws sagemaker list-endpoints \
  --region eu-central-1 \
  --status-equals InService

# Deletar endpoint específico
aws sagemaker delete-endpoint \
  --endpoint-name my-endpoint-name \
  --region eu-central-1

# Deletar também a configuração do endpoint
aws sagemaker delete-endpoint-config \
  --endpoint-config-name my-endpoint-config \
  --region eu-central-1

# Deletar o modelo
aws sagemaker delete-model \
  --model-name my-model-name \
  --region eu-central-1
```

### Via Python

```python
import boto3

sm_client = boto3.client('sagemaker')

# Listar endpoints
endpoints = sm_client.list_endpoints()['Endpoints']

for endpoint in endpoints:
    name = endpoint['EndpointName']
    print(f"Deletando endpoint: {name}")
    
    # Deletar endpoint
    sm_client.delete_endpoint(EndpointName=name)
    
    # Deletar config (opcional, mas recomendado)
    try:
        sm_client.delete_endpoint_config(EndpointConfigName=name)
    except:
        pass

print("Todos os endpoints deletados!")
```

---

## 4. Limpeza de Dados no S3

### Estratégia de Limpeza

**⚠️ CUIDADO:** S3 gera custo por armazenamento (~$0.023/GB-mês)

#### O que Manter?
- ✅ Dados brutos originais
- ✅ Modelos finais em produção
- ✅ Resultados importantes

#### O que Deletar?
- ❌ Dados temporários
- ❌ Experimentos intermediários
- ❌ Outputs de treinamento antigos
- ❌ Checkpoints de treino

### Limpeza Seletiva via CLI

```bash
# Listar tamanho do bucket
aws s3 ls s3://seu-bucket/ --recursive --human-readable --summarize

# Deletar pasta específica (ex: experimentos antigos)
aws s3 rm s3://seu-bucket/sagemaker-training/output/ --recursive

# Deletar arquivos antigos (>30 dias)
aws s3 ls s3://seu-bucket/ --recursive | \
  awk '{if ($1 < "2025-12-01") print $4}' | \
  xargs -I {} aws s3 rm s3://seu-bucket/{}

# Mover para Glacier (arquivamento barato)
aws s3 cp s3://seu-bucket/archive/ s3://seu-bucket/archive/ \
  --recursive \
  --storage-class GLACIER
```

### Lifecycle Policy (Automação)

```bash
# lifecycle-policy.json
cat > lifecycle-policy.json << 'EOF'
{
  "Rules": [
    {
      "Id": "MoveOldTrainingToGlacier",
      "Status": "Enabled",
      "Prefix": "sagemaker-training/output/",
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "Id": "DeleteTempFiles",
      "Status": "Enabled",
      "Prefix": "temp/",
      "Expiration": {
        "Days": 7
      }
    }
  ]
}
EOF

# Aplicar policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket seu-bucket \
  --lifecycle-configuration file://lifecycle-policy.json
```

### Via Python

```python
import boto3
from datetime import datetime, timedelta

s3 = boto3.resource('s3')
bucket = s3.Bucket('seu-bucket')

# Deletar objetos antigos (>30 dias)
cutoff_date = datetime.now() - timedelta(days=30)

deleted_count = 0
deleted_size = 0

for obj in bucket.objects.filter(Prefix='sagemaker-training/output/'):
    if obj.last_modified.replace(tzinfo=None) < cutoff_date:
        print(f"Deletando: {obj.key} ({obj.size / 1024 / 1024:.2f} MB)")
        deleted_size += obj.size
        obj.delete()
        deleted_count += 1

print(f"\nTotal deletado: {deleted_count} arquivos")
print(f"Espaço liberado: {deleted_size / 1024 / 1024:.2f} MB")
```

---

## 5. Deletar Domain e User Profiles (Opcional)

**⚠️ ATENÇÃO:** Só faça isso se não for mais usar o SageMaker!

### Ordem de Deleção

```bash
# 1. Deletar todas as apps (já feito anteriormente)

# 2. Deletar user profiles
aws sagemaker delete-user-profile \
  --domain-id d-xxxxxxxxxxxx \
  --user-profile-name default-user \
  --region eu-central-1

# Aguardar deleção
aws sagemaker describe-user-profile \
  --domain-id d-xxxxxxxxxxxx \
  --user-profile-name default-user \
  --region eu-central-1 2>&1 | grep "Could not find"

# 3. Deletar domain
aws sagemaker delete-domain \
  --domain-id d-xxxxxxxxxxxx \
  --retention-policy '{
    "HomeEfsFileSystem": "Delete"
  }' \
  --region eu-central-1

# Monitorar deleção (pode levar 10-15 min)
aws sagemaker describe-domain \
  --domain-id d-xxxxxxxxxxxx \
  --region eu-central-1
```

---

## 6. Deletar Stacks CloudFormation

```bash
# Listar stacks
aws cloudformation list-stacks \
  --region eu-central-1 \
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE

# Deletar stack do S3
aws cloudformation delete-stack \
  --stack-name sagemaker-s3-buckets \
  --region eu-central-1

# Deletar stack do SageMaker Domain
# (Só depois de deletar domain e user profiles manualmente)
aws cloudformation delete-stack \
  --stack-name sagemaker-training-stack \
  --region eu-central-1

# Monitorar deleção
aws cloudformation wait stack-delete-complete \
  --stack-name sagemaker-s3-buckets \
  --region eu-central-1
```

---

## 7. Boas Práticas de Segurança

### IAM - Princípio do Menor Privilégio

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateTrainingJob",
        "sagemaker:DescribeTrainingJob",
        "sagemaker:StopTrainingJob"
      ],
      "Resource": "arn:aws:sagemaker:*:*:training-job/meu-projeto-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::meu-bucket-projeto/*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "sagemaker:CreateEndpoint",
        "sagemaker:UpdateEndpoint"
      ],
      "Resource": "*"
    }
  ]
}
```

### Criptografia

```python
# Sempre use criptografia no S3
import boto3

s3_client = boto3.client('s3')

# Upload com criptografia
s3_client.put_object(
    Bucket='seu-bucket',
    Key='dados-sensiveis.csv',
    Body=data,
    ServerSideEncryption='AES256'  # ✅ Criptografado
)

# Treino com criptografia
from sagemaker.estimator import Estimator

estimator = Estimator(
    ...,
    encrypt_inter_container_traffic=True,  # ✅ Criptografia em trânsito
    output_kms_key='arn:aws:kms:...'      # ✅ Criptografia at-rest
)
```

### VPC e Isolamento

```python
# Treinar em VPC privada (sem internet)
estimator = Estimator(
    ...,
    subnets=['subnet-xxx', 'subnet-yyy'],
    security_group_ids=['sg-xxx'],
    enable_network_isolation=True  # ✅ Sem acesso à internet
)
```

### Não Comitar Credenciais

```bash
# ❌ NUNCA faça isso
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ✅ Use IAM roles e variáveis de ambiente
import boto3
session = boto3.Session()  # Usa credenciais do ambiente
```

---

## 8. Gerenciamento de Custos

### Configurar AWS Budgets

```bash
# budget.json
cat > budget.json << 'EOF'
{
  "BudgetName": "SageMaker-Monthly-Budget",
  "BudgetLimit": {
    "Amount": "50",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {
    "Service": ["Amazon SageMaker", "Amazon S3"]
  }
}
EOF

# notifications.json
cat > notifications.json << 'EOF'
[
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [
      {
        "SubscriptionType": "EMAIL",
        "Address": "seu-email@example.com"
      }
    ]
  }
]
EOF

# Criar budget
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

### Monitorar Custos

```bash
# Ver custos dos últimos 30 dias
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --filter file://<(echo '{
    "Dimensions": {
      "Key": "SERVICE",
      "Values": ["Amazon SageMaker"]
    }
  }')

# Por tipo de recurso
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '7 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=USAGE_TYPE \
  --filter file://<(echo '{
    "Dimensions": {
      "Key": "SERVICE",
      "Values": ["Amazon SageMaker"]
    }
  }')
```

### Tags para Rastreamento

```python
# Adicionar tags aos recursos
estimator = Estimator(
    ...,
    tags=[
        {'Key': 'Project', 'Value': 'california-housing'},
        {'Key': 'Team', 'Value': 'data-science'},
        {'Key': 'CostCenter', 'Value': 'ML-R&D'},
        {'Key': 'Environment', 'Value': 'training'}
    ]
)

# Depois, filtrar custos por tag
aws ce get-cost-and-usage \
  --time-period Start=2026-02-01,End=2026-02-28 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=TAG,Key=Project
```

---

## 9. Organização de Projetos ML

### Estrutura Recomendada

```
projeto-ml/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
│
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_data_preparation.ipynb
│   └── 03_model_training.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineering.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── predict.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── tests/
│   ├── test_preprocessing.py
│   └── test_models.py
│
├── configs/
│   ├── config.yaml
│   └── hyperparameters.yaml
│
├── cloudformation/
│   ├── infrastructure.yaml
│   └── parameters.json
│
└── docs/
    ├── architecture.md
    └── experiments.md
```

### .gitignore para ML

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
.env

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Data (NÃO comitar datasets grandes)
data/raw/
data/processed/
*.csv
*.parquet
*.h5
*.pkl

# Models (usar Git LFS ou S3)
models/*.pkl
models/*.h5
models/*.pt

# AWS
.aws/
*.pem

# Outputs
outputs/
logs/
```

### README Template

```markdown
# Projeto: California Housing Price Prediction

## Visão Geral
Modelo de predição de preços de imóveis na Califórnia usando XGBoost no Amazon SageMaker.

## Setup
```bash
# Criar ambiente
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Estrutura de Dados
- **Input**: S3://bucket/data/raw/
- **Output**: S3://bucket/models/

## Treinamento
```bash
python src/models/train.py --config configs/config.yaml
```

## Métricas
- RMSE: 0.634
- R²: 0.813

## Autores
- João Silva (joao@example.com)
```

---

## 10. Próximos Passos no Aprendizado

### Recursos AWS

#### Documentação Oficial
- [SageMaker Developer Guide](https://docs.aws.amazon.com/sagemaker/)
- [SageMaker Examples GitHub](https://github.com/aws/amazon-sagemaker-examples)
- [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/)

#### Treinamentos Gratuitos
- [AWS Skill Builder](https://skillbuilder.aws/)
  - "Getting Started with Amazon SageMaker"
  - "MLOps Engineering on AWS"
- [AWS Machine Learning University](https://aws.amazon.com/machine-learning/mlu/)

#### Certificações
- AWS Certified Machine Learning - Specialty
- AWS Certified Solutions Architect

### Tópicos Avançados

#### 1. MLOps com SageMaker
- SageMaker Pipelines (CI/CD para ML)
- Model Registry e versionamento
- Model Monitor (detectar drift)
- Feature Store

#### 2. Deployment
- Real-time endpoints
- Batch transform
- Multi-model endpoints
- Serverless inference

#### 3. Treinamento Avançado
- Distributed training
- Automatic model tuning
- SageMaker Debugger
- SageMaker Experiments

#### 4. Integrações
- Step Functions para orquestração
- Lambda para inference
- API Gateway para servir modelos
- EventBridge para automação

### Comunidade

- [AWS re:Post](https://repost.aws/)
- [Stack Overflow - amazon-sagemaker](https://stackoverflow.com/questions/tagged/amazon-sagemaker)
- Meetups locais de AWS e ML

---

## 11. Checklist Final

### Limpeza Imediata
- [ ] Parei todas as KernelGateway apps
- [ ] Deletei endpoints não utilizados
- [ ] Limpei dados temporários do S3

### Após o Treinamento
- [ ] Deletei user profiles (se aplicável)
- [ ] Deletei SageMaker Domain (se aplicável)
- [ ] Deletei stacks CloudFormation
- [ ] Deletei buckets S3 não necessários

### Segurança
- [ ] Revisei permissões IAM
- [ ] Habilitei criptografia
- [ ] Não comitei credenciais no Git
- [ ] Configurei MFA na conta AWS

### Custos
- [ ] Configurei AWS Budgets
- [ ] Adicionei tags aos recursos
- [ ] Revisei billing dashboard
- [ ] Configurei alertas de custo

### Organização
- [ ] Documentei o projeto
- [ ] Salvei código em repositório Git
- [ ] Salvei modelos importantes no S3
- [ ] Criei README e documentação

---

## 12. Recursos Adicionais

### Ferramentas Úteis

**AWS CLI - Comandos Úteis:**
```bash
# Ver todos os recursos SageMaker ativos
aws sagemaker list-training-jobs --region eu-central-1
aws sagemaker list-endpoints --region eu-central-1
aws sagemaker list-notebook-instances --region eu-central-1

# Ver custos estimados
aws ce get-cost-forecast \
  --time-period Start=$(date +%Y-%m-%d),End=$(date -d '+30 days' +%Y-%m-%d) \
  --metric UNBLENDED_COST \
  --granularity MONTHLY \
  --filter file://<(echo '{"Dimensions":{"Key":"SERVICE","Values":["Amazon SageMaker"]}}')
```

**Python - Script de Limpeza Completo:**

Consulte [snippets.md](../codigo-exemplo/snippets.md) para script completo de limpeza.

---

## Conclusão

Parabéns por concluir o treinamento AWS SageMaker! 🎉

Você agora sabe:
- ✅ Acessar e configurar AWS
- ✅ Criar infraestrutura com IaC
- ✅ Usar SageMaker Studio
- ✅ Gerenciar dados no S3
- ✅ Treinar modelos (local e gerenciado)
- ✅ Usar algoritmos built-in
- ✅ Limpar recursos adequadamente
- ✅ Aplicar boas práticas

**Continue aprendendo e construindo projetos incríveis!** 🚀

---

**Dúvidas ou feedback?** Entre em contato com os instrutores.
