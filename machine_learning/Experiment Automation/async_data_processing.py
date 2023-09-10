from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
from PyNomaly import loop
from matplotlib import pyplot as plt
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import os
import pandas as pd
from pathlib import Path


V_TO_MV = 1000
V_TO_GRAM = -25000
lop_score_threshold = 0.2


def main():  # sourcery skip: remove-redundant-slice-index
    plt.ion()
    unfiltered_df = get_multiIndex(
        Path(
            r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Automated Data"
        )
    )

    # Initilize empty filtered_df with correct indexing, no data
    filtered_df = pd.DataFrame(index=unfiltered_df.index, columns=unfiltered_df.columns)

    print(unfiltered_df.loc[("T2"), "trial_data"][0:6][2])

    trim_start, trim_end = plot_first_five(unfiltered_df)

    print(unfiltered_df.loc[("T2"), "trial_data"][0:6][2])

    data_to_apply = unfiltered_df.loc[("T2"), "trial_data"][0:6].apply(
        lambda df: filter_data(df)
    )

    print(data_to_apply)
    # filtered_df.loc[("T2"), "trial_data"][0:6] = data_to_apply

    # # Compare to first printed DataFrame
    # print(filtered_df.loc[("T2"), "trial_data"][0])

    # # # TODO: Use async programming here


def get_multiIndex(folder: Path) -> pd.DataFrame:
    """Put data into MultiIndex DataFrame"""

    trials: list[pd.DataFrame] = []
    multiindex_tuples: list[tuple[str, str]] = []

    for file in os.listdir(folder):
        temperature, trial_index = get_index(
            Path(os.path.join(folder, file))
        )  # parse MultiIndex labels
        trial = pd.read_csv(os.path.join(folder, file))  # Read data
        trial.drop(
            trial.columns[2], axis="columns", inplace=True
        )  # drop second time index
        trial.iloc[:, 2] = trial.iloc[:, 2] * V_TO_GRAM
        trial.iloc[:, 1] = trial.iloc[:, 1] * V_TO_MV
        trial.columns = ["Time (s)", "Response (mV)", "Load (g)"]
        trials.append(trial)
        multiindex_tuples.append((temperature, trial_index))

    multiindex = pd.MultiIndex.from_tuples(
        multiindex_tuples, names=["Temperature", "Experiment"]
    )
    unfiltered_data = pd.DataFrame({"trial_data": trials}, index=multiindex)
    return unfiltered_data


def trim_data(df: pd.DataFrame, trim_start: int, trim_end: int) -> pd.DataFrame:
    """Filters input DataFrame for noise using LOP. Returns filtered DataFrame."""
    trimmed_df = df.iloc[trim_start : (len(df) - trim_end)]
    return trimmed_df


def filter_and_trim_data(
    unfiltered_df: pd.DataFrame, trim_start: int, trim_end: int
) -> pd.DataFrame:
    """Filters input DataFrame for noise using LOP. Returns filtered DataFrame."""
    unfiltered_df = unfiltered_df.iloc[trim_start : (len(unfiltered_df) - trim_end)]
    m = loop.LocalOutlierProbability(
        unfiltered_df.drop(columns="Load (g)"), extent=1, n_neighbors=20
    ).fit()  # Used to find scores
    scores = (
        m.local_outlier_probabilities
    )  # this is an attribute after performing LocalOutlierProbability()
    unfiltered_df["scores"] = scores.tolist()  # Adding scores column to lop_df
    unfiltered_df.loc["Time (s)"] = unfiltered_df["Time (s)"].sub(
        unfiltered_df["Time (s)"].iloc[0]
    )
    unfiltered_df.set_index(keys="Time (s)", inplace=True)
    return unfiltered_df.query(f"scores < {lop_score_threshold}")


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters input DataFrame for noise using LOP. Returns filtered DataFrame."""

    df.fillna(0, inplace=True)
    m = loop.LocalOutlierProbability(
        df.drop(columns="Load (g)"), extent=1, n_neighbors=20
    ).fit()  # Used to find scores
    scores = (
        m.local_outlier_probabilities
    )  # this is an attribute after performing LocalOutlierProbability()
    df_copy = df.copy()
    df_copy["scores"] = scores.tolist()  # Adding scores column to lop_df
    # df.loc["Time (s)"] = df["Time (s)"].sub(df["Time (s)"].iloc[0])
    return df_copy.query(f"scores < {lop_score_threshold}")


def plot_first_five(df):
    fig, ax = plt.subplots()

    # Filter data
    first_five_filtered = df.loc[("T2"), "trial_data"][:6].apply(
        lambda df: filter_data(df)
    )

    # Plot initial filtered untrimmed
    first_five_filtered.apply(lambda df: plot_temp(df=df, ax=ax, color="red"))

    # Trim data initial parameters, not yet modifiying data through trimming
    trim_start, trim_end = (
        input("Enter trim start and trim end values as tuple  as start, end: ")
        .replace(",", "")
        .split()
    )
    trim_start, trim_end = int(trim_start), int(trim_end)

    # Plot trimmed and filtered data
    first_five_filtered_trimmed = first_five_filtered.apply(
        lambda df: trim_data(df=df, trim_start=trim_start, trim_end=trim_end)
    )
    first_five_filtered_trimmed.apply(lambda df: plot_temp(df=df, ax=ax, color="blue"))
    fig.show()

    while hash(input("Satisfied? Y, otherwise press anything: ")) != hash("Y"):
        trim_start, trim_end = (
            input("Enter trim start and trim end values as tuple  as start, end: ")
            .replace(",", "")
            .split()
        )

        ax.clear()
        trim_start, trim_end = int(trim_start), int(trim_end)
        first_five_filtered.apply(lambda df: plot_temp(df=df, ax=ax, color="red"))
        first_five_filtered.apply(lambda df: trim_data(df=df, trim_start=trim_start, trim_end=trim_end)).apply(lambda df: plot_temp(df=df, ax=ax, color="blue"))  # type: ignore
        fig.show()

    return trim_start, trim_end
    # access_data(df, "T1", start_trial_no=1, end_trial__no=5).apply(trim_data(unfiltered_df = df, trim_start=start, trim_end=end)).apply(lambda df: plot_temp(df=df, ax=ax))

    ## TODO plot ax.scatter first five first, filtered and TRIMMED
    # access_data(df, "T1", start_trial_no=start, end_trial__no=end)


def plot_temp(df, ax, color: str, size=0.2):
    ax.set_ylabel("Response (mV)", fontsize=13)  # a figure with a single Axes
    ax.set_xlabel("Time (s)", fontsize=13)
    ax.set_title("Response vs. Time", fontsize=13)
    ax.scatter(df.index, df["Response (mV)"], c=color, s=size)


def get_index(filepath: Path) -> tuple[str, str]:
    """Parse trial filenames and get the temperature and trial."""
    temperature = filepath.stem[:2]
    trial_index = filepath.stem[2:]
    return temperature, trial_index


if __name__ == "__main__":
    main()
