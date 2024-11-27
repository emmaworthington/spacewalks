import matplotlib.pyplot as plt
import pandas as pd

def read_json_to_dataframe(input_file):
    """
    Load data from JSON into a pandas dataframe,
    clean the data by removing incomplete rows and
    sort by date.

    Args:
        input_file (str): The path to the JSON file.

    Returns:
        eva_df (pd.DataFrame): The cleaned and sorted data as a dataframe.
    """

    eva_df = pd.read_json(input_file, convert_dates=['date'])
    eva_df['eva'] = eva_df['eva'].astype(float)
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values('date', inplace=True)

    return eva_df

def write_dataframe_to_csv(df, output_file):
    """
    Write the pandas dataframe to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe to write to CSV
        output_file (str): The path to the CSV file to save.
    """

    # Output data to spreadsheet for further analysis
    df.to_csv(output_file, index=False)

# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('eva-data.json', 'r')
output_file = open('eva-data.csv', 'w')
graph_file = './cumulative_eva_graph.png'

eva_df = read_json_to_dataframe(input_file)

# Convert duration to hours instead of hours/minutes/seconds
eva_df['duration_hours'] = eva_df['duration'].str.split(':').apply(lambda x: int(x[0]) + int(x[1]) / 60)

# Calculate cumulative sum of hours
eva_df['cumulative_hours'] = eva_df['duration_hours'].cumsum()

write_dataframe_to_csv(eva_df, output_file)

# Plot cumulative hours with time
plt.plot(eva_df['date'], eva_df['cumulative_hours'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
