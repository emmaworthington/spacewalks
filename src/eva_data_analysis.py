import matplotlib.pyplot as plt
import pandas as pd
import sys
import re
import numpy as np


def main(input_file, output_file, graph_file):
    print("--START--")

    eva_data = read_json_to_dataframe(input_file)

    eva_data = add_crew_size_column(eva_data) # added this line

    write_dataframe_to_csv(eva_data, output_file)

    plot_cumulative_time_in_space(eva_data, graph_file)

    print("--END--")


def calculate_crew_size(crew):
    """
    Calculate the size of the crew for a single crew entry

    Args:
        crew (str): The text entry in the crew column containing a list of crew member names

    Returns:
        int: The crew size
    """
    
    names = re.split(r';', crew)
    crew_size = 0

    for i in np.arange(len(names)):

        if len(names[i]) > 0:
            crew_size = crew_size + 1

    return crew_size


def add_crew_size_column(df):
    """
    Add crew_size column to the dataset containing the value of the crew size

    Args:
        df (pd.DataFrame): The input data frame.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy


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
    print('Saving to CSV file {}'.format(output_file))
    df.to_csv(output_file, index=False)


def text_to_duration(duration):
    """
    Convert text in HH:MM format to
    duration in hours.
    """

    hours, minutes = duration.split(':')
    duration_hours = int(hours) + int(minutes) / 60

    return duration_hours


def add_duration_hours_variable(df):

    df_copy = df.copy()
    df_copy['duration_hours'] = df_copy['duration'].apply(text_to_duration)

    return df_copy


def plot_cumulative_time_in_space(df, graph_file):
    """
    Plot cumulative hours in space.
    """

    print('Plotting cumulative spacewalk duration and saving to {}'.format(graph_file))

    df = add_duration_hours_variable(df)

    # Calculate cumulative sum of hours
    df['cumulative_hours'] = df['duration_hours'].cumsum()

    plt.figure()
    plt.plot(df['date'], df['cumulative_hours'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


if __name__ == "__main__":

    if len(sys.argv) < 3:
        input_file = 'data/eva-data.json'
        output_file = 'results/eva-data.csv'
        print(f'Using default input and output filenames')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('Using custom input and output filenames')

    graph_file = 'results/cumulative_eva_graph.png'
    main(input_file, output_file, graph_file)
