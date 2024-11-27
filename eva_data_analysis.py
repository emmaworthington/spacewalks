import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('eva-data.json', 'r')
output_file = open('eva-data.csv','w')
graph_file = './cumulative_eva_graph.png'

fieldnames = ("EVA #", "Country", "Crew    ", "Vehicle", "Date", "Duration", "Purpose")

eva_df = pd.read_json(input_file, convert_dates=['date'])
eva_df['eva'] = eva_df['eva'].astype(float)
eva_df.dropna(axis=0, inplace=True)
eva_df.sort_values('date', inplace=True)

# Convert duration to hours instead of hours/minutes/seconds
eva_df['duration_hours'] = eva_df['duration'].str.split(':').apply(lambda x: int(x[0]) + int(x[1]) / 60)

# Calculate cumulative sum of hours
eva_df['cumulative_hours'] = eva_df['duration_hours'].cumsum()

eva_df.to_csv(output_file, index=False)

plt.plot(eva_df['date'], eva_df['cumulative_hours'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
