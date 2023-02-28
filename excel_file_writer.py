import pandas as pd
from pandas import DataFrame



file = open('report.txt', 'r')
lines = file.readlines()
title = lines[0]
informations = lines[1]

print(title)
print(informations)

# read text file into pandas DataFrame and
# create header
df = pd.read_csv("report.txt", sep=": ", skiprows=[0, 1, 2], header=None, encoding='unicode_escape', engine='python')
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

df = df.astype({titels[2]: 'int'})
df = df.astype({titels[3]: 'int'})
df = df.astype({titels[4]: 'float'})
df = df.astype({titels[5]: 'float'})
df = df.astype({titels[6]: 'float'})
df = df.astype({titels[7]: 'float'})
df = df.astype({titels[8]: 'float'})
df = df.astype({titels[9]: 'int'})
df = df.astype({titels[10]: 'int'})

print(df)

writer = pd.ExcelWriter('Daten_Sessellist_Simulator.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Simulationsdaten', startrow=2)

workbook = writer.book
worksheet = writer.sheets['Simulationsdaten']

format_title = workbook.add_format()
format_title.set_bold()
format_title.set_size(20)

format_informations = workbook.add_format()
format_informations.set_size(20)

worksheet.write("A1", title, format_title)
worksheet.write("A2", informations, format_informations)

x_zoom_factor = 1.5

# Create a chart object.
chart_transported_skiers = workbook.add_chart({'type': 'line'})
chart_transported_skiers.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})
chart_transported_skiers.set_size({'x_scale': x_zoom_factor})

chart_skiers_in_queue = workbook.add_chart({'type': 'line'})
chart_skiers_in_queue.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})
chart_skiers_in_queue.set_title({'name': 'Skifahrer in Warteschlange'})
chart_skiers_in_queue.set_size({'x_scale': x_zoom_factor})

chart_skiers_in_queue_duration = workbook.add_chart({'type': 'line'})
chart_skiers_in_queue_duration.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})

chart_utilisation = workbook.add_chart({'type': 'line'})
chart_utilisation.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})
chart_utilisation.set_title({'name': 'Liftauslastung'})
chart_utilisation.set_size({'x_scale': x_zoom_factor})

chart_capacity_vs_demand = workbook.add_chart({'type': 'line'})
chart_capacity_vs_demand.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})
chart_capacity_vs_demand.set_title({'name': 'Differenz Nachfrage/Kapazität'})
chart_capacity_vs_demand.set_size({'x_scale': x_zoom_factor})

chart_skiers_per_hour = workbook.add_chart({'type': 'line'})
chart_skiers_per_hour.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})
chart_skiers_per_hour.set_title({'name': 'Skifahrer pro Stunde'})
chart_skiers_per_hour.set_size({'x_scale': x_zoom_factor})

chart_lost_skier = workbook.add_chart({'type': 'line'})
chart_lost_skier.set_x_axis({'name': titels[1], 'num_font': {'rotation': 90}})
chart_lost_skier.set_size({'x_scale': x_zoom_factor})

# Get the dimensions of the dataframe.
(max_row, max_col) = df.shape

widths = [8, 18, 19, 21, 17, 21, 22, 18, 21, 21, 18]

for i in range(len(widths)):
    worksheet.set_column(i + 1, i + 1, widths[i])

worksheet.add_table(2, 1, max_row + 2, max_col, {'header_row': 0})

# Configure the series of the chart from the dataframe data.
chart_transported_skiers.add_series({'name': titels[2], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                                     'values': ['Simulationsdaten', 1, 3, max_row, 3]})

chart_skiers_in_queue.add_series({'name': titels[3], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                                  'values': ['Simulationsdaten', 1, 4, max_row, 4],
                                  'line': {'color': '#a8323c'}})
chart_skiers_in_queue_duration.add_series({'name': titels[4], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                                           'values': ['Simulationsdaten', 1, 5, max_row, 5],
                                           'line': {'color': '#690812'}, 'y2_axis': True})
chart_skiers_in_queue.combine(chart_skiers_in_queue_duration)

chart_utilisation.add_series({'name': titels[5], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                              'values': ['Simulationsdaten', 1, 6, max_row, 6],
                              'line': {'color': '#000000'}})
chart_utilisation.add_series({'name': titels[6], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                              'values': ['Simulationsdaten', 1, 7, max_row, 7],
                              'line': {'color': '#6788b5'}})

chart_capacity_vs_demand.add_series({'name': titels[7], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                                     'values': ['Simulationsdaten', 1, 8, max_row, 8],
                                     'line': {'color': '#000000'}})

chart_skiers_per_hour.add_series({'name': titels[8], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                                  'values': ['Simulationsdaten', 1, 9, max_row, 9],
                                  'line': {'color': '#109910'}})
chart_skiers_per_hour.add_series({'name': titels[9], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                                  'values': ['Simulationsdaten', 1, 10, max_row, 10],
                                  'line': {'color': '#bbbbbb'}})

chart_lost_skier.add_series({'name': titels[10], 'categories': ['Simulationsdaten', 3, 2, max_row + 2, 2],
                             'values': ['Simulationsdaten', 1, 11, max_row, 11],
                             'line': {'color': '#ff5555'}})

# Insert the chart into the worksheet.
worksheet.insert_chart(2, max_col + 2, chart_transported_skiers)
worksheet.insert_chart(18, max_col + 2, chart_skiers_in_queue)
worksheet.insert_chart(34, max_col + 2, chart_utilisation)
worksheet.insert_chart(50, max_col + 2, chart_capacity_vs_demand)
worksheet.insert_chart(66, max_col + 2, chart_skiers_per_hour)
worksheet.insert_chart(82, max_col + 2, chart_lost_skier)

writer.close()
