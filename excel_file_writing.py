import pandas as pd
from pandas import DataFrame

# read text file into pandas DataFrame and
# create header
df = pd.read_csv("report.txt", sep=": ", skiprows=[0, 1, 2], header=None)
titels = []
for index, row in df.iterrows():
    if not row[0] in titels:
        titels.append(row[0])
del df[0]

dataframes = []

for i in range(4):
    current_df = DataFrame(df[df.index % 4 == i])
    current_df = current_df.reset_index()
    del current_df['index']
    dataframes.append(current_df)
    df.add(current_df)

df = DataFrame()

for i in range(4):
    df.insert(i, titels[i], dataframes[i])

df = df.astype({titels[2]:'int'})
df = df.astype({titels[3]:'int'})

print(df)


writer = pd.ExcelWriter('Daten_Sessellist_Simulator.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Simulationsdaten')

workbook = writer.book
worksheet = writer.sheets['Simulationsdaten']

# Create a chart object.
chart = workbook.add_chart({'type': 'column'})

# Get the dimensions of the dataframe.
(max_row, max_col) = df.shape

# Configure the series of the chart from the dataframe data.
chart.add_series({'name': titels[2], 'values': ['Simulationsdaten', 0, 3, max_row, 3]})
chart.add_series({'name': titels[3], 'values': ['Simulationsdaten', 0, 4, max_row, 4]})

# Insert the chart into the worksheet.
worksheet.insert_chart(max_row+3, 0, chart)

writer.close()
