# Scripts de Infraestrutura - SageMaker Training

Este diretório contém templates CloudFormation para provisionar a infraestrutura necessária para o treinamento AWS SageMaker.

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `sagemaker-complete-infrastructure.yaml` | Template completo (VPC + SageMaker + IAM) |
| `parameters.json` | Parâmetros de exemplo para o template |
| `no-shows.csv` | Dataset de exemplo para o Módulo 6 |
| `exemplo-treinamento.ipynb` | Notebook com exemplos de EDA e XGBoost (local) |
| `exemplo-treinamento-sagemaker.ipynb` | Notebook com XGBoost via SageMaker Training Job |
| `cap2_EDA_univariada.py` | Script Python - EDA univariada |
| `cap9_XGBoost_Boston_regressão.py` | Script Python - XGBoost regressão |

---

## Dataset de Exemplo

O arquivo `no-shows.csv` contém dados de agendamentos médicos para uso no **Módulo 6: Upload de Datasets**.

### Descrição

Dataset "Medical Appointment No Shows" - registros de consultas médicas onde o objetivo é prever se o paciente comparecerá ou não à consulta agendada.

- **Fonte:** [Kaggle - Medical Appointment No Shows](https://www.kaggle.com/datasets/joniarroba/noshowappointments)
- **Registros:** ~110.000 agendamentos
- **Período:** 2016
- **Problema:** Classificação binária (compareceu / não compareceu)

### Colunas

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `PatientId` | int | Identificador único do paciente |
| `AppointmentID` | int | Identificador único do agendamento |
| `Gender` | string | Gênero do paciente (M/F) |
| `ScheduledDay` | datetime | Data/hora em que o agendamento foi feito |
| `AppointmentDay` | datetime | Data da consulta agendada |
| `Age` | int | Idade do paciente |
| `Neighbourhood` | string | Bairro do paciente |
| `Scholarship` | int | Beneficiário do Bolsa Família (0/1) |
| `Hipertension` | int | Paciente com hipertensão (0/1) |
| `Diabetes` | int | Paciente com diabetes (0/1) |
| `Alcoholism` | int | Paciente com alcoolismo (0/1) |
| `Handcap` | int | Paciente com deficiência (0/1) |
| `SMS_received` | int | Recebeu SMS de lembrete (0/1) |
| `No-show` | string | **Target:** "Yes" = não compareceu, "No" = compareceu |

### Uso no Treinamento

Este dataset será utilizado para:
1. **Módulo 6:** Upload para S3 e acesso via SageMaker
2. **Módulo 7:** Análise exploratória e preparação de dados
3. **Módulo 8:** Treinamento com algoritmos built-in (XGBoost/Linear Learner)

### Exemplo de Carregamento

```python
import pandas as pd

# Carregar do arquivo local
df = pd.read_csv('no-shows.csv')

# Ou do S3 após upload
df = pd.read_csv('s3://seu-bucket/data/no-shows.csv')

# Visualizar primeiras linhas
df.head()

# Info básica
print(f"Registros: {len(df)}")
print(f"Colunas: {df.columns.tolist()}")
print(f"Taxa de No-show: {df['No-show'].value_counts(normalize=True)}")
```

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

### Via Console AWS (Passo a Passo Detalhado)

#### Passo 1: Acessar o CloudFormation

1. Faça login na sua conta AWS: https://console.aws.amazon.com
2. Verifique se está na região correta: **EU (Frankfurt) eu-central-1**
3. Na barra de pesquisa superior, digite **CloudFormation**
4. Clique no serviço **CloudFormation** nos resultados

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 CloudFormation                                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ CloudFormation                                          ││
│  │ Create and manage resources with templates              ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

#### Passo 2: Criar Nova Stack

1. Na página do CloudFormation, clique no botão **Create stack**
2. No menu suspenso, selecione **With new resources (standard)**

```
┌─────────────────────────────────────────────────────────────┐
│  CloudFormation > Stacks                                    │
│                                                             │
│  [ Create stack ▼ ]                                         │
│    ├─ With new resources (standard)  ◄── Selecione este    │
│    ├─ With existing resources (import resources)            │
│    └─ ...                                                   │
└─────────────────────────────────────────────────────────────┘
```

#### Passo 3: Fazer Upload do Template

Na tela **"Create stack"**, seção **"Prerequisite - Prepare template"**:

1. Selecione: **Choose an existing template**
2. Em **"Specify template"**, selecione: **Upload a template file**
3. Clique no botão **Choose file**
4. Navegue até a pasta `scripts/` e selecione o arquivo `sagemaker-complete-infrastructure.yaml`
5. Aguarde o upload completar (aparecerá "S3 URL" preenchida automaticamente)
6. Clique em **Next**

```
┌─────────────────────────────────────────────────────────────┐
│  Create stack                                               │
│                                                             │
│  Prerequisite - Prepare template                            │
│  ○ Use a sample template                                    │
│  ○ Create template in Designer                              │
│  ● Choose an existing template  ◄── Selecione              │
│                                                             │
│  Specify template                                           │
│  ○ Amazon S3 URL                                            │
│  ● Upload a template file  ◄── Selecione                   │
│                                                             │
│  [ Choose file ]  sagemaker-complete-infrastructure.yaml    │
│                                                             │
│  S3 URL: https://s3.amazonaws.com/cf-templates-xxx/...     │
│                                                             │
│                                           [ Next ]          │
└─────────────────────────────────────────────────────────────┘
```

#### Passo 4: Configurar Nome e Parâmetros da Stack

**Stack name:**
- Digite um nome único para sua stack, exemplo: `deploy-sagemaker`

**Parameters:**
Revise e ajuste os parâmetros conforme necessário:

| Parâmetro | Descrição | Valor Sugerido |
|-----------|-----------|----------------|
| ProjectName | Prefixo para recursos | `sagemaker-training` |
| EnvironmentName | Ambiente | `training` |
| VpcCIDR | CIDR da VPC | `10.0.0.0/16` (manter padrão) |
| SageMakerDomainName | Nome do Domain | `sagemaker-studio-domain` |
| IAMUserName | Nome do usuário IAM | `sagemaker-user` |
| CreateIAMUserAccessKey | Criar access key | `false` |
| SageMakerUserProfileName | Nome do User Profile | `default-user` |

Clique em **Next** após configurar.

```
┌─────────────────────────────────────────────────────────────┐
│  Specify stack details                                      │
│                                                             │
│  Stack name *                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ deploy-sagemaker                                        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  Parameters                                                 │
│  ─────────────────────────────────────────────────────────  │
│  1. Configuracoes Gerais                                    │
│                                                             │
│  ProjectName *              [ sagemaker-training    ]       │
│  EnvironmentName *          [ training          ▼ ]        │
│                                                             │
│  2. Configuracoes de Rede (VPC)                            │
│                                                             │
│  VpcCIDR *                  [ 10.0.0.0/16          ]       │
│  ...                                                        │
│                                                             │
│                                           [ Next ]          │
└─────────────────────────────────────────────────────────────┘
```

#### Passo 5: Configurar Opções da Stack (Opcional)

Na tela **"Configure stack options"**:

**Tags (opcional mas recomendado):**
- Key: `Owner`, Value: `[Seu Nome]`
- Key: `Purpose`, Value: `Training`

**Permissions:**
- **IAM role - optional**: Deixe em branco (usará suas credenciais)

**Stack failure options:**
- Mantenha: `Roll back all stack resources`

**Advanced options:**
- Mantenha os valores padrão

Clique em **Next**.

```
┌─────────────────────────────────────────────────────────────┐
│  Configure stack options                                    │
│                                                             │
│  Tags (optional)                                            │
│  ┌───────────────────┬───────────────────┐                 │
│  │ Key               │ Value             │                 │
│  ├───────────────────┼───────────────────┤                 │
│  │ Owner             │ Seu Nome          │                 │
│  │ Purpose           │ Training          │                 │
│  └───────────────────┴───────────────────┘                 │
│                                                             │
│  Permissions                                                │
│  IAM role - optional                                        │
│  [ Deixe em branco                              ▼ ]        │
│                                                             │
│                                           [ Next ]          │
└─────────────────────────────────────────────────────────────┘
```

#### Passo 6: Revisar e Criar

Na tela **"Review and create"**:

1. **Revise** todas as configurações (Stack name, Parameters, Tags)

2. **IMPORTANTE - Capabilities:**
   
   Role até a seção **"Capabilities"** no final da página.
   
   Você verá uma mensagem sobre recursos IAM:
   
   ```
   ┌─────────────────────────────────────────────────────────────┐
   │  Capabilities                                               │
   │                                                             │
   │  The following resource(s) require capabilities:            │
   │  [AWS::IAM::Policy, AWS::IAM::Role, AWS::IAM::User,        │
   │   AWS::IAM::Group]                                          │
   │                                                             │
   │  ⚠️  This template contains Identity and Access Management │
   │  (IAM) resources. Check that you want to create each of    │
   │  these resources and that they have the minimum required   │
   │  permissions. In addition, they have custom names. Check   │
   │  that the custom names are unique within your AWS account. │
   │                                                             │
   │  ☑️  I acknowledge that AWS CloudFormation might create    │
   │      IAM resources with custom names.  ◄── MARQUE ESTE     │
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
   ```
   
   **Marque o checkbox** para aceitar a criação de recursos IAM.

3. Clique em **Submit** para iniciar a criação.

#### Passo 7: Acompanhar a Criação

Após clicar em Submit, você será redirecionado para a página da stack.

1. Observe o status: `CREATE_IN_PROGRESS`
2. Clique na aba **Events** para ver o progresso em tempo real
3. Aguarde até o status mudar para: `CREATE_COMPLETE`

```
┌─────────────────────────────────────────────────────────────┐
│  Stack: deploy-sagemaker                                    │
│  Status: CREATE_IN_PROGRESS → CREATE_COMPLETE              │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Tabs: [ Stack info ] [ Events ] [ Resources ] [Outputs]││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  Events:                                                    │
│  ────────────────────────────────────────────────────────── │
│  Timestamp          Resource              Status            │
│  10:30:00           VPC                   CREATE_COMPLETE   │
│  10:30:30           InternetGateway       CREATE_COMPLETE   │
│  10:31:00           PublicSubnet1         CREATE_COMPLETE   │
│  10:32:00           NatGateway            CREATE_IN_PROGRESS│
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

**Tempo estimado:** 10-15 minutos

#### Passo 8: Obter Informações de Acesso

Após `CREATE_COMPLETE`:

1. Clique na aba **Outputs**
2. Anote os valores importantes:

| Output | Descrição | Exemplo |
|--------|-----------|---------|
| `IAMUserLoginUrl` | URL para login | `https://123456789012.signin.aws.amazon.com/console` |
| `IAMUserName` | Usuário criado | `sagemaker-user` |
| `IAMUserInitialPassword` | Senha temporária | `sagemaker-trainingTemp123!` |
| `SageMakerDomainUrl` | URL do Studio | `https://d-xxx.studio.eu-central-1.sagemaker.aws` |

```
┌─────────────────────────────────────────────────────────────┐
│  Outputs                                                    │
│                                                             │
│  Key                        Value                           │
│  ───────────────────────────────────────────────────────── │
│  IAMUserLoginUrl            https://123456789012.signin...  │
│  IAMUserName                sagemaker-user                  │
│  IAMUserInitialPassword     sagemaker-trainingTemp123!      │
│  SageMakerDomainId          d-xxxxxxxxxxxx                  │
│  SageMakerDomainUrl         https://d-xxx.studio.eu-ce...   │
│  VPCId                      vpc-xxxxxxxxxxxx                │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

#### Resumo Visual do Processo

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Login   │───▶│  Cloud   │───▶│  Upload  │───▶│  Config  │
│  AWS     │    │Formation │    │ Template │    │  Params  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                     │
┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  Done!   │◀───│  Wait    │◀───│  Accept  │◀───────┘
│  Outputs │    │ ~15 min  │    │   IAM    │
└──────────┘    └──────────┘    └──────────┘
```

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

> **Nota:** Ao executar a stack com sucesso, o **usuário IAM** e o **User Profile do SageMaker** já foram criados automaticamente. Não é necessário criar manualmente - basta acessar o SageMaker Studio conforme os passos abaixo.

---

### 1. Acessar o SageMaker AI

Após o deploy da stack estar completo (`CREATE_COMPLETE`):

**Passo 1:** Na barra de pesquisa do console AWS, digite **SageMaker AI** e clique no serviço

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 SageMaker AI                                            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Amazon SageMaker AI                                     ││ ◀─ Clique
│  │ Build, train, and deploy machine learning models        ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Passo 2:** No menu lateral esquerdo, clique em **Domains**

```
┌─────────────────────────────────────────────────────────────┐
│  Amazon SageMaker                                           │
│                                                             │
│  ◀ Menu lateral                                             │
│  ─────────────────                                          │
│  Home                                                       │
│  Getting started                                            │
│  ─────────────────                                          │
│  Admin configurations                                       │
│    ▶ Domains  ◀─── Clique aqui                             │
│    ▶ Shared spaces                                          │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

**Passo 3:** Clique no **nome do Domain** criado (ex: `sagemaker-studio-domain`)

```
┌─────────────────────────────────────────────────────────────┐
│  Amazon SageMaker > Domains                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Domain name              Status        Created          ││
│  ├─────────────────────────────────────────────────────────┤│
│  │ sagemaker-studio-domain  InService     2026-02-05       ││ ◀─ Clique no nome
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Passo 4:** Na página do Domain, clique na aba **User profiles** (parte superior)

**Passo 5:** Localize o usuário criado (ex: `default-user`) e clique em **Open Studio**

```
┌─────────────────────────────────────────────────────────────┐
│  Domain: sagemaker-studio-domain                            │
│                                                             │
│  [ Domain details ] [ User profiles ] [ Shared spaces ]     │
│                      ▲                                      │
│                      └─── Clique aqui                       │
│                                                             │
│  User profiles:                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Name           Status     Actions                       ││
│  ├─────────────────────────────────────────────────────────┤│
│  │ default-user   InService  [ Open Studio ]  ◀─ Clique   ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Passo 6:** Aguarde o SageMaker Studio carregar (primeira vez pode levar 2-3 minutos)

---

### 2. Criar Instância JupyterLab

Após acessar o SageMaker Studio, você precisa criar um **JupyterLab Space** para executar notebooks:

**Passo 1:** No menu lateral do Studio, clique em **JupyterLab**

```
┌─────────────────────────────────────────────────────────────┐
│  SageMaker Studio                           [default-user] │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│  Home    │                                                  │
│  ─────── │                                                  │
│  ▶ JupyterLab  ◀─── Clique aqui                            │
│  ▶ Code Editor │                                           │
│  ▶ Data        │                                           │
│  ...           │                                           │
│          │                                                  │
└──────────┴──────────────────────────────────────────────────┘
```

**Passo 2:** Clique no botão **Create JupyterLab space**

```
┌─────────────────────────────────────────────────────────────┐
│  JupyterLab                                                 │
│                                                             │
│  [ Create JupyterLab space ]  ◀─── Clique aqui             │
│                                                             │
│  Your JupyterLab spaces:                                    │
│  (nenhum space criado ainda)                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Passo 3:** Configure o JupyterLab Space:

| Campo | Valor |
|-------|-------|
| **Name** | Digite um nome (ex: `jupyter-treinamento`) |
| **Sharing** | Selecione **Private** |

Clique em **Create space**

```
┌─────────────────────────────────────────────────────────────┐
│  Create JupyterLab space                                    │
│                                                             │
│  Name *                                                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ jupyter-treinamento                                     ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  Sharing                                                    │
│  ○ Shared                                                   │
│  ● Private  ◀─── Selecione                                 │
│                                                             │
│                              [ Cancel ] [ Create space ]    │
└─────────────────────────────────────────────────────────────┘
```

**Passo 4:** Selecione o tipo de instância e inicie:

| Campo | Valor Recomendado |
|-------|-------------------|
| **Instance** | `ml.t3.medium` (2 vCPU, 4 GB RAM) |
| **Image** | Manter padrão (SageMaker Distribution) |
| **Storage** | Manter padrão (5 GB) |

Clique em **Run space**

```
┌─────────────────────────────────────────────────────────────┐
│  JupyterLab space: jupyter-treinamento                      │
│                                                             │
│  Instance                                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ml.t3.medium  ▼                                         ││ ◀─ Selecione
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  Image                                                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ SageMaker Distribution 2.0 (recommended)                ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│                                         [ Run space ]       │
└─────────────────────────────────────────────────────────────┘
```

**Passo 5:** Aguarde a instância iniciar

- Status mudará de `Starting` para `Running`
- Tempo estimado: **3-5 minutos**

```
┌─────────────────────────────────────────────────────────────┐
│  JupyterLab space: jupyter-treinamento                      │
│                                                             │
│  Status: Starting...  ████████░░░░░░░░░░░░  40%            │
│                                                             │
│  Instance: ml.t3.medium                                     │
│  Image: SageMaker Distribution 2.0                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Passo 6:** Quando o status mudar para `Running`, clique em **Open**

```
┌─────────────────────────────────────────────────────────────┐
│  JupyterLab space: jupyter-treinamento                      │
│                                                             │
│  Status: Running  ✓                                         │
│                                                             │
│  Instance: ml.t3.medium                                     │
│  Image: SageMaker Distribution 2.0                          │
│                                                             │
│                              [ Stop ] [ Open ]  ◀─ Clique  │
└─────────────────────────────────────────────────────────────┘
```

**Passo 7:** O JupyterLab será aberto em uma nova aba

```
┌─────────────────────────────────────────────────────────────┐
│  JupyterLab                                                 │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│  📁 Files │    Launcher                                     │
│          │    ─────────────────────────────────────────────│
│  /home/  │    Notebook          Console         Other      │
│  sagemaker│    ┌─────────┐      ┌─────────┐    ┌─────────┐ │
│          │    │ Python 3│      │ Python 3│    │Terminal │ │
│          │    └─────────┘      └─────────┘    └─────────┘ │
│          │                                                  │
│          │    [+ Create new notebook]                       │
└──────────┴──────────────────────────────────────────────────┘
```

Agora você pode criar notebooks e executar código Python!

---

### 3. Resumo do Fluxo Completo

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Deploy     │    │  SageMaker   │    │   Domains    │    │    User      │
│   Stack      │───▶│     AI       │───▶│   (menu)     │───▶│  Profiles    │
│  (15 min)    │    │  (pesquisa)  │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                   │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│   Pronto!    │    │    Open      │    │   Create     │           │
│   Notebook   │◀───│  JupyterLab  │◀───│   Space      │◀──────────┘
│   Running    │    │   (Run)      │    │  (Private)   │     Open Studio
└──────────────┘    └──────────────┘    └──────────────┘
```

---

### 4. Login do Usuário IAM (Opcional)

Se você precisa acessar com o usuário IAM criado pela stack (ao invés do usuário administrador):

1. **Abra uma janela anônima** do navegador

2. **Acesse a URL de login:**
   ```
   https://[ACCOUNT-ID].signin.aws.amazon.com/console
   ```
   (Veja o output `IAMUserLoginUrl` da stack)

3. **Credenciais:**
   - **IAM user name:** `sagemaker-user` (ou o nome configurado)
   - **Password:** `sagemaker-trainingTemp123!` (senha temporária)

4. **Altere a senha** no primeiro login (obrigatório)

---

### 6. Verificar Recursos Criados (Opcional)

**Via Console AWS:**

| Serviço | Navegação | O que procurar |
|---------|-----------|----------------|
| **VPC** | VPC → Your VPCs | `sagemaker-training-vpc` |
| **Subnets** | VPC → Subnets | 4 subnets com prefixo `sagemaker-training` |
| **SageMaker** | SageMaker → Domains | Domain com status `InService` |
| **IAM** | IAM → Users | `sagemaker-user` |

**Via AWS CLI:**

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
aws iam get-user --user-name sagemaker-user
```

### 7. Checklist de Validação

Confirme que conseguiu completar todas as etapas:

- [ ] Stack criada com sucesso (`CREATE_COMPLETE`)
- [ ] VPC com 4 subnets (2 públicas + 2 privadas)
- [ ] SageMaker Domain com status `InService`
- [ ] Conseguiu acessar o SageMaker Studio
- [ ] JupyterLab Space criado e rodando
- [ ] Conseguiu abrir o JupyterLab

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
