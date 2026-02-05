# Snippets de Código Python - SageMaker Training

Este arquivo contém todos os snippets de código utilizados durante o treinamento, organizados por categoria para fácil referência e reutilização.

---

## Índice

1. [Configuração Inicial](#1-configuração-inicial)
2. [Trabalho com S3](#2-trabalho-com-s3)
3. [Análise Exploratória de Dados](#3-análise-exploratória-de-dados)
4. [Preparação de Dados](#4-preparação-de-dados)
5. [Treinamento Local](#5-treinamento-local)
6. [Treinamento SageMaker (XGBoost)](#6-treinamento-sagemaker-xgboost)
7. [Monitoramento e Métricas](#7-monitoramento-e-métricas)
8. [Salvamento de Artefatos](#8-salvamento-de-artefatos)
9. [Limpeza de Recursos](#9-limpeza-de-recursos)
10. [Utilitários](#10-utilitários)

---

## 1. Configuração Inicial

### 1.1 Importar Bibliotecas

```python
# Bibliotecas padrão
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

# Científicas
import numpy as np
import pandas as pd

# Machine Learning
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Visualização
import matplotlib.pyplot as plt
import seaborn as sns

# AWS
import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator

# Configurações
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
```

### 1.2 Configurar Ambiente AWS

```python
def setup_aws_environment():
    """Configura ambiente AWS e retorna variáveis importantes"""
    
    # Sessão SageMaker
    session = sagemaker.Session()
    region = session.boto_region_name
    bucket = session.default_bucket()
    role = get_execution_role()
    
    # Cliente boto3
    s3_client = boto3.client('s3', region_name=region)
    sm_client = boto3.client('sagemaker', region_name=region)
    
    # Informações
    print("=" * 50)
    print("CONFIGURAÇÃO AWS")
    print("=" * 50)
    print(f"Região: {region}")
    print(f"Bucket: {bucket}")
    print(f"Role: {role[:50]}...")
    
    return {
        'session': session,
        'region': region,
        'bucket': bucket,
        'role': role,
        's3_client': s3_client,
        'sm_client': sm_client
    }

# Uso
aws_env = setup_aws_environment()
```

### 1.3 Criar Estrutura de Diretórios

```python
def create_project_structure():
    """Cria estrutura de diretórios para o projeto"""
    
    directories = [
        'data/raw',
        'data/processed',
        'data/train',
        'data/validation',
        'data/test',
        'models',
        'outputs/figures',
        'outputs/reports',
        'src'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("Estrutura de diretórios criada!")
    print("\n".join(f"  ✓ {d}" for d in directories))

# Uso
create_project_structure()
```

---

## 2. Trabalho com S3

### 2.1 Upload de Arquivo

```python
def upload_to_s3(local_path, bucket, s3_key, region='eu-central-1'):
    """Upload de arquivo para S3"""
    
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        s3_client.upload_file(local_path, bucket, s3_key)
        s3_uri = f's3://{bucket}/{s3_key}'
        print(f"✓ Upload concluído: {s3_uri}")
        return s3_uri
    except Exception as e:
        print(f"✗ Erro no upload: {e}")
        return None

# Uso
upload_to_s3('data/train/train.csv', 'meu-bucket', 'data/train.csv')
```

### 2.2 Download de Arquivo

```python
def download_from_s3(bucket, s3_key, local_path, region='eu-central-1'):
    """Download de arquivo do S3"""
    
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        # Criar diretório se não existir
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        
        s3_client.download_file(bucket, s3_key, local_path)
        print(f"✓ Download concluído: {local_path}")
        return True
    except Exception as e:
        print(f"✗ Erro no download: {e}")
        return False

# Uso
download_from_s3('meu-bucket', 'data/train.csv', './data/train.csv')
```

### 2.3 Listar Arquivos no S3

```python
def list_s3_files(bucket, prefix='', region='eu-central-1'):
    """Lista arquivos em um bucket S3"""
    
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            print(f"Nenhum arquivo encontrado em s3://{bucket}/{prefix}")
            return []
        
        files = []
        for obj in response['Contents']:
            size_mb = obj['Size'] / (1024 * 1024)
            files.append({
                'key': obj['Key'],
                'size_mb': size_mb,
                'last_modified': obj['LastModified']
            })
        
        # Exibir
        print(f"Arquivos em s3://{bucket}/{prefix}:")
        for f in files:
            print(f"  {f['key']} ({f['size_mb']:.2f} MB)")
        
        return files
        
    except Exception as e:
        print(f"✗ Erro ao listar: {e}")
        return []

# Uso
list_s3_files('meu-bucket', 'data/')
```

### 2.4 Ler CSV Direto do S3

```python
def read_csv_from_s3(bucket, key, **kwargs):
    """Lê CSV diretamente do S3 usando pandas"""
    
    s3_uri = f's3://{bucket}/{key}'
    
    try:
        df = pd.read_csv(s3_uri, **kwargs)
        print(f"✓ Dataset carregado: {df.shape}")
        return df
    except Exception as e:
        print(f"✗ Erro ao ler: {e}")
        return None

# Uso
df = read_csv_from_s3('meu-bucket', 'data/train.csv')
```

---

## 3. Análise Exploratória de Dados

### 3.1 Informações Básicas do Dataset

```python
def dataset_info(df):
    """Exibe informações completas sobre o dataset"""
    
    print("=" * 60)
    print("INFORMAÇÕES DO DATASET")
    print("=" * 60)
    
    print(f"\nShape: {df.shape}")
    print(f"Linhas: {df.shape[0]:,}")
    print(f"Colunas: {df.shape[1]}")
    print(f"Tamanho em memória: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\n" + "=" * 60)
    print("TIPOS DE DADOS")
    print("=" * 60)
    print(df.dtypes)
    
    print("\n" + "=" * 60)
    print("VALORES FALTANTES")
    print("=" * 60)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing': missing[missing > 0],
        'Percent': missing_pct[missing > 0]
    }).sort_values('Missing', ascending=False)
    
    if len(missing_df) == 0:
        print("✓ Nenhum valor faltante!")
    else:
        print(missing_df)
    
    print("\n" + "=" * 60)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("=" * 60)
    print(df.describe())
    
    print("\n" + "=" * 60)
    print("DUPLICATAS")
    print("=" * 60)
    duplicates = df.duplicated().sum()
    print(f"Total de linhas duplicadas: {duplicates}")

# Uso
dataset_info(df)
```

### 3.2 Visualização de Distribuição

```python
def plot_distribution(df, column, figsize=(12, 5)):
    """Plota histograma e boxplot de uma coluna"""
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histograma
    axes[0].hist(df[column], bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_title(f'Distribuição de {column}')
    axes[0].set_xlabel(column)
    axes[0].set_ylabel('Frequência')
    axes[0].axvline(df[column].mean(), color='red', linestyle='--', 
                    label=f'Média: {df[column].mean():.2f}')
    axes[0].axvline(df[column].median(), color='green', linestyle='--', 
                    label=f'Mediana: {df[column].median():.2f}')
    axes[0].legend()
    
    # Boxplot
    axes[1].boxplot(df[column])
    axes[1].set_title(f'Boxplot de {column}')
    axes[1].set_ylabel(column)
    
    plt.tight_layout()
    plt.show()
    
    # Estatísticas
    print(f"Estatísticas de {column}:")
    print(f"  Mínimo: {df[column].min():.2f}")
    print(f"  Q1: {df[column].quantile(0.25):.2f}")
    print(f"  Mediana: {df[column].median():.2f}")
    print(f"  Q3: {df[column].quantile(0.75):.2f}")
    print(f"  Máximo: {df[column].max():.2f}")
    print(f"  Média: {df[column].mean():.2f}")
    print(f"  Desvio Padrão: {df[column].std():.2f}")

# Uso
plot_distribution(df, 'MedHouseVal')
```

### 3.3 Matriz de Correlação

```python
def plot_correlation_matrix(df, figsize=(10, 8), method='pearson'):
    """Plota matriz de correlação"""
    
    # Calcular correlação
    corr = df.corr(method=method)
    
    # Plotar
    plt.figure(figsize=figsize)
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    plt.title(f'Matriz de Correlação ({method.capitalize()})', fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()
    
    # Top correlações
    if 'target' in df.columns or len(df.columns) > 0:
        target_col = 'target' if 'target' in df.columns else df.columns[-1]
        if target_col in corr.columns:
            print(f"\nCorrelações com {target_col}:")
            print(corr[target_col].sort_values(ascending=False))

# Uso
plot_correlation_matrix(df)
```

---

## 4. Preparação de Dados

### 4.1 Split Train/Val/Test

```python
def split_data(X, y, train_size=0.7, val_size=0.15, test_size=0.15, random_state=42):
    """Split em train, validation e test"""
    
    if not np.isclose(train_size + val_size + test_size, 1.0):
        raise ValueError("train_size + val_size + test_size deve ser igual a 1.0")
    
    # Split 1: Train vs Temp
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y,
        test_size=(1 - train_size),
        random_state=random_state
    )
    
    # Split 2: Val vs Test
    val_ratio = val_size / (val_size + test_size)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        test_size=(1 - val_ratio),
        random_state=random_state
    )
    
    print("Split concluído:")
    print(f"  Train: {len(X_train):,} ({len(X_train)/len(X):.1%})")
    print(f"  Validation: {len(X_val):,} ({len(X_val)/len(X):.1%})")
    print(f"  Test: {len(X_test):,} ({len(X_test)/len(X):.1%})")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

# Uso
X = df.drop('target', axis=1)
y = df['target']
X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)
```

### 4.2 Normalização

```python
def normalize_data(X_train, X_val, X_test, method='standard'):
    """Normaliza dados usando StandardScaler ou MinMaxScaler"""
    
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError("method deve ser 'standard' ou 'minmax'")
    
    # Fit apenas no train
    scaler.fit(X_train)
    
    # Transform em todos
    X_train_scaled = scaler.transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Normalização ({method}) concluída:")
    print(f"  Média train: {X_train_scaled.mean():.6f}")
    print(f"  Std train: {X_train_scaled.std():.6f}")
    
    return X_train_scaled, X_val_scaled, X_test_scaled, scaler

# Uso
X_train_scaled, X_val_scaled, X_test_scaled, scaler = normalize_data(
    X_train, X_val, X_test, method='standard'
)
```

---

## 5. Treinamento Local

### 5.1 Treinar e Avaliar Modelo

```python
def train_and_evaluate(model, X_train, y_train, X_val, y_val, model_name='Model'):
    """Treina modelo e retorna métricas"""
    
    # Treinar
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # Predições
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    
    # Métricas
    metrics = {
        'model_name': model_name,
        'training_time': training_time,
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
        'train_mae': mean_absolute_error(y_train, y_train_pred),
        'train_r2': r2_score(y_train, y_train_pred),
        'val_rmse': np.sqrt(mean_squared_error(y_val, y_val_pred)),
        'val_mae': mean_absolute_error(y_val, y_val_pred),
        'val_r2': r2_score(y_val, y_val_pred)
    }
    
    # Exibir
    print("=" * 50)
    print(f"MODELO: {model_name}")
    print("=" * 50)
    print(f"Tempo de treinamento: {training_time:.2f}s")
    print("\nMétricas de Treino:")
    print(f"  RMSE: {metrics['train_rmse']:.4f}")
    print(f"  MAE:  {metrics['train_mae']:.4f}")
    print(f"  R²:   {metrics['train_r2']:.4f}")
    print("\nMétricas de Validação:")
    print(f"  RMSE: {metrics['val_rmse']:.4f}")
    print(f"  MAE:  {metrics['val_mae']:.4f}")
    print(f"  R²:   {metrics['val_r2']:.4f}")
    
    return model, metrics

# Uso
lr_model, lr_metrics = train_and_evaluate(
    LinearRegression(),
    X_train_scaled, y_train,
    X_val_scaled, y_val,
    'Linear Regression'
)
```

---

## 6. Treinamento SageMaker (XGBoost)

### 6.1 Preparar Dados para XGBoost

```python
def prepare_data_for_xgboost(df, target_col, output_path):
    """Prepara dados no formato XGBoost (target na primeira coluna, sem header)"""
    
    feature_cols = [col for col in df.columns if col != target_col]
    df_xgb = df[[target_col] + feature_cols]
    
    # Salvar
    df_xgb.to_csv(output_path, header=False, index=False)
    print(f"✓ Dados salvos: {output_path}")
    print(f"  Shape: {df_xgb.shape}")
    print(f"  Colunas: [{target_col}] + {len(feature_cols)} features")
    
    return output_path

# Uso
prepare_data_for_xgboost(train_df, 'MedHouseVal', 'data/train/train_xgb.csv')
```

### 6.2 Treinar XGBoost no SageMaker

```python
def train_xgboost_sagemaker(
    train_s3_uri,
    val_s3_uri,
    output_path,
    role,
    session,
    region,
    instance_type='ml.m5.xlarge',
    hyperparameters=None
):
    """Treina modelo XGBoost no SageMaker"""
    
    # Obter container
    xgb_container = sagemaker.image_uris.retrieve(
        framework='xgboost',
        region=region,
        version='1.5-1'
    )
    
    # Criar estimator
    estimator = Estimator(
        image_uri=xgb_container,
        role=role,
        instance_count=1,
        instance_type=instance_type,
        output_path=output_path,
        sagemaker_session=session,
        base_job_name='xgboost-training'
    )
    
    # Hiperparâmetros padrão
    if hyperparameters is None:
        hyperparameters = {
            'objective': 'reg:squarederror',
            'num_round': 100,
            'max_depth': 5,
            'eta': 0.2,
            'gamma': 4,
            'min_child_weight': 6,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'eval_metric': 'rmse',
            'silent': 0
        }
    
    estimator.set_hyperparameters(**hyperparameters)
    
    # Inputs
    train_input = TrainingInput(s3_data=train_s3_uri, content_type='text/csv')
    val_input = TrainingInput(s3_data=val_s3_uri, content_type='text/csv')
    
    # Treinar
    print("Iniciando treinamento...")
    estimator.fit({'train': train_input, 'validation': val_input})
    
    print(f"\n✓ Treinamento concluído!")
    print(f"  Modelo: {estimator.model_data}")
    
    return estimator

# Uso
estimator = train_xgboost_sagemaker(
    train_s3_uri='s3://bucket/train.csv',
    val_s3_uri='s3://bucket/val.csv',
    output_path='s3://bucket/output/',
    role=aws_env['role'],
    session=aws_env['session'],
    region=aws_env['region']
)
```

---

## 7. Monitoramento e Métricas

### 7.1 Visualizar Curva de Aprendizado

```python
def plot_learning_curves(train_scores, val_scores, metric_name='RMSE'):
    """Plota curvas de aprendizado"""
    
    epochs = list(range(len(train_scores)))
    
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, train_scores, label=f'Train {metric_name}', linewidth=2)
    plt.plot(epochs, val_scores, label=f'Validation {metric_name}', linewidth=2)
    plt.xlabel('Epoch')
    plt.ylabel(metric_name)
    plt.title('Curvas de Aprendizado')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Uso
plot_learning_curves(train_rmse_history, val_rmse_history)
```

---

## 8. Salvamento de Artefatos

### 8.1 Salvar Modelo e Metadados

```python
import joblib

def save_model_artifacts(model, scaler, metadata, base_path='models'):
    """Salva modelo, scaler e metadados"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model_dir = Path(base_path) / timestamp
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar modelo
    model_path = model_dir / 'model.pkl'
    joblib.dump(model, model_path)
    
    # Salvar scaler
    scaler_path = model_dir / 'scaler.pkl'
    joblib.dump(scaler, scaler_path)
    
    # Salvar metadados
    metadata['timestamp'] = timestamp
    metadata_path = model_dir / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Artefatos salvos em: {model_dir}")
    print(f"  - {model_path.name}")
    print(f"  - {scaler_path.name}")
    print(f"  - {metadata_path.name}")
    
    return model_dir

# Uso
metadata = {
    'model_type': 'RandomForest',
    'val_rmse': 0.634,
    'val_r2': 0.813,
    'features': X_train.columns.tolist()
}

save_model_artifacts(model, scaler, metadata)
```

---

## 9. Limpeza de Recursos

### 9.1 Parar Todas as Apps

```python
def cleanup_sagemaker_apps(domain_id, user_profile, region='eu-central-1'):
    """Para todas as apps de um usuário"""
    
    sm_client = boto3.client('sagemaker', region_name=region)
    
    # Listar apps
    response = sm_client.list_apps(
        DomainIdEquals=domain_id,
        UserProfileNameEquals=user_profile
    )
    
    apps_to_delete = [
        app for app in response['Apps']
        if app['AppType'] == 'KernelGateway' and app['Status'] == 'InService'
    ]
    
    if not apps_to_delete:
        print("✓ Nenhuma app para deletar")
        return
    
    print(f"Deletando {len(apps_to_delete)} app(s)...")
    
    for app in apps_to_delete:
        print(f"  Deletando: {app['AppName']}")
        sm_client.delete_app(
            DomainId=domain_id,
            UserProfileName=user_profile,
            AppType='KernelGateway',
            AppName=app['AppName']
        )
    
    print("✓ Limpeza concluída!")

# Uso
cleanup_sagemaker_apps('d-xxxxxxxxxxxx', 'default-user')
```

---

## 10. Utilitários

### 10.1 Timer / Cronômetro

```python
from contextlib import contextmanager

@contextmanager
def timer(description="Operação"):
    """Context manager para medir tempo de execução"""
    
    start = time.time()
    yield
    elapsed = time.time() - start
    
    print(f"⏱️  {description}: {elapsed:.2f}s")

# Uso
with timer("Carregamento de dados"):
    df = pd.read_csv('large_file.csv')
```

### 10.2 Verificar Recursos do Sistema

```python
import psutil

def check_system_resources():
    """Verifica CPU, memória e disco"""
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    
    # Memória
    memory = psutil.virtual_memory()
    
    # Disco
    disk = psutil.disk_usage('/')
    
    print("=" * 50)
    print("RECURSOS DO SISTEMA")
    print("=" * 50)
    print(f"\nCPU:")
    print(f"  Uso: {cpu_percent}%")
    print(f"  Núcleos: {cpu_count}")
    print(f"\nMemória:")
    print(f"  Uso: {memory.percent}%")
    print(f"  Disponível: {memory.available / (1024**3):.2f} GB")
    print(f"  Total: {memory.total / (1024**3):.2f} GB")
    print(f"\nDisco:")
    print(f"  Uso: {disk.percent}%")
    print(f"  Livre: {disk.free / (1024**3):.2f} GB")
    print(f"  Total: {disk.total / (1024**3):.2f} GB")

# Uso
check_system_resources()
```

---

## Conclusão

Estes snippets cobrem as operações mais comuns em projetos de Machine Learning no SageMaker. Para usar:

1. Copie o snippet desejado
2. Ajuste os parâmetros conforme necessário
3. Execute no seu notebook SageMaker

**Dica:** Salve seus snippets favoritos em um arquivo `.py` para reutilização!

---

**Última atualização:** Fevereiro 2026
