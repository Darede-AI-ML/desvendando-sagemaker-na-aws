# Módulo 7: Execução de Código de Exemplo para Análise e Treinamento

## Objetivos de Aprendizagem

Ao final deste módulo, você será capaz de:
- Realizar análise exploratória de dados (EDA) univariada
- Entender estatísticas de assimetria e curtose
- Treinar modelos XGBoost localmente no notebook
- Avaliar modelos com métricas de regressão
- Interpretar importância de variáveis

## Duração Estimada
45 minutos

---

## 1. Material Disponível

Para este módulo, utilizaremos os notebooks e scripts disponíveis na pasta `scripts/`:

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `exemplo-treinamento.ipynb` | **Notebook principal** | Executar no JupyterLab |
| `cap2_EDA_univariada.py` | Script de EDA | Referência |
| `cap9_XGBoost_Boston_regressão.py` | Script XGBoost | Referência |

### Como Usar

1. Faça upload do notebook `exemplo-treinamento.ipynb` para o SageMaker Studio
2. Ou copie o código das seções abaixo para um novo notebook

---

## 2. Análise Exploratória de Dados (EDA) Univariada

A análise univariada examina cada variável **individualmente** para entender suas características.

### 2.1 Conceitos Importantes

| Conceito | O que mede | Interpretação |
|----------|-----------|---------------|
| **Média** | Valor central | Tendência central |
| **Desvio padrão** | Dispersão dos dados | Quanto os dados variam |
| **Assimetria (Skewness)** | Simetria da distribuição | 0 = simétrico |
| **Curtose (Kurtosis)** | "Peso" das caudas | 3 = normal |

### 2.2 Código: EDA Univariada

```python
import pandas as pd
from scipy.stats import skew, kurtosis

# Criar um DataFrame de exemplo
dados = pd.DataFrame({
    'Idade': [25, 30, 22, 35, 28, 40, 27, 23, 32, 29],
    'Rendimento': [1800, 2400, 1500, 3100, 2000, 4000, 1900, 1700, 2800, 2200]
})

# Visualizar dados
dados
```

### 2.3 Estatísticas Descritivas

```python
# Estatísticas descritivas básicas
print("Estatísticas descritivas básicas:")
dados.describe()
```

**O que cada métrica significa:**

| Métrica | Descrição |
|---------|-----------|
| `count` | Quantidade de registros |
| `mean` | Média dos valores |
| `std` | Desvio padrão |
| `min` | Valor mínimo |
| `25%` | Primeiro quartil |
| `50%` | Mediana |
| `75%` | Terceiro quartil |
| `max` | Valor máximo |

### 2.4 Assimetria (Skewness)

A assimetria mede se a distribuição é simétrica ou tem uma "cauda" mais longa:

```python
from scipy.stats import skew

print("Coeficiente de assimetria (skewness):")
print(f"Idade: {skew(dados['Idade']):.2f}")
print(f"Rendimento: {skew(dados['Rendimento']):.2f}")
```

**Interpretação:**
- **= 0**: Distribuição simétrica (ideal)
- **> 0**: Cauda à direita (valores altos extremos)
- **< 0**: Cauda à esquerda (valores baixos extremos)

```
Distribuição Simétrica     Assimetria Positiva      Assimetria Negativa
      (skew = 0)              (skew > 0)              (skew < 0)
        
         ▄▄                      ▄                          ▄
        ████                    ██▄                        ▄██
       ██████                  ████▄▄                    ▄▄████
      ████████                ████████▄▄            ▄▄████████
     ──────────              ────────────          ────────────
```

### 2.5 Curtose (Kurtosis)

A curtose mede o "achatamento" da distribuição e o peso das caudas:

```python
from scipy.stats import kurtosis

print("Coeficiente de curtose (kurtosis):")
print(f"Idade: {kurtosis(dados['Idade'], fisher=False):.2f}")
print(f"Rendimento: {kurtosis(dados['Rendimento'], fisher=False):.2f}")

print("\nExcesso de curtose (kurtosis - 3):")
print(f"Idade: {kurtosis(dados['Idade'], fisher=True):.2f}")
print(f"Rendimento: {kurtosis(dados['Rendimento'], fisher=True):.2f}")
```

**Interpretação:**
- **= 3**: Distribuição normal (mesocúrtica)
- **> 3**: Caudas pesadas, pico alto (leptocúrtica)
- **< 3**: Caudas leves, pico baixo (platicúrtica)

---

## 3. Treinamento de Modelo XGBoost (Local)

Agora vamos treinar um modelo XGBoost para prever valores de imóveis.

### 3.1 O que é XGBoost?

**XGBoost** (eXtreme Gradient Boosting) é um algoritmo de Machine Learning que:
- Usa múltiplas "árvores de decisão" em sequência
- Cada árvore corrige os erros da anterior
- É muito utilizado em competições de ML por sua eficiência

### 3.2 Importar Bibliotecas

```python
import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
    r2_score
)
```

### 3.3 Carregar Dataset

Usaremos o dataset **California Housing** que contém informações sobre casas na Califórnia:

```python
# Carregar o conjunto de dados
california = fetch_california_housing()
X = pd.DataFrame(california.data, columns=california.feature_names)
y = pd.Series(california.target, name='MedHouseVal')

print(f"Total de registros: {len(X)}")
print(f"\nColunas disponíveis:")
X.info()
```

**Colunas do dataset:**

| Coluna | Descrição |
|--------|-----------|
| `MedInc` | Renda média do bairro |
| `HouseAge` | Idade média das casas |
| `AveRooms` | Média de quartos por casa |
| `AveBedrms` | Média de quartos de dormir |
| `Population` | População do bairro |
| `AveOccup` | Média de ocupantes por casa |
| `Latitude` | Latitude |
| `Longitude` | Longitude |
| `MedHouseVal` | **Target**: Valor médio das casas (em $100.000) |

### 3.4 Dividir Dados: Treino e Teste

```python
# Divisão treino/teste (80% treino, 20% teste)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Dados de treino: {len(X_train)} registros")
print(f"Dados de teste: {len(X_test)} registros")
```

**Por que dividimos os dados?**
- **Treino**: O modelo aprende com estes dados
- **Teste**: Avaliamos o modelo com dados que ele nunca viu

### 3.5 Configurar e Treinar o Modelo

```python
# Criar modelo XGBoost para regressão
xgb_reg = xgb.XGBRegressor(
    objective="reg:squarederror",  # Problema de regressão
    n_estimators=200,               # Número de árvores
    max_depth=4,                    # Profundidade das árvores
    learning_rate=0.1,              # Taxa de aprendizado
    subsample=0.8,                  # % de dados por árvore
    colsample_bytree=0.8,           # % de features por árvore
    random_state=42
)

# Treinar o modelo
print("Treinando modelo...")
xgb_reg.fit(X_train, y_train)
print("Treinamento concluído!")
```

**Hiperparâmetros explicados:**

| Parâmetro | O que faz | Valor típico |
|-----------|-----------|--------------|
| `n_estimators` | Quantidade de árvores | 100-500 |
| `max_depth` | Profundidade das árvores | 3-10 |
| `learning_rate` | Velocidade de aprendizado | 0.01-0.3 |
| `subsample` | % de dados por iteração | 0.7-1.0 |

### 3.6 Fazer Previsões

```python
# Fazer previsões no conjunto de teste
y_pred = xgb_reg.predict(X_test)

# Ver algumas previsões
print("Comparação: Real vs Previsto")
for i in range(5):
    print(f"Real: {y_test.iloc[i]:.2f} | Previsto: {y_pred[i]:.2f}")
```

### 3.7 Avaliar o Modelo

```python
# Calcular métricas de avaliação
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred) * 100
r2 = r2_score(y_test, y_pred)

print("=" * 40)
print("AVALIAÇÃO DO MODELO XGBOOST")
print("=" * 40)
print(f"MSE  (Erro Quadrático Médio): {mse:.3f}")
print(f"MAE  (Erro Absoluto Médio):   {mae:.3f}")
print(f"MAPE (Erro Percentual):       {mape:.2f}%")
print(f"R²   (Coef. Determinação):    {r2:.3f}")
print("=" * 40)
```

**O que cada métrica significa:**

| Métrica | O que mede | Bom resultado |
|---------|-----------|---------------|
| **MSE** | Erro quadrático médio | Quanto menor, melhor |
| **MAE** | Erro absoluto médio | Quanto menor, melhor |
| **MAPE** | Erro percentual | < 10% é bom |
| **R²** | % da variância explicada | Próximo de 1.0 |

### 3.8 Importância das Variáveis

O XGBoost calcula automaticamente quais variáveis são mais importantes:

```python
# Criar tabela de importância
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": xgb_reg.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("Importância das Variáveis:")
print(feature_importance)
```

### 3.9 Visualizar Importância

```python
# Gráfico de barras horizontais
plt.figure(figsize=(10, 6))
plt.barh(
    feature_importance["Feature"],
    feature_importance["Importance"],
    color='steelblue'
)
plt.gca().invert_yaxis()
plt.xlabel("Importância")
plt.ylabel("Variável")
plt.title("Importância das Variáveis - XGBoost")
plt.tight_layout()
plt.show()
```

---

## 4. Executando o Notebook Completo

Para executar todo o código de uma vez:

1. **No SageMaker Studio**, vá até **JupyterLab**
2. Faça upload do arquivo `scripts/exemplo-treinamento.ipynb`
3. Abra o notebook e execute célula por célula (`Shift + Enter`)

### Estrutura do Notebook `exemplo-treinamento.ipynb`

| Seção | Conteúdo |
|-------|----------|
| 1. EDA Univariada | Estatísticas descritivas, skewness, kurtosis |
| 2. XGBoost Regressão | Carregar dados, treinar modelo, avaliar |

---

## 5. Resumo: Treino Local vs Treino Gerenciado

| Aspecto | Este Módulo (Local) | Próximo Módulo (SageMaker) |
|---------|--------------------|-----------------------------|
| **Execução** | No notebook | Em instâncias dedicadas |
| **Código** | `xgb.XGBRegressor()` | `sagemaker.estimator.Estimator()` |
| **Dados** | Em memória | Upload para S3 |
| **Escala** | Limitada ao notebook | Qualquer tamanho |
| **Custo** | Paga pelo notebook | Paga apenas pelo treino |

---

## 6. Checklist de Validação

- [ ] Entendi os conceitos de assimetria e curtose
- [ ] Executei a EDA univariada
- [ ] Carreguei o dataset California Housing
- [ ] Dividi os dados em treino/teste
- [ ] Treinei o modelo XGBoost
- [ ] Avaliei com métricas (MSE, MAE, R²)
- [ ] Analisei a importância das variáveis

---

## 7. Arquivos de Referência

Os scripts Python originais estão disponíveis para consulta:

- **EDA Univariada**: `scripts/cap2_EDA_univariada.py`
- **XGBoost Regressão**: `scripts/cap9_XGBoost_Boston_regressão.py`
- **Notebook Completo**: `scripts/exemplo-treinamento.ipynb`

---

## Próximo Módulo

Agora que aprendemos a treinar localmente, vamos usar o **SageMaker Training Job** com algoritmos built-in!

➡️ [Módulo 8: Algoritmos Built-in do SageMaker](08-algoritmos-builtin.md)
