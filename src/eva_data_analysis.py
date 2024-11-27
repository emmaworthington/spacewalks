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
    print('Saving to CSV file {}'.format(output_file))
    df.to_csv(output_file, index=False)


def text_to_duration(duration):
    """
    Convert text in hours:minutes:seconds to
    duration in hours.
    """

    hours, minutes = duration.split(':')
    duration_hours = int(hours) + int(minutes) / 6

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

    print('-- START --')
    # https://data.nasa.gov/resource/eva.json (with modifications)
    input_file = open('data/eva-data.json', 'r')
    output_file = open('output/eva-data.csv', 'w')
    graph_file = 'figures/cumulative_eva_graph.png'

    eva_df = read_json_to_dataframe(input_file)

    write_dataframe_to_csv(eva_df, output_file)

    plot_cumulative_time_in_space(eva_df, graph_file)
