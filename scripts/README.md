# Scripts de Infraestrutura - SageMaker Training

Este diretório contém templates CloudFormation para provisionar a infraestrutura necessária para o treinamento AWS SageMaker.

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `sagemaker-complete-infrastructure.yaml` | Template completo (VPC + SageMaker + IAM) |
| `parameters.json` | Parâmetros de exemplo para o template |

## Recursos Criados

O template `sagemaker-complete-infrastructure.yaml` cria:

### Networking (VPC)
- VPC com DNS habilitado
- 2 Subnets Públicas (em AZs diferentes)
- 2 Subnets Privadas (em AZs diferentes)
- Internet Gateway
- NAT Gateway (para subnets privadas)
- Route Tables (pública e privada)

### SageMaker
- SageMaker Domain
- User Profile
- Security Group dedicado
- IAM Execution Role com permissões para:
  - SageMaker Full Access
  - S3 Access
  - ECR Access
  - CloudWatch Logs
  - KMS

### IAM
- Grupo de usuários SageMaker
- Usuário IAM com:
  - Acesso ao console (senha temporária)
  - Permissões para SageMaker e S3
  - (Opcional) Access Key para CLI

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                              VPC (10.0.0.0/16)                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                     Internet Gateway                            ││
│  └─────────────────────────────────────────────────────────────────┘│
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────┐          │
│  │        Public Subnets     │                           │          │
│  │  ┌───────────────┐  ┌─────┴─────┐  ┌───────────────┐ │          │
│  │  │ Subnet 1      │  │ NAT GW    │  │ Subnet 2      │ │          │
│  │  │ 10.0.1.0/24   │  │           │  │ 10.0.2.0/24   │ │          │
│  │  │ (AZ-a)        │  │           │  │ (AZ-b)        │ │          │
│  │  └───────────────┘  └─────┬─────┘  └───────────────┘ │          │
│  └───────────────────────────┼───────────────────────────┘          │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────┐          │
│  │        Private Subnets    │                           │          │
│  │  ┌───────────────┐        │        ┌───────────────┐ │          │
│  │  │ Subnet 1      │◄───────┘        │ Subnet 2      │ │          │
│  │  │ 10.0.10.0/24  │                 │ 10.0.20.0/24  │ │          │
│  │  │ (AZ-a)        │                 │ (AZ-b)        │ │          │
│  │  │               │                 │               │ │          │
│  │  │ ┌───────────┐ │                 │ ┌───────────┐ │ │          │
│  │  │ │ SageMaker │ │                 │ │ SageMaker │ │ │          │
│  │  │ │ Studio    │ │                 │ │ Studio    │ │ │          │
│  │  │ └───────────┘ │                 │ └───────────┘ │ │          │
│  │  └───────────────┘                 └───────────────┘ │          │
│  └───────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

## Deploy

### Pré-requisitos

1. AWS CLI instalado e configurado
2. Permissões para criar recursos (VPC, IAM, SageMaker)
3. Conta AWS ativa

### Via AWS CLI

```bash
# Navegar para o diretório scripts
cd scripts

# Validar o template
aws cloudformation validate-template \
  --template-body file://sagemaker-complete-infrastructure.yaml \
  --region eu-central-1

# Criar a stack
aws cloudformation create-stack \
  --stack-name sagemaker-training-infrastructure \
  --template-body file://sagemaker-complete-infrastructure.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-central-1

# Monitorar criação
aws cloudformation describe-stacks \
  --stack-name sagemaker-training-infrastructure \
  --region eu-central-1 \
  --query 'Stacks[0].StackStatus'

# Ver eventos em tempo real
aws cloudformation describe-stack-events \
  --stack-name sagemaker-training-infrastructure \
  --region eu-central-1 \
  --max-items 10

# Aguardar conclusão (opcional)
aws cloudformation wait stack-create-complete \
  --stack-name sagemaker-training-infrastructure \
  --region eu-central-1

# Obter outputs após criação
aws cloudformation describe-stacks \
  --stack-name sagemaker-training-infrastructure \
  --region eu-central-1 \
  --query 'Stacks[0].Outputs'
```

### Via Console AWS

1. Acesse **CloudFormation** no console AWS
2. Clique em **Create stack** → **With new resources**
3. Selecione **Upload a template file**
4. Faça upload do arquivo `sagemaker-complete-infrastructure.yaml`
5. Preencha os parâmetros conforme necessário
6. Marque **"I acknowledge that AWS CloudFormation might create IAM resources"**
7. Clique em **Create stack**

## Parâmetros

| Parâmetro | Descrição | Valor Padrão |
|-----------|-----------|--------------|
| `ProjectName` | Nome do projeto (prefixo) | `sagemaker-training` |
| `EnvironmentName` | Ambiente (dev/training/staging/prod) | `dev` |
| `VpcCIDR` | CIDR da VPC | `10.0.0.0/16` |
| `SageMakerDomainName` | Nome do SageMaker Domain | `sagemaker-studio-domain` |
| `IAMUserName` | Nome do usuário IAM | `sagemaker-user` |
| `CreateIAMUserAccessKey` | Criar access key? | `false` |
| `SageMakerUserProfileName` | Nome do User Profile | `default-user` |

## Outputs

Após o deploy, os seguintes outputs estarão disponíveis:

| Output | Descrição |
|--------|-----------|
| `VPCId` | ID da VPC criada |
| `SageMakerDomainId` | ID do SageMaker Domain |
| `SageMakerDomainUrl` | URL do SageMaker Domain |
| `IAMUserName` | Nome do usuário IAM |
| `IAMUserLoginUrl` | URL para login no console |
| `IAMUserInitialPassword` | Senha temporária (DEVE SER ALTERADA) |

## Pós-Deploy

### 1. Login do Usuário IAM

```
URL: https://[ACCOUNT-ID].signin.aws.amazon.com/console
Usuário: sagemaker-training-user
Senha: [Ver output IAMUserInitialPassword]
```

A senha temporária deve ser alterada no primeiro login.

### 2. Acessar SageMaker Studio

1. Faça login com o usuário IAM criado
2. Navegue até **SageMaker** → **Domains**
3. Selecione o domain criado
4. Clique no user profile
5. Clique em **Launch** → **Studio**

### 3. Verificar Recursos

```bash
# Verificar VPC
aws ec2 describe-vpcs \
  --filters "Name=tag:Project,Values=sagemaker-training" \
  --region eu-central-1

# Verificar SageMaker Domain
aws sagemaker list-domains --region eu-central-1

# Verificar User Profiles
aws sagemaker list-user-profiles \
  --domain-id-equals [DOMAIN-ID] \
  --region eu-central-1

# Verificar usuário IAM
aws iam get-user --user-name sagemaker-training-user
```

## Limpeza

Para deletar todos os recursos criados:

```bash
# ATENÇÃO: Primeiro delete manualmente Apps e recursos no SageMaker Studio

# Deletar a stack
aws cloudformation delete-stack \
  --stack-name sagemaker-training-infrastructure \
  --region eu-central-1

# Aguardar deleção
aws cloudformation wait stack-delete-complete \
  --stack-name sagemaker-training-infrastructure \
  --region eu-central-1
```

**IMPORTANTE:** Antes de deletar a stack:
1. Pare todas as apps no SageMaker Studio
2. Delete os user profiles manualmente se necessário
3. Limpe dados do EFS se aplicável

## Custos Estimados

| Recurso | Custo Aproximado (eu-central-1) |
|---------|--------------------------------|
| NAT Gateway | ~$0.048/hora + $0.048/GB |
| VPC | Sem custo direto |
| SageMaker Domain | Sem custo (paga por uso) |
| IAM User | Sem custo |
| **Total Base** | ~$35/mês (NAT Gateway apenas) |

**Nota:** Custos adicionais são gerados ao usar instâncias no SageMaker Studio.

## Troubleshooting

### Erro: "Resource limit exceeded"

Pode ser limite de VPCs ou IPs elásticos na região.

**Solução:** Delete VPCs não utilizadas ou solicite aumento de limite.

### Erro: "IAM Role already exists"

Role com mesmo nome já existe.

**Solução:** Use nome diferente em `ProjectName` ou delete role existente.

### Erro: "Domain creation failed"

Geralmente problema de rede ou permissões.

**Solução:**
1. Verifique se NAT Gateway está funcionando
2. Verifique permissões da role
3. Consulte CloudWatch Logs

### Stack travada em DELETE_IN_PROGRESS

Pode haver recursos que impedem deleção.

**Solução:**
1. Delete apps SageMaker manualmente
2. Delete user profiles manualmente
3. Delete domain manualmente
4. Tente deletar stack novamente

## Suporte

Para dúvidas ou problemas, consulte:
- [Documentação AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
- [Documentação SageMaker](https://docs.aws.amazon.com/sagemaker/)
- Instrutores do treinamento

---

**Versão:** 1.0  
**Última atualização:** Fevereiro 2026
