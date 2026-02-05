# Glossário de Termos - AWS SageMaker

Guia de referência rápida para termos técnicos utilizados durante o treinamento.

---

## Índice Alfabético

[A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [G](#g) | [H](#h) | [I](#i) | [J](#j) | [K](#k) | [L](#l) | [M](#m) | [N](#n) | [O](#o) | [P](#p) | [R](#r) | [S](#s) | [T](#t) | [U](#u) | [V](#v) | [W](#w) | [X](#x)

---

## A

### Algorithm (Algoritmo)
Conjunto de regras e procedimentos matemáticos para resolver um problema ou realizar uma tarefa de Machine Learning.

### Amazon S3 (Simple Storage Service)
Serviço de armazenamento de objetos da AWS. Oferece durabilidade de 99.999999999% (11 noves) e escalabilidade ilimitada.

### Amazon SageMaker
Serviço gerenciado de Machine Learning da AWS que permite construir, treinar e implantar modelos de ML em escala.

### API (Application Programming Interface)
Interface que permite comunicação entre diferentes softwares. No SageMaker, usamos APIs via SDK Python (boto3) ou AWS CLI.

### App
Aplicação em execução no SageMaker Studio. Exemplos: JupyterServer, KernelGateway, Canvas.

### ARN (Amazon Resource Name)
Identificador único de recursos AWS. Formato: `arn:aws:service:region:account-id:resource-type/resource-name`

### Auto Scaling
Capacidade de ajustar automaticamente recursos computacionais baseado na demanda.

### Availability Zone (AZ)
Datacenter isolado dentro de uma região AWS. Cada região tem múltiplas AZs para alta disponibilidade.

### AWS (Amazon Web Services)
Plataforma de computação em nuvem da Amazon, oferecendo mais de 200 serviços.

### AWS CLI (Command Line Interface)
Ferramenta de linha de comando para interagir com serviços AWS.

---

## B

### Batch Transform
Modo de inferência para processar grandes volumes de dados de uma vez, sem manter endpoint ativo.

### Bias
Viés ou erro sistemático em modelos de ML. Pode ser estatístico (underfitting) ou social (discriminação).

### BlazingText
Algoritmo built-in do SageMaker para processamento de texto, word embeddings e classificação de texto.

### Boto3
SDK oficial da AWS para Python. Permite interagir programaticamente com serviços AWS.

### Bucket
Container de armazenamento no Amazon S3. Nome deve ser único globalmente.

### Built-in Algorithm
Algoritmo otimizado e pré-construído pelo SageMaker (ex: XGBoost, Linear Learner).

---

## C

### Classification (Classificação)
Tipo de problema de ML supervisionado onde prevemos categorias discretas (ex: spam/não-spam).

### CloudFormation
Serviço de Infrastructure as Code (IaC) da AWS. Define recursos em templates YAML/JSON.

### CloudTrail
Serviço de auditoria que registra todas as ações realizadas na conta AWS.

### CloudWatch
Serviço de monitoramento e observabilidade da AWS. Coleta logs e métricas.

### Cluster
Grupo de recursos computacionais trabalhando juntos. Ex: cluster de treinamento distribuído.

### Container
Unidade padronizada de software que empacota código e dependências. SageMaker usa Docker containers.

### CORS (Cross-Origin Resource Sharing)
Mecanismo de segurança que permite requisições entre diferentes domínios.

### CPU (Central Processing Unit)
Processador principal do computador. Usado para tarefas de computação geral.

### Cross-Validation
Técnica de avaliação de modelos dividindo dados em múltiplos folds para treino/teste.

---

## D

### Data Drift
Mudança na distribuição dos dados de entrada ao longo do tempo, afetando performance do modelo.

### Data Wrangler
Ferramenta visual do SageMaker para preparação e transformação de dados.

### Dataset
Conjunto de dados usado para treinar ou avaliar modelos de ML.

### Deep Learning
Subcampo de ML usando redes neurais artificiais com múltiplas camadas.

### Deploy (Deployment)
Processo de colocar um modelo treinado em produção para fazer predições.

### Docker
Plataforma para desenvolver, distribuir e executar aplicações em containers.

### Domain (SageMaker Domain)
Ambiente centralizado do SageMaker que agrupa user profiles, apps e recursos compartilhados.

---

## E

### EBS (Elastic Block Store)
Serviço de armazenamento de blocos para instâncias EC2. Funciona como um "disco rígido virtual".

### EC2 (Elastic Compute Cloud)
Serviço de computação que fornece servidores virtuais (instâncias) na AWS.

### ECR (Elastic Container Registry)
Registro de imagens Docker da AWS. Armazena containers customizados.

### EDA (Exploratory Data Analysis)
Análise exploratória de dados para entender características, padrões e anomalias.

### EFS (Elastic File System)
Sistema de arquivos NFS gerenciado pela AWS. Usado pelo SageMaker Studio para armazenar notebooks.

### Endpoint
Serviço hospedado que fornece predições em tempo real. Fica ativo 24/7 aguardando requisições.

### Ensemble Learning
Técnica que combina múltiplos modelos para melhorar performance. Ex: Random Forest, XGBoost.

### Epoch
Uma passagem completa por todo o dataset de treinamento.

### Estimator
Classe do SageMaker SDK que encapsula configuração e execução de treinamento.

### ETL (Extract, Transform, Load)
Processo de extrair dados de fontes, transformá-los e carregá-los em destino.

---

## F

### Feature
Variável de entrada (coluna) usada para treinar modelo de ML. Sinônimo: variável independente.

### Feature Engineering
Processo de criar, transformar e selecionar features para melhorar modelos.

### Feature Store
Repositório centralizado de features para ML, com controle de versão.

### Fine-tuning
Ajuste de modelo pré-treinado para tarefa específica.

### Framework
Biblioteca de software para desenvolvimento. Ex: TensorFlow, PyTorch, scikit-learn.

---

## G

### GPU (Graphics Processing Unit)
Processador especializado para computação paralela. Essencial para deep learning.

### Ground Truth
Serviço do SageMaker para rotulação de dados (data labeling).

---

## H

### Hyperparameter
Parâmetro configurável do algoritmo que não é aprendido dos dados. Ex: learning rate, max_depth.

### Hyperparameter Tuning (HPO)
Processo automatizado de busca pelos melhores hiperparâmetros. Também chamado de Automatic Model Tuning.

---

## I

### IaC (Infrastructure as Code)
Prática de gerenciar infraestrutura através de código versionável. Ex: CloudFormation, Terraform.

### IAM (Identity and Access Management)
Serviço de gerenciamento de identidades e permissões da AWS.

### IAM Role
Identidade AWS com políticas de permissão. Usada por serviços para acessar recursos.

### Image (Imagem Docker)
Template imutável contendo código, runtime, bibliotecas e dependências.

### Inference
Processo de usar modelo treinado para fazer predições em novos dados.

### Instance
Servidor virtual com recursos computacionais dedicados (vCPU, RAM, disco).

### Instance Type
Categoria de instância definindo recursos. Ex: ml.t3.medium, ml.p3.2xlarge.

---

## J

### Jupyter Notebook
Ambiente interativo para código, visualizações e texto. Extensão `.ipynb`.

### JupyterLab
Interface web para trabalhar com notebooks Jupyter e outros arquivos.

### JupyterServer App
Aplicação que fornece a interface do SageMaker Studio.

---

## K

### Kernel
Processo que executa código em notebooks Jupyter. Cada linguagem tem seu kernel (Python, R, etc.).

### KernelGateway App
Aplicação que gerencia e executa kernels no SageMaker Studio.

### Key (S3 Key)
Identificador único de objeto no S3. Inclui o caminho completo: `folder/subfolder/file.csv`

### KMS (Key Management Service)
Serviço de gerenciamento de chaves criptográficas da AWS.

### K-Means
Algoritmo de clustering (não supervisionado) que agrupa dados em K clusters.

### KNN (K-Nearest Neighbors)
Algoritmo de ML que classifica baseado nos K vizinhos mais próximos.

---

## L

### Label
Valor que queremos prever (variável dependente, target). Em ML supervisionado.

### Lambda (AWS Lambda)
Serviço serverless para executar código sem gerenciar servidores.

### Latency (Latência)
Tempo de resposta entre requisição e resposta. Importante em inferência real-time.

### Learning Rate
Hiperparâmetro que controla o tamanho dos passos durante otimização do modelo.

### Lifecycle Configuration
Script executado ao iniciar notebook ou app no SageMaker.

### Linear Learner
Algoritmo built-in do SageMaker para regressão e classificação linear.

### Loss Function
Função que mede erro do modelo. O treinamento busca minimizar essa função.

---

## M

### MAE (Mean Absolute Error)
Métrica de erro: média dos erros absolutos. Mais robusta a outliers que MSE.

### Machine Learning (ML)
Campo da IA onde sistemas aprendem padrões dos dados sem programação explícita.

### Metadata
Dados sobre dados. Ex: data de criação, tamanho, tipo de arquivo.

### Metrics (Métricas)
Valores que medem performance do modelo. Ex: accuracy, RMSE, R².

### MLOps
Práticas de DevOps aplicadas a Machine Learning. Automatização de pipelines ML.

### Model
Representação matemática aprendida dos dados para fazer predições.

### Model Registry
Repositório centralizado de modelos com versionamento e metadata.

### MSE (Mean Squared Error)
Métrica de erro: média dos erros ao quadrado. Penaliza erros grandes.

### Multi-AZ
Deployment em múltiplas Availability Zones para alta disponibilidade.

### Multipart Upload
Upload de arquivo grande em partes paralelas no S3.

---

## N

### NAT Gateway
Serviço que permite recursos em subnet privada acessarem a internet.

### Normalization
Transformação de features para escala comum. Ex: StandardScaler, MinMaxScaler.

### NumPy
Biblioteca Python para computação numérica com arrays multidimensionais.

---

## O

### Object (S3 Object)
Arquivo armazenado no S3. Consiste em dados, key e metadata.

### Outlier
Valor que se desvia significativamente dos outros no dataset.

### Overfitting
Quando modelo aprende ruído dos dados de treino, generalizando mal para novos dados.

---

## P

### Pandas
Biblioteca Python para manipulação e análise de dados tabulares.

### Parameter
Valor interno do modelo aprendido durante treinamento. Ex: pesos de rede neural.

### Parquet
Formato de arquivo colunar comprimido, otimizado para analytics e ML.

### PCA (Principal Component Analysis)
Algoritmo de redução de dimensionalidade mantendo máxima variância.

### Pickle
Formato Python para serializar objetos (salvar modelos).

### Pipeline
Sequência automatizada de etapas de ML (dados → treino → avaliação → deploy).

### Policy (IAM Policy)
Documento JSON que define permissões de acesso a recursos AWS.

### Prefix (S3 Prefix)
"Pasta" no S3. Na verdade, parte do nome do objeto antes do `/`.

### Presigned URL
URL temporária com permissões para acessar objeto privado no S3.

### PyTorch
Framework open-source de deep learning desenvolvido pelo Facebook.

---

## R

### R²  (R-squared / Coefficient of Determination)
Métrica que indica proporção da variância explicada pelo modelo (0 a 1).

### Random Forest
Algoritmo ensemble que combina múltiplas árvores de decisão.

### RDS (Relational Database Service)
Serviço de banco de dados relacional gerenciado da AWS.

### RecordIO-Protobuf
Formato binário eficiente usado por algoritmos built-in do SageMaker.

### Region (Região)
Localização geográfica com múltiplos datacenters AWS. Ex: eu-central-1 (Frankfurt).

### Regression (Regressão)
Tipo de problema de ML supervisionado onde prevemos valores contínuos.

### Regularization
Técnica para prevenir overfitting penalizando complexidade do modelo. Ex: L1, L2.

### RMSE (Root Mean Squared Error)
Raiz quadrada do MSE. Métrica na mesma unidade do target.

### Role (IAM Role)
Ver "IAM Role" acima.

### Route Table
Configuração de rede que determina para onde direcionar tráfego na VPC.

---

## S

### SageMaker Studio
IDE web-based do SageMaker para desenvolvimento de ML.

### Scaler
Transformador que normaliza features. Ex: StandardScaler, MinMaxScaler.

### scikit-learn
Biblioteca Python de ML clássico. Inclui algoritmos, preprocessing e métricas.

### SDK (Software Development Kit)
Conjunto de ferramentas para desenvolvimento. Ex: SageMaker Python SDK.

### Security Group
Firewall virtual que controla tráfego de entrada/saída de recursos AWS.

### Serialization
Processo de converter objeto em formato que pode ser armazenado/transmitido.

### Serverless
Modelo de computação onde provedor gerencia infraestrutura automaticamente.

### Session (SageMaker Session)
Objeto que gerencia interações com serviços AWS do SageMaker.

### Spot Instance
Instância EC2 com capacidade spare da AWS. Até 90% mais barata, pode ser interrompida.

### SQL (Structured Query Language)
Linguagem para consultar bancos de dados relacionais.

### SSE (Server-Side Encryption)
Criptografia de objetos no S3 gerenciada pela AWS.

### Stack (CloudFormation Stack)
Coleção de recursos AWS criados e gerenciados como unidade única.

### Storage Class (S3)
Categoria de armazenamento S3 com diferentes custos/performance. Ex: Standard, Glacier.

### Subnet
Sub-rede dentro de uma VPC. Pode ser pública ou privada.

### Supervised Learning
ML onde modelo aprende de dados rotulados (com labels conhecidos).

---

## T

### Tag
Par chave-valor para organizar e rastrear recursos AWS. Ex: `Environment: Production`

### Target
Variável que queremos prever. Sinônimos: label, dependent variable.

### Template (CloudFormation Template)
Arquivo YAML/JSON que define infraestrutura como código.

### TensorFlow
Framework open-source de deep learning desenvolvido pelo Google.

### Test Set
Conjunto de dados separado para avaliação final do modelo (não visto no treino).

### Training Job
Execução de treinamento de modelo no SageMaker. Roda em instâncias dedicadas.

### Training Set
Conjunto de dados usado para treinar o modelo.

### Transfer Learning
Reutilizar modelo pré-treinado como ponto de partida para nova tarefa.

### Trust Policy
Documento que define quais entidades podem assumir uma IAM Role.

---

## U

### Underfitting
Quando modelo é muito simples para capturar padrões dos dados.

### Unsupervised Learning
ML onde modelo aprende padrões de dados não rotulados.

### URI (Uniform Resource Identifier)
Identificador de recurso. No S3: `s3://bucket/key`

### User Profile
Identidade individual dentro de SageMaker Domain. Cada usuário tem seu profile.

---

## V

### Validation Set
Conjunto de dados para ajustar hiperparâmetros e avaliar durante treinamento.

### Variable
Característica dos dados. Feature (entrada) ou label (saída).

### vCPU (Virtual CPU)
CPU virtual em instância EC2. Não equivale exatamente a core físico.

### Versioning (S3 Versioning)
Manter múltiplas versões de objetos no S3.

### VPC (Virtual Private Cloud)
Rede virtual isolada logicamente na AWS. Controla redes e segurança.

### VPC Endpoint
Conexão privada entre VPC e serviços AWS sem usar internet pública.

---

## W

### Weight Decay
Técnica de regularização L2 que penaliza pesos grandes.

---

## X

### XGBoost (eXtreme Gradient Boosting)
Algoritmo ensemble baseado em gradient boosting. Muito popular em competições Kaggle.

---

## Símbolos e Acrônimos Adicionais

### λ (Lambda)
Parâmetro de regularização que controla força da penalização.

### η (Eta)
Learning rate no XGBoost.

### API
Application Programming Interface

### ARN
Amazon Resource Name

### AZ
Availability Zone

### CLI
Command Line Interface

### CSV
Comma-Separated Values

### EBS
Elastic Block Store

### EC2
Elastic Compute Cloud

### ECR
Elastic Container Registry

### EDA
Exploratory Data Analysis

### EFS
Elastic File System

### ETL
Extract, Transform, Load

### GPU
Graphics Processing Unit

### HPO
Hyperparameter Optimization

### IAM
Identity and Access Management

### IDE
Integrated Development Environment

### JSON
JavaScript Object Notation

### KMS
Key Management Service

### KNN
K-Nearest Neighbors

### MAE
Mean Absolute Error

### ML
Machine Learning

### MLOps
Machine Learning Operations

### MSE
Mean Squared Error

### NLP
Natural Language Processing

### PCA
Principal Component Analysis

### RDS
Relational Database Service

### RMSE
Root Mean Squared Error

### S3
Simple Storage Service

### SDK
Software Development Kit

### SQL
Structured Query Language

### SSE
Server-Side Encryption

### SSH
Secure Shell

### SSL/TLS
Secure Sockets Layer / Transport Layer Security

### URI
Uniform Resource Identifier

### URL
Uniform Resource Locator

### VPC
Virtual Private Cloud

### YAML
YAML Ain't Markup Language

---

## Referências Úteis

### Documentação Oficial
- [AWS Glossary](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html)
- [SageMaker Glossary](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [ML Glossary](https://developers.google.com/machine-learning/glossary)

### Para Mais Informações
Consulte os módulos do treinamento para explicações detalhadas de cada conceito.

---

**Última atualização:** Fevereiro 2026
