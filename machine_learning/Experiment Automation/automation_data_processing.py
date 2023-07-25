from pathlib import Path
import pandas as pd


def main():
    
    directory = Path(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Raw Temperature Data")
    data = get_data(list(directory.iterdir()))
    



def get_data(files: list[Path]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get data"""
    loads: list[pd.DataFrame] = []
    responses: list[pd.DataFrame] = []
    multiindex: list[tuple[int, int]] = []

    for file in files:
        temperature_index, trial_index = get_index(file)
        trial = pd.read_csv(file)
        load = trial  # TODO: Get just the load values and associated times
        response = trial  # TODO: Get just the responses and associated times
        loads.append(load)
        responses.append(response)
        multiindex.append((temperature_index, trial_index))

    index_names = ["temperature", "trial"]
    all_loads = pd.concat(loads).set_index(pd.MultiIndex.from_tuples(multiindex, names=index_names))
    all_responses = pd.concat(responses).set_index(pd.MultiIndex.from_tuples(multiindex, names=index_names))
    return all_loads, all_responses




def get_index(file: Path) -> tuple[int, int]:
    """Parse trial filenames and get the temperature and trial."""
    temperatures = {"T1": 23, "T2": 30, "T3": 40}
    temperature_index = temperatures[file.name.strip('.csv').split('_')[0]]
    trial_index = int(file.name.strip('.csv').split('_')[1][1:])
    return temperature_index, trial_index




if __name__ == "__main__":
    main()