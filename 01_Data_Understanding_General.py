import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
from io import BytesIO

# Daten laden
print("STATUS 01: Daten werden aus CSV-Datei geladen ...")
data = pd.read_csv('/Users/tobi/Documents/Ablage/Dawa_Project_Ablage/Shopping_Daten.csv')

print("STATUS 02: Daten werden analysiert ...")
# Berechnen des Gesamtumsatzes für jede Transaktion
data['Total_Sales'] = data['Quantity'] * data['Avg_Price']

# Gesamtumsatz pro Monat
data['Transaction_Month'] = pd.to_datetime(data['Transaction_Date']).dt.to_period('M')
monthly_sales = data.groupby('Transaction_Month')['Total_Sales'].sum()

# Beliebte Produktgruppen
product_sales = data.groupby('Product_Category').agg({'Quantity': 'sum', 'Total_Sales': 'sum'})

# Geschlechterverteilung
gender_distribution = data['Gender'].value_counts()

# Excel-Datei erstellen
excel_path = '/Users/tobi/Documents/Ablage/Dawa_Project_Ablage/Analyse_DataUnderstanding.xlsx'
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

# Funktion zum Speichern von Grafiken als Bytes
def save_fig_to_bytes(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)  # Schließen der Figur, um Ressourcen freizugeben
    buffer.seek(0)
    return buffer

print("STATUS 03: Grafiken werden erstellt ...")
# Grafiken erstellen 
# Monatlicher Gesamtumsatz
fig, ax = plt.subplots(figsize=(12, 6))
monthly_sales.plot(kind='bar', ax=ax)
ax.set_title('Gesamtumsatz pro Monat')
ax.set_ylabel('Umsatz')
ax.set_xlabel('Monat')
monthly_sales_fig = save_fig_to_bytes(fig)

# Verkaufszahlen und Umsatz pro Produktkategorie
fig, axes = plt.subplots(2, 1, figsize=(15, 10))
product_sales['Quantity'].sort_values().plot(kind='barh', ax=axes[0], title='Verkaufszahlen pro Produktkategorie')
product_sales['Total_Sales'].sort_values().plot(kind='barh', ax=axes[1], title='Umsatz pro Produktkategorie')
product_sales_fig = save_fig_to_bytes(fig)

# Geschlechterverteilung
fig, ax = plt.subplots(figsize=(8, 6))
gender_distribution.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, labels=gender_distribution.index)
ax.set_title('Geschlechterverteilung')
ax.set_ylabel('')
gender_distribution_fig = save_fig_to_bytes(fig)

print("STATUS 04: Excel_Datei wird erstellt und Ergebnisse eingefügt...")
# Basisdaten in Excel-Datei einfügen
data.head().to_excel(writer, sheet_name='First Five Rows')
data.describe().to_excel(writer, sheet_name='Data Description')
data.isnull().sum().to_frame('Missing Values').to_excel(writer, sheet_name='Missing Data')

# Grafiken in Excel-Datei einfügen
workbook = writer.book
worksheet1 = workbook.add_worksheet('Monthly Sales')
worksheet1.insert_image('B2', 'monthly_sales.png', {'image_data': monthly_sales_fig})
worksheet2 = workbook.add_worksheet('Product Sales')
worksheet2.insert_image('B2', 'product_sales.png', {'image_data': product_sales_fig})
worksheet3 = workbook.add_worksheet('Gender Distribution')
worksheet3.insert_image('B2', 'gender_distribution.png', {'image_data': gender_distribution_fig})

# Writer schließen und die Datei speichern
writer.close()
print("STATUS 05: Der Vorgang ist nun abgeschlossen.")
