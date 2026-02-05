# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 17:47:15 2025

@author: jcaia
"""

import pandas as pd

# Criar um DataFrame de exemplo
dados = pd.DataFrame({
    'Idade': [25, 30, 22, 35, 28, 40, 27, 23, 32, 29],
    'Rendimento': [1800, 2400, 1500, 3100, 2000, 4000, 1900, 1700, 2800, 2200]
})

# Estatísticas descritivas básicas
print("Estatísticas descritivas básicas:")
print(dados.describe())

# Calcular estatísticas de assimetria e achatamento
from scipy.stats import skew, kurtosis

print("\nCoeficiente de assimetria (skewness):")
print(f"Idade: {skew(dados['Idade']):.2f}")
print(f"Rendimento: {skew(dados['Rendimento']):.2f}")

print("\nCoeficiente de achatamento (kurtosis):")
print(f"Idade: {kurtosis(dados['Idade'], fisher=False):.2f}")
print(f"Rendimento: {kurtosis(dados['Rendimento'], fisher=False):.2f}")

print("\nExcesso de kurtosis (kurtosis-3):")
print(f"Idade: {kurtosis(dados['Idade'], fisher=True):.2f}")
print(f"Rendimento: {kurtosis(dados['Rendimento'], fisher=True):.2f}")
