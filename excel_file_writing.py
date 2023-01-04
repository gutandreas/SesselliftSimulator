import pandas as pd
from pandas import DataFrame

# read text file into pandas DataFrame and
# create header
df = pd.read_csv("report.txt", sep=": ", skiprows=[0, 1, 2], header=None)
titels = []
for index, row in df.iterrows():
    if not row[0] in titels:
        titels.append(row[0])
        print(row[0])
del df[0]

dataframes = []

for i in range(len(titels)):
    current_df = DataFrame(df[df.index % len(titels) == i])
    current_df = current_df.reset_index()
    del current_df['index']
    dataframes.append(current_df)
    df.add(current_df)

df = DataFrame()

for i in range(len(titels)):
    df.insert(i, titels[i], dataframes[i])

df = df.astype({titels[2]:'int'})
df = df.astype({titels[3]:'int'})
df = df.astype({titels[4]:'float'})
df = df.astype({titels[5]:'float'})
df = df.astype({titels[6]:'float'})
df = df.astype({titels[7]:'float'})

print(df)


writer = pd.ExcelWriter('Daten_Sessellist_Simulator.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Simulationsdaten')

workbook = writer.book
worksheet = writer.sheets['Simulationsdaten']

# Create a chart object.
chart_transported_skiers = workbook.add_chart({'type': 'line'})
chart_transported_skiers.set_x_axis({'name': titels[1], 'num_font':  {'rotation': 90}})

chart_skiers_in_queue = workbook.add_chart({'type': 'line'})
chart_skiers_in_queue.set_x_axis({'name': titels[1], 'num_font':  {'rotation': 90}})

chart_utilisation = workbook.add_chart({'type': 'line'})
chart_utilisation.set_x_axis({'name': titels[1], 'num_font':  {'rotation': 90}})



# Get the dimensions of the dataframe.
(max_row, max_col) = df.shape

# Configure the series of the chart from the dataframe data.
chart_transported_skiers.add_series({'name': titels[2], 'categories': ['Simulationsdaten', 1, 2, max_row, 2],
                                     'values': ['Simulationsdaten', 1, 3, max_row, 3]})
chart_skiers_in_queue.add_series({'name': titels[3], 'categories': ['Simulationsdaten', 1, 2, max_row, 2],
                                  'values': ['Simulationsdaten', 1, 4, max_row, 4],
                                  'line': {'color': '#ff0000'}})

chart_utilisation.add_series({'name': titels[4], 'categories': ['Simulationsdaten', 1, 2, max_row, 2],
                                  'values': ['Simulationsdaten', 1, 5, max_row, 5],
                                  'line': {'color': '#000000'}})
chart_utilisation.add_series({'name': titels[5], 'categories': ['Simulationsdaten', 1, 2, max_row, 2],
                                  'values': ['Simulationsdaten', 1, 6, max_row, 6],
                                  'line': {'color': '#aaaaff'}})

# Insert the chart into the worksheet.
worksheet.insert_chart(0, max_col + 2, chart_transported_skiers)
worksheet.insert_chart(16, max_col + 2, chart_skiers_in_queue)
worksheet.insert_chart(32, max_col + 2, chart_utilisation)

writer.close()
