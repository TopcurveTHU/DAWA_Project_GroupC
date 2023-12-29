import pandas as pd
import numpy as np

# Daten laden
data = pd.read_csv('/Users/tobi/Documents/Ablage/Dawa_Project_Ablage/Shopping_Daten.csv') # PFAD ÄNDERN

# Berechnen des Gesamtumsatzes für jede Transaktion
# Annahme: Die Spalte 'Quantity' und 'Avg_Price' existieren, um den Gesamtumsatz zu berechnen
if 'Quantity' in data.columns and 'Avg_Price' in data.columns:
    data['Total_Sales'] = data['Quantity'] * data['Avg_Price']

# Fehlende Werte behandeln
for column in data.columns:
    if data[column].dtype == 'object':  # Kategoriale Daten
        data[column].fillna(data[column].mode()[0], inplace=True)
    elif pd.api.types.is_numeric_dtype(data[column]):  # Numerische Daten
        data[column].fillna(data[column].median(), inplace=True)

# Ausreißer identifizieren und behandeln
numerical_columns = data.select_dtypes(include=[np.number]).columns
for column in numerical_columns:
    upper_limit = data[column].mean() + 3 * data[column].std()
    lower_limit = data[column].mean() - 3 * data[column].std()
    data[column] = np.where(
        (data[column] > upper_limit) | (data[column] < lower_limit),
        np.nan,  # Setze Ausreißer auf NaN
        data[column]
    )
# Ersetze NaN, die durch Ausreißer entstanden sind, durch den Median
data[numerical_columns] = data[numerical_columns].apply(lambda x: x.fillna(x.median()))

# Kodierung kategorialer Variablen
data = pd.get_dummies(data, drop_first=True)

# Neue Merkmale erstellen
if 'CustomerID' in data.columns and 'Total_Sales' in data.columns:
    customer_total_sales = data.groupby('CustomerID')['Total_Sales'].sum().rename('Customer_Total_Sales')
    data = data.merge(customer_total_sales, on='CustomerID', how='left')

# Daten für Analyse speichern
cleaned_file_path = '/Users/tobi/Documents/Ablage/Dawa_Project_Ablage/Shopping_Daten_Cleaned.csv' # PFAD ÄNDERN
data.to_csv(cleaned_file_path, index=False)

print(f"Data preparation is complete. The cleaned data is saved to {cleaned_file_path}.")
