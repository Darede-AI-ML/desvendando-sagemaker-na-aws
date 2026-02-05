# Treinamento AWS SageMaker

Bem-vindo ao treinamento prático de Amazon SageMaker! Este guia foi desenvolvido para ajudar iniciantes a compreender e utilizar os principais recursos do AWS SageMaker para projetos de Machine Learning.

## Visão Geral

Este treinamento é estruturado em 9 módulos práticos que cobrem desde o acesso inicial à AWS até o treinamento de modelos usando algoritmos built-in do SageMaker. Cada módulo foi desenvolvido com explicações detalhadas, exemplos de código e boas práticas.

## Pré-requisitos

### Conhecimentos Necessários
- Conhecimento básico de Python
- Familiaridade com conceitos de Machine Learning (recomendado, mas não obrigatório)
- Noções básicas de computação em nuvem

### Recursos Técnicos
- Acesso a uma conta AWS (será fornecido durante o treinamento)
- Navegador web atualizado (Chrome, Firefox ou Safari)
- Conexão estável com a internet

## Estrutura do Treinamento

### [Módulo 1: Acesso à Conta AWS](modulos/01-acesso-conta-aws.md)
**Duração estimada: 30 minutos**

Aprenda a acessar o console AWS, selecionar a região correta e verificar permissões básicas.

**Tópicos:**
- Login no console AWS
- Navegação por regiões
- Verificação de permissões IAM
- Validação de acesso ao SageMaker e S3

---

### [Módulo 2: Criação do Domínio SageMaker via IaC](modulos/02-criacao-dominio-sagemaker.md)
**Duração estimada: 45 minutos**

Entenda e implemente Infrastructure as Code usando CloudFormation para criar um domínio SageMaker.

**Tópicos:**
- Conceitos de Infrastructure as Code
- Análise do template CloudFormation
- Deploy do SageMaker Domain
- Validação no console

---

### [Módulo 3: Criação de Usuários no SageMaker Domain](modulos/03-criacao-usuarios.md)
**Duração estimada: 20 minutos**

Configure perfis de usuário para acesso ao ambiente SageMaker.

**Tópicos:**
- Conceito de User Profile
- Criação de usuários
- Gerenciamento de permissões

---

### [Módulo 4: Acesso ao SageMaker Studio](modulos/04-acesso-sagemaker-studio.md)
**Duração estimada: 30 minutos**

Navegue pelo ambiente de desenvolvimento do SageMaker Studio.

**Tópicos:**
- Acesso ao SageMaker Studio
- Interface e navegação
- JupyterLab vs Studio
- Apps e Kernels

---

### [Módulo 5: Instâncias de Trabalho](modulos/05-instancias-trabalho.md)
**Duração estimada: 25 minutos**

Compreenda os tipos de instâncias e como gerenciá-las eficientemente.

**Tópicos:**
- Tipos de instância disponíveis
- Seleção adequada de recursos
- Gestão de custos
- Monitoramento

---

### [Módulo 6: Upload de Datasets](modulos/06-upload-datasets.md)
**Duração estimada: 40 minutos**

Aprenda a gerenciar dados no Amazon S3 e acessá-los do SageMaker.

**Tópicos:**
- Conceitos do Amazon S3
- Métodos de upload
- Leitura de dados no SageMaker
- Boas práticas de organização

---

### [Módulo 7: Execução de Código de Exemplo](modulos/07-execucao-codigo-exemplo.md)
**Duração estimada: 60 minutos**

Execute análises exploratórias e treine modelos simples localmente.

**Tópicos:**
- Estrutura de projeto ML
- Análise exploratória de dados
- Treinamento local
- Salvamento de artefatos

---

### [Módulo 8: Algoritmos Built-in do SageMaker](modulos/08-algoritmos-builtin.md)
**Duração estimada: 60 minutos**

Utilize os algoritmos otimizados do SageMaker para treinamento gerenciado.

**Tópicos:**
- Treino local vs. gerenciado
- Principais algoritmos built-in
- SageMaker Estimators
- Monitoramento de métricas

---

### [Módulo 9: Encerramento e Boas Práticas](modulos/09-encerramento-boas-praticas.md)
**Duração estimada: 20 minutos**

Finalize seu ambiente adequadamente e aprenda boas práticas.

**Tópicos:**
- Limpeza de recursos
- Gestão de custos
- Segurança
- Próximos passos

---

## Tempo Total Estimado

**Aproximadamente 5h30min** (incluindo exercícios práticos)

## Recursos Adicionais

### Templates de Infraestrutura
- [CloudFormation - SageMaker Domain](cloudformation/sagemaker-domain.yaml)
- [CloudFormation - S3 Bucket](cloudformation/s3-bucket.yaml)

### Código de Exemplo
- [Snippets Python](codigo-exemplo/snippets.md)

### Referências
- [Glossário de Termos](recursos/glossario.md)
- [Documentação Oficial AWS SageMaker](https://docs.aws.amazon.com/sagemaker/)
- [Guia de Preços SageMaker](https://aws.amazon.com/sagemaker/pricing/)

## FAQ - Perguntas Frequentes

### 1. Preciso de uma conta AWS própria?
Não. Durante o treinamento, serão fornecidas credenciais de acesso temporárias.

### 2. Há custos envolvidos?
O ambiente de treinamento é fornecido sem custos para os participantes. É importante seguir as instruções de limpeza para evitar cobranças após o treinamento.

### 3. Posso reproduzir este treinamento na minha conta pessoal?
Sim! Todos os templates e códigos estão disponíveis. Lembre-se de que haverá custos associados ao uso dos recursos AWS.

### 4. Qual região AWS devo usar?
Recomendamos a região de Frankfurt (eu-central-1) para este treinamento.

### 5. O que fazer se encontrar erros?
Cada módulo inclui uma seção de troubleshooting. Se persistir, consulte o instrutor.

### 6. Os notebooks funcionam em Python 2?
Não. Todo o código foi desenvolvido para Python 3.8+.

### 7. Posso usar meu próprio dataset?
Sim! O módulo 6 ensina como fazer upload de seus próprios dados.

### 8. Preciso saber programar?
Conhecimento básico de Python é necessário. Os exemplos são comentados para facilitar o entendimento.

## Suporte

Durante o treinamento, os instrutores estarão disponíveis para dúvidas e assistência técnica.

## Contribuições

Este material é mantido para fins educacionais. Sugestões de melhoria são bem-vindas.

---

**Última atualização:** Fevereiro 2026  
**Versão:** 1.0
