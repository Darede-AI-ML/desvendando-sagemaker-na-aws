# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:28:18 2026

@author: jcaia
"""

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

# Carregar o conjunto de dados de habitação da Califórnia
california = fetch_california_housing()
X = pd.DataFrame(california.data, columns=california.feature_names)
y = pd.Series(california.target, name='MedHouseVal')
print(X.info())

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Modelo XGBoost para regressão
xgb_reg = xgb.XGBRegressor(
    objective="reg:squarederror",
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Treino
xgb_reg.fit(X_train, y_train)

# Previsões
y_pred = xgb_reg.predict(X_test)

# Avaliação do desempenho
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred) * 100
r2 = r2_score(y_test, y_pred)

print("Avaliação do Modelo XGBoost (Regressão)")
print(f"MSE : {mse:.3f}")
print(f"MAE : {mae:.3f}")
print(f"MAPE: {mape:.2f}%")
print(f"R²  : {r2:.3f}")

# Criar tabela de importância das variáveis
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": xgb_reg.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nImportância das Variáveis:")
print(feature_importance)

# Gráfico das features mais importantes
plt.figure(figsize=(8, 6))
plt.barh(
    feature_importance["Feature"],
    feature_importance["Importance"]
)
plt.gca().invert_yaxis()
plt.xlabel("Importância")
plt.ylabel("Variável")
plt.title("Importância das variáveis: XGBoost")
plt.show()

