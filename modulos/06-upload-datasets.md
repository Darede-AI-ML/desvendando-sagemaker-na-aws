# Módulo 6: Upload de Datasets para o Ambiente SageMaker

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:
- Fazer upload de arquivos diretamente no JupyterLab
- Criar datasets em memória para testes rápidos
- Entender quando usar S3 para datasets maiores
- Carregar dados em notebooks Python

## Duração Estimada
20 minutos

---

## 1. Formas de Trabalhar com Dados no SageMaker

Existem **três formas principais** de trabalhar com dados:

| Método | Quando Usar | Complexidade |
|--------|-------------|--------------|
| **Upload direto no JupyterLab** | Arquivos pequenos (<100MB) | Simples |
| **Dataset em memória** | Testes rápidos, exemplos | Muito simples |
| **Amazon S3** | Datasets grandes, produção | Mais complexo |

Para este treinamento, usaremos principalmente as **duas primeiras opções**.

---

## 2. Upload Direto no JupyterLab (Recomendado)

A forma mais simples de trabalhar com dados é fazer **upload direto** pela interface do JupyterLab.

### Dataset do Treinamento

📁 **Arquivo:** `scripts/no-shows.csv`

| Informação | Valor |
|------------|-------|
| **Fonte** | [Kaggle - Medical Appointment No Shows](https://www.kaggle.com/datasets/joniarroba/noshowappointments) |
| **Registros** | ~110.000 |
| **Problema** | Classificação (paciente compareceu ou não) |

### Passo a Passo: Upload no JupyterLab

**Passo 1:** No JupyterLab, localize o painel de arquivos à esquerda

**Passo 2:** Clique no botão **Upload** (ícone de seta para cima)

```
┌─────────────────────────────────────────────────────────────┐
│  JupyterLab                                                 │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│  📁 Files │                                                 │
│  ─────── │                                                  │
│  [⬆️ Upload]  ◀─── Clique aqui                              │
│  [+ Folder]   │                                             │
│          │                                                  │
│  📄 file1.py │                                              │
│  📄 file2.ipynb                                             │
│          │                                                  │
└──────────┴──────────────────────────────────────────────────┘
```

**Passo 3:** Selecione o arquivo `no-shows.csv` do seu computador

**Passo 4:** Aguarde o upload completar

**Passo 5:** O arquivo aparecerá na lista de arquivos

### Carregar no Notebook

Após o upload, carregue os dados no notebook:

```python
import pandas as pd

# Carregar o dataset
df = pd.read_csv('no-shows.csv')

# Verificar os dados
print(f"Total de registros: {len(df)}")
print(f"Colunas: {list(df.columns)}")

# Visualizar primeiras linhas
df.head()
```

**Saída esperada:**
```
Total de registros: 110527
Colunas: ['PatientId', 'AppointmentID', 'Gender', 'ScheduledDay', ...]
```

### Colunas do Dataset no-shows.csv

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `PatientId` | int | ID do paciente |
| `AppointmentID` | int | ID do agendamento |
| `Gender` | str | Gênero (M/F) |
| `ScheduledDay` | datetime | Quando foi agendado |
| `AppointmentDay` | datetime | Data da consulta |
| `Age` | int | Idade |
| `Neighbourhood` | str | Bairro |
| `Scholarship` | int | Bolsa Família (0/1) |
| `Hipertension` | int | Hipertensão (0/1) |
| `Diabetes` | int | Diabetes (0/1) |
| `Alcoholism` | int | Alcoolismo (0/1) |
| `Handcap` | int | Deficiência (0/1) |
| `SMS_received` | int | Recebeu SMS (0/1) |
| `No-show` | str | **Target:** Yes/No |

---

## 3. Dataset em Memória (Para Testes)

Para testes rápidos ou exemplos, podemos criar datasets diretamente no código.

### Exemplo 1: DataFrame Simples

```python
import pandas as pd

# Criar DataFrame de exemplo
dados = pd.DataFrame({
    'Idade': [25, 30, 22, 35, 28, 40, 27, 23, 32, 29],
    'Rendimento': [1800, 2400, 1500, 3100, 2000, 4000, 1900, 1700, 2800, 2200]
})

print("Dataset criado em memória:")
dados
```

### Exemplo 2: Dataset do Scikit-learn

O Scikit-learn inclui datasets prontos para experimentação:

```python
from sklearn.datasets import fetch_california_housing
import pandas as pd

# Carregar dataset California Housing
california = fetch_california_housing()

# Converter para DataFrame
X = pd.DataFrame(california.data, columns=california.feature_names)
y = pd.Series(california.target, name='MedHouseVal')

print(f"Registros: {len(X)}")
print(f"Features: {list(X.columns)}")
X.head()
```

**Datasets disponíveis no Scikit-learn:**

| Dataset | Função | Tipo | Registros |
|---------|--------|------|-----------|
| California Housing | `fetch_california_housing()` | Regressão | 20.640 |
| Iris | `load_iris()` | Classificação | 150 |
| Digits | `load_digits()` | Classificação | 1.797 |
| Wine | `load_wine()` | Classificação | 178 |
| Breast Cancer | `load_breast_cancer()` | Classificação | 569 |

### Quando Usar Cada Abordagem

| Situação | Dataset em Memória | Upload de Arquivo |
|----------|-------------------|-------------------|
| Testar código rapidamente | ✅ | |
| Aprender conceitos | ✅ | |
| Dados reais do projeto | | ✅ |
| Reproduzir análises | | ✅ |
| Compartilhar com equipe | | ✅ |

---

## 4. Amazon S3 (Para Referência)

O **Amazon S3** é usado quando:
- Datasets são muito grandes (>100MB)
- Dados precisam ser compartilhados entre notebooks
- Training Jobs do SageMaker precisam acessar dados

### Conceito Básico

```
S3 = "HD na nuvem"

s3://meu-bucket/pasta/arquivo.csv
   │      │       │       │
   │      │       │       └── arquivo
   │      │       └── prefixo (pasta)
   │      └── nome do bucket
   └── protocolo S3
```

### Upload para S3 via Notebook (Opcional)

Se precisar enviar dados para o S3:

```python
import sagemaker

# Sessão SageMaker
session = sagemaker.Session()

# Bucket padrão (criado automaticamente)
bucket = session.default_bucket()

# Upload do arquivo
s3_path = session.upload_data(
    path='no-shows.csv',
    bucket=bucket,
    key_prefix='dados'
)

print(f"Arquivo enviado para: {s3_path}")
```

### Ler do S3

```python
import pandas as pd

# Ler diretamente do S3
df = pd.read_csv('s3://meu-bucket/dados/no-shows.csv')
```

> **Nota:** Para o treinamento básico, o upload direto no JupyterLab é suficiente. O S3 será usado no Módulo 8 para os Training Jobs.

---

## 5. Notebooks de Exemplo

Os notebooks do treinamento já incluem código para carregar dados:

| Notebook | Tipo de Dados | Localização |
|----------|---------------|-------------|
| `exemplo-treinamento.ipynb` | Em memória (California Housing) | `scripts/` |
| `exemplo-treinamento-sagemaker.ipynb` | Upload para S3 | `scripts/` |

---

## 6. Exercício Prático

### Exercício 1: Upload e Carregamento

1. Faça upload do arquivo `no-shows.csv` no JupyterLab
2. Crie um novo notebook
3. Execute o código:

```python
import pandas as pd

# Carregar dados
df = pd.read_csv('no-shows.csv')

# Informações básicas
print("=" * 50)
print("INFORMAÇÕES DO DATASET")
print("=" * 50)
print(f"Total de registros: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")
print(f"\nColunas:")
for col in df.columns:
    print(f"  - {col}: {df[col].dtype}")

# Ver distribuição do target
print(f"\nDistribuição do Target (No-show):")
print(df['No-show'].value_counts())
```

### Exercício 2: Dataset em Memória

```python
import pandas as pd
from sklearn.datasets import fetch_california_housing

# Carregar dataset
california = fetch_california_housing()
df = pd.DataFrame(california.data, columns=california.feature_names)
df['target'] = california.target

# Estatísticas
print("Estatísticas do California Housing:")
df.describe()
```

---

## 7. Checklist de Validação

- [ ] Consegui fazer upload de arquivo no JupyterLab
- [ ] Carreguei o `no-shows.csv` com pandas
- [ ] Criei um dataset em memória
- [ ] Entendi quando usar cada abordagem

---

## Resumo

| Método | Comando | Uso |
|--------|---------|-----|
| Upload JupyterLab | Interface gráfica | Arquivos locais |
| Dataset memória | `pd.DataFrame({...})` | Testes rápidos |
| Scikit-learn | `fetch_california_housing()` | Datasets prontos |
| S3 | `pd.read_csv('s3://...')` | Produção |

---

## Próximo Módulo

Dados carregados! Vamos executar código de análise e treinamento!

➡️ [Módulo 7: Execução de Código de Exemplo](07-execucao-codigo-exemplo.md)
