# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:27:45 2023

@author: juan.isaza
"""

#banrep

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# URL of the data source
url = 'https://www.datos.gov.co/resource/32sa-8pi3.json'

#path

desktopPath="D:\\Users\\juan.isaza\\OneDrive - SURA INVESTMENT MANAGEMENT S.A\\Escritorio\\"

# Making a GET request to the URL
response = requests.get(url,verify=False)

# Checking the status code of the response
if response.status_code == 200:
    
    data = response.json()
    df = pd.DataFrame(data)
    df["fecha"]=pd.to_datetime(df["vigenciadesde"])
    df["valor"]=df["valor"].astype(float)
    df=df.sort_values(by="fecha")
    
    
    print(df.head(10))
else:
    # Printing an error message if the status code is not 200
    print(f'Request failed with status code {response.status_code}')
    
# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['fecha'].iloc[-180:], df['valor'].iloc[-180:], label='Valor')
plt.title('TRM Historica')
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.legend()

# Save the plot as PNG on the desktop
plt.savefig(os.path.join(desktopPath, 'grafico1.png'))
plt.close()  # Close the plot to free up resources

# Calculate statistics
statistics_df = pd.DataFrame(columns=['Starting Date', 'Ending Date', 'Min', '25%', '50%', '75%', 'Max', 'Value at Risk (95%)', 'Standard Deviation', 'Cumulative Return'])

# Descriptive statistics
descriptive_stats = df['valor'].describe(percentiles=[.25, .50, .75])
statistics_df.loc[0, 'Fecha de Inicio'] = df['fecha'].iloc[0]
statistics_df.loc[0, 'Fecha de Fin'] = df['fecha'].iloc[-1]
statistics_df.loc[0, 'Mínimo'] = descriptive_stats['min']
statistics_df.loc[0, '25%'] = descriptive_stats['25%']
statistics_df.loc[0, '50%'] = descriptive_stats['50%']
statistics_df.loc[0, '75%'] = descriptive_stats['75%']
statistics_df.loc[0, 'Máximo'] = descriptive_stats['max']
# Additional statistics
statistics_df.loc[0, 'Value at Risk (95%)'] = float(df['valor'].pct_change().quantile(0.05))
statistics_df.loc[0, 'Desviación Estándar'] = float(df['valor'].pct_change().std())
statistics_df.loc[0, 'Rendimiento Acumulado'] = float((df['valor'].iloc[-1] / df['valor'].iloc[0] - 1) * 100)





statistics_path = os.path.join(desktopPath, 'valor_statistics.xlsx')
statistics_df.to_excel(statistics_path, index=False)




# Save analysis in a text file
analysis_path = os.path.join(desktopPath, 'valor_analysis.txt')
with open(analysis_path, 'w') as f:
    f.write("Análisis de la variable DOLAR:\n\n")
    f.write(f"Fecha de inicio: {statistics_df.iloc[0]['Fecha de Inicio']}\n")
    f.write(f"Fecha de fin: {statistics_df.iloc[0]['Fecha de Fin']}\n")
    f.write(f"Mínimo: {statistics_df.iloc[0]['Mínimo']}\n")
    f.write(f"25%: {statistics_df.iloc[0]['25%']}\n")
    f.write(f"50%: {statistics_df.iloc[0]['50%']}\n")
    f.write(f"75%: {statistics_df.iloc[0]['75%']}\n")
    f.write(f"Máximo: {statistics_df.iloc[0]['Máximo']}\n")
    f.write(f"Value at Risk (95%): {statistics_df.iloc[0]['Value at Risk (95%)']}\n")
    f.write(f"Desviación Estándar: {statistics_df.iloc[0]['Desviación Estándar']}\n")
    f.write(f"Rendimiento Acumulado: {statistics_df.iloc[0]['Rendimiento Acumulado']}\n\n")
    
    # Commentary/Opinion
    f.write("Opinión:\n")
    f.write("El comportamiento de la variable DOLAR durante el período analizado presenta los siguientes aspectos destacados:\n")
    
    if statistics_df.iloc[0]['Rendimiento Acumulado'] > 0:
        f.write("El valor acumulado ha experimentado un crecimiento positivo, lo que indica un rendimiento positivo en el periodo.\n")
    elif statistics_df.iloc[0]['Rendimiento Acumulado'] < 0:
        f.write("El valor acumulado ha experimentado una disminución, lo que indica un rendimiento negativo en el periodo.\n")
    else:
        f.write("El valor acumulado se ha mantenido estable durante el periodo analizado.\n")
    
    if statistics_df.iloc[0]['Desviación Estándar'] > 0:
        f.write("La desviación estándar muestra que la variable DOLAR ha experimentado cierta volatilidad durante el periodo.\n")
    else:
        f.write("La desviación estándar es cero, lo que indica que la variable DOLAR ha mantenido una constante durante el periodo.\n")






print(f"Plot saved")
print(f"Statistics saved at: {statistics_path}")