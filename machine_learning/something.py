# %% [markdown]
# # Function Definitions

# %%
from datetime import datetime
from pathlib import Path
import pandas as pd 
import matplotlib
import os 
import matplotlib.pyplot as plt
import numpy as np
from math import factorial
from PyNomaly import loop
    



def main():
    # %% [markdown]
    # # One graph: all trials - noisy (response vs. time) saves graph .jpg automatically

    # %%
    # #############################################################################! Trim and display all data (voltage vs. time) ##########################################################################################################
    


    directory = Path(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Raw Temperature Data")

    fig, ax = plt.subplots()
    ax.set_ylabel('Response (mV)', fontsize = 13)  # a figure with a single Axes
    ax.set_xlabel('Time (s)', fontsize = 13)
    ax.set_title('ATBC P4 PVC Gel Temperature Response (Unfiltered)', fontsize = 13)

    data = get_data(list(directory.iterdir()))

    for csv_file in os.listdir(directory):
        if csv_file[1] == '1':
            trimmed_df = trim_data(csv_file)
            ax.scatter(trimmed_df['Relative Time'], trimmed_df['Response (mV)'], c = 'lightsalmon', s=.2)
            
        elif csv_file[1] == '2':
            trimmed_df = trim_data(csv_file)
            ax.scatter(trimmed_df['Relative Time'], trimmed_df['Response (mV)'], c = 'red', s=.2)
            
        elif csv_file[1] == '3':
            trimmed_df = trim_data(csv_file)
            ax.scatter(trimmed_df['Relative Time'], trimmed_df['Response (mV)'], c = 'maroon', s=.2)
            ax.legend(['40°C'])

    # Change legend marker size
    lgnd = ax.legend(['40°C', '30°C', '23°C'], framealpha = 1, fancybox = False, loc = 'lower right')
    for handle in lgnd.legend_handles:
        handle.set_sizes([20])

    # Manually change legend color
    ax.get_legend().legend_handles[0].set_color('maroon')
    ax.get_legend().legend_handles[1].set_color('red')
    ax.get_legend().legend_handles[2].set_color('lightsalmon')
    lgnd.get_frame().set_edgecolor('black')
    # plt.legend().legend_handles.set_sizes([30])
    # ax.get_legend().legend_handles[1].set_sizes(30) 
    # ax.get_legend().legend_handles[2].set_sizes(30) 
    print(dir(ax.get_legend().legend_handles[2]))
    print(ax)

    #! Save image
    # plt.savefig(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Plots\Response vs. Time (all trials).jpg", format="jpg", dpi=1200)


    # %% [markdown]
    # # Grid: noisy - all trials 4x3 grid 

    # %%

    #############################################################################! Remove noise before Savitzky-Golay Filter #########################################################################################################################
    xlabel = 'Time (s)'
    ylabel = 'Response (mV)'

    # Set dimension of number of graphs used for figure 

    fig, ax = plt.subplots(nrows=4, ncols=3)
    fig.set_figheight(15)
    fig.set_figwidth(20)
    fig.suptitle('ATBC P4 PVC Gel \n Response vs. Load (Discrete Temperature - unfiltered)', fontsize = 30, y = .97)

    i = 0
    for csv_file in os.listdir(directory)[0:4]:
        trimmed_df = trim_data(f't1e{i+1}.csv')
        ax[i,0].scatter(trimmed_df['Relative Time'], trimmed_df['Response (mV)'], c = 'lightsalmon', s=4)
        ax[i,0].set_xlabel(xlabel)
        ax[i,0].set_ylabel(ylabel)
        i += 1

    i = 0
    for csv_file in os.listdir(directory)[4:8]:
        trimmed_df = trim_data(f't2e{i+1}.csv')
        ax[i,1].scatter(trimmed_df['Relative Time'], trimmed_df['Response (mV)'], c = 'red', s=4)
        ax[i,1].set_xlabel(xlabel)
        ax[i,1].set_ylabel(ylabel)
        i += 1


    i = 0
    for csv_file in os.listdir(directory)[8:12]:
        trimmed_df = trim_data(f't3e{i+1}.csv')
        ax[i,2].scatter(trimmed_df['Relative Time'], trimmed_df['Response (mV)'], c = 'maroon', s=4)
        ax[i,2].set_xlabel(xlabel)
        ax[i,2].set_ylabel(ylabel)
        i += 1


    # Change legend marker size
    lgnd = fig.legend(['40°C', '30°C', '23°C'], framealpha = 1, borderpad = 2, loc = (0.835, 0.9))
    for handle in lgnd.legend_handles:
        handle.set_sizes([100])

    # Manually change legend color
    lgnd.legend_handles[0].set_color('maroon')
    lgnd.legend_handles[1].set_color('red')
    lgnd.legend_handles[2].set_color('lightsalmon')
    lgnd.get_frame().set_edgecolor('black')

    fig.tight_layout(pad=3.0)

    #! Save image
    plt.savefig(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Plots\Grid (Noisy) - Response vs. Time (all trials).jpg", format="jpg", dpi=1200)


    # %% [markdown]
    # # Grid: LocalOutlierProability outliers removed 4 x 3 grid

    # %%

    #!#######################################################################################################################

    # Set dimension of number of graphs used for figure 

    filtered_df_list = [] # Initialize list to store filtered dataframes 

    fig, ax = plt.subplots(nrows=4, ncols=3)
    fig.set_figheight(15)
    fig.set_figwidth(20)
    fig.suptitle('ATBC P4 PVC Gel \n Response vs. Time (Discrete Temperature)', fontsize = 30, y = .96)

    # threshold to drop data points based on the probablity that they are outliers
    lop_score_threshold = 0.2

    # Set xlabel and ylabel for all graphs
    xlabel = 'Time (s)'
    ylabel = 'Response (mV)'

    i = 0
    for csv_file in os.listdir(directory)[0:4]:
        lop_df = trim_data(f't1e{i+1}.csv')
        m = loop.LocalOutlierProbability(lop_df.drop(columns='Load (g)'), extent=.25, n_neighbors = 20).fit() # Used to find scores
        scores = m.local_outlier_probabilities # this is an attribute after performing LocalOutlierProbability()
        lop_df['scores'] = scores.tolist() # Adding scores to lop_df
        filtered_df = lop_df.query(f'scores < {lop_score_threshold}') # Final df with dropped outliers
        filtered_df_list.append(filtered_df)
        ax[i,0].scatter(lop_df.query(f'scores < {lop_score_threshold}')['Relative Time'], lop_df.query(f'scores < {lop_score_threshold}')['Response (mV)'], c = 'lightsalmon', s=4 )
        ax[i,0].set_xlabel(xlabel)
        ax[i,0].set_ylabel(ylabel)
        i += 1


    i = 0
    for csv_file in os.listdir(directory)[4:8]:
        lop_df = trim_data(f't2e{i+1}.csv')
        m = loop.LocalOutlierProbability(lop_df.drop(columns='Load (g)'), extent=.25, n_neighbors = 20).fit() # Used to find scores
        scores = m.local_outlier_probabilities # this is an attribute after performing LocalOutlierProbability()
        lop_df['scores'] = scores.tolist() # Adding scores to lop_df
        filtered_df = lop_df.query(f'scores < {lop_score_threshold}') # Final df with dropped outliers
        filtered_df_list.append(filtered_df)
        ax[i,1].scatter(lop_df.query(f'scores < {lop_score_threshold}')['Relative Time'], lop_df.query(f'scores < {lop_score_threshold}')['Response (mV)'], c = 'red', s=4 )
        ax[i,1].set_xlabel(xlabel)
        ax[i,1].set_ylabel(ylabel)
        i += 1



    i = 0
    for csv_file in os.listdir(directory)[8:12]:
        lop_df = trim_data(f't3e{i+1}.csv')
        m = loop.LocalOutlierProbability(lop_df.drop(columns='Load (g)'), extent=.25, n_neighbors = 20).fit() # Used to find scores
        scores = m.local_outlier_probabilities # this is an attribute after performing LocalOutlierProbability()
        lop_df['scores'] = scores.tolist() # Adding scores to lop_df
        filtered_df = lop_df.query(f'scores < {lop_score_threshold}') # Final df with dropped outliers
        filtered_df_list.append(filtered_df)
        ax[i,2].scatter(lop_df.query(f'scores < {lop_score_threshold}')['Relative Time'], lop_df.query(f'scores < {lop_score_threshold}')['Response (mV)'], c = 'maroon', s=4 )
        ax[i,2].set_xlabel(xlabel)
        ax[i,2].set_ylabel(ylabel)
        i += 1




    # Change legend marker size
    lgnd = fig.legend(['40°C', '30°C', '23°C'], framealpha = 1, borderpad = 2, loc = (0.835, 0.9))
    for handle in lgnd.legend_handles:
        handle.set_sizes([100])

    # Manually change legend color
    lgnd.legend_handles[0].set_color('maroon')
    lgnd.legend_handles[1].set_color('red')
    lgnd.legend_handles[2].set_color('lightsalmon')
    lgnd.get_frame().set_edgecolor('black')

    fig.tight_layout(pad=3.0)

    # #! Save image
    plt.savefig(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Plots\Grid (LOP) - Response vs. Time (all trials).jpg", format="jpg", dpi=1200)



    # %% [markdown]
    # # Grid: Resp. vs Load (filtered data used)

    # %%
    fig, ax = plt.subplots(nrows=4, ncols=3)
    fig.set_figheight(15)
    fig.set_figwidth(20)
    fig.suptitle('ATBC P4 PVC Gel \n Response vs. Load (Discrete Temperature)', fontsize = 30, y = .96)


    xlabel = 'Load (g)'
    ylabel = 'Response (mV)'

    i = 0
    for filtered_df in filtered_df_list[0:4]:
        if i < 4:
            ax[i,0].scatter(filtered_df['Load (g)'], filtered_df['Response (mV)'], c = 'lightsalmon', s=4 )
            ax[i,0].set_xlabel(xlabel)
            ax[i,0].set_ylabel(ylabel)
            i += 1

    i = 0
    for filtered_df in filtered_df_list[4:8]:
        if i < 4:
            ax[i,1].scatter(filtered_df['Load (g)'], filtered_df['Response (mV)'], c = 'red', s=4 )
            ax[i,1].set_xlabel(xlabel)
            ax[i,1].set_ylabel(ylabel)
            i += 1

    i = 0
    for filtered_df in filtered_df_list[8:12]:
        if i < 4:
            ax[i,2].scatter(filtered_df['Load (g)'], filtered_df['Response (mV)'], c = 'maroon', s=4 )
            ax[i,2].set_xlabel(xlabel)
            ax[i,2].set_ylabel(ylabel)
            i += 1



    # Change legend marker size
    lgnd = fig.legend(['40°C', '30°C', '23°C'], framealpha = 1, borderpad = 2, loc = (0.835, 0.9))
    for handle in lgnd.legend_handles:
        handle.set_sizes([100])

    # Manually change legend color
    lgnd.legend_handles[0].set_color('maroon')
    lgnd.legend_handles[1].set_color('red')
    lgnd.legend_handles[2].set_color('lightsalmon')
    lgnd.get_frame().set_edgecolor('black')
    fig.tight_layout(pad=3.0)

    print(len(filtered_df_list))



    # %% [markdown]
    # # One graph: Load domain (LOP filtered data)

    # %%

    fig, ax = plt.subplots()
    ax.set_ylabel('Response (mV)', fontsize = 13)  # a figure with a single Axes
    ax.set_xlabel('Load (g)', fontsize = 13)
    ax.set_title('ATBC P4 PVC Gel \n Response vs. Load (Discrete Temperature)', fontsize = 13)



    for filtered_df in filtered_df_list[0:4]:
        ax.scatter(filtered_df['Load (g)'], filtered_df['Response (mV)'], c = 'lightsalmon', s=.2)
            
    for filtered_df in filtered_df_list[4:8]:
        trimmed_df = trim_data(csv_file)
        ax.scatter(filtered_df['Load (g)'], filtered_df['Response (mV)'], c = 'red', s=.2)
            
    for filtered_df in filtered_df_list[8:12]:
        trimmed_df = trim_data(csv_file)
        ax.scatter(filtered_df['Load (g)'], filtered_df['Response (mV)'], c = 'maroon', s=.2)


    # Change legend marker size
    lgnd = ax.legend(['40°C', '30°C', '23°C'], framealpha = 1, fancybox = False, loc = 'lower right')
    for handle in lgnd.legend_handles:
        handle.set_sizes([20])

    # Manually change legend color
    ax.get_legend().legend_handles[0].set_color('maroon')
    ax.get_legend().legend_handles[1].set_color('red')
    ax.get_legend().legend_handles[2].set_color('lightsalmon')
    lgnd.get_frame().set_edgecolor('black')
    # plt.legend().legend_handles.set_sizes([30])
    # ax.get_legend().legend_handles[1].set_sizes(30) 
    # ax.get_legend().legend_handles[2].set_sizes(30) 
    print(dir(ax.get_legend().legend_handles[2]))
    print(ax)

    # #! Save image
    plt.savefig(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Plots\One graph (LOP) - Response vs. Load (all trials).jpg", format="jpg", dpi=1200)

    # %% [markdown]
    # # One graph: Time domain (LOP filtered data)

    # %%

    fig, ax = plt.subplots()
    ax.set_ylabel('Response (mV)', fontsize = 13)  # a figure with a single Axes
    ax.set_xlabel('Time (s)', fontsize = 13)
    ax.set_title('ATBC P4 PVC Gel \n Response vs. Time (Discrete Temperature)', fontsize = 13)



    for filtered_df in filtered_df_list[0:4]:
        ax.scatter(filtered_df['Relative Time'], filtered_df['Response (mV)'], c = 'lightsalmon', s=.2)
            
    for filtered_df in filtered_df_list[4:8]:
        trimmed_df = trim_data(csv_file)
        ax.scatter(filtered_df['Relative Time'], filtered_df['Response (mV)'], c = 'red', s=.2)
            
    for filtered_df in filtered_df_list[8:12]:
        trimmed_df = trim_data(csv_file)
        ax.scatter(filtered_df['Relative Time'], filtered_df['Response (mV)'], c = 'maroon', s=.2)


    # Change legend marker size
    lgnd = ax.legend(['40°C', '30°C', '23°C'], framealpha = 1, fancybox = False, loc = 'lower right')
    for handle in lgnd.legend_handles:
        handle.set_sizes([20])

    # Manually change legend color
    ax.get_legend().legend_handles[0].set_color('maroon')
    ax.get_legend().legend_handles[1].set_color('red')
    ax.get_legend().legend_handles[2].set_color('lightsalmon')
    lgnd.get_frame().set_edgecolor('black')
    # plt.legend().legend_handles.set_sizes([30])
    # ax.get_legend().legend_handles[1].set_sizes(30) 
    # ax.get_legend().legend_handles[2].set_sizes(30) 
    print(dir(ax.get_legend().legend_handles[2]))
    print(ax)

    # #! Save image
    plt.savefig(r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Plots\One graph (LOP) - Response vs. Time (all trials).jpg", format="jpg", dpi=1200)

    # %% [markdown]
    # # Random .pdf to .jpg conversion script

    # %%
    from pdf2image import convert_from_path

    # import required module
    import os
    dates_list = ['4.2', '6.12', '6.13', '6.15', '6.19', '6.21', '6.24', '6.26', '6.28', '6.29']

    dunder = []
    i = 0
    for day in dates_list:   
        dunder.append(dates_list[i].replace('.', '_'))
        i += 1

    print(dates_list)
    print(dunder)

    for day in dunder:
        date = f'{day}_23'
        file_name = f'{date}.jpg'
        old_file_name = file_name.replace('_', '.').replace('.jpg', '.pdf') 
        # assign directory
        directory = r'C:\\Users\\asenn\\OneDrive\\Dhamma\\Journaling\\old\\{}'.format(old_file_name)
        print(f"old_file_name: {directory}")
        output_file = r'C:\\Users\\asenn\\OneDrive\\Dhamma\\Journaling\\test\\Date{}'.format(file_name)
        print(output_file)
        pages = convert_from_path(directory, poppler_path = r"C:\Users\asenn\Downloads\Release-23.05.0-0\poppler-23.05.0\Library\bin", output_folder=r'C:\\Users\\asenn\\OneDrive\\Dhamma\\Journaling\\test\\', output_file = r'{}'.format(file_name), dpi = 400, fmt='jpg')
        
    # for count, page in enumerate(pages):
    #     page.save(f'out{count}.jpg', 'JPEG')


    # MyID = 'X12345'    
    # MasterFile_Name = r'Users\ABC\{}\DEF\File - Test.xlsx'.format(MyID)    
    # print(MasterFile_Name)

    # %%
    files_list = []

    for file in os.listdir(r"C:\\Users\\asenn\\OneDrive\\Dhamma\\Journaling\\old"):
        files_list.append(file.replace('.pdf', '.jpg'))

    for file in files_list:
        print (file)

def get_data(files: list[Path]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get data"""
    loads: list[pd.DataFrame] = []
    responses: list[pd.DataFrame] = []
    multiindex: list[tuple[int, int]] = []
    for file in files:
        temperature, trial_index = get_index(file)
        trial = pd.read_csv(file)
        load = trial  # TODO: Get just the load values and associated times
        response = trial  # TODO: Get just the responses and associated times
        loads.append(load)
        responses.append(response)
        multiindex.append((temperature, trial_index))

    index_names = ["temperature", "trial"]
    all_loads = pd.concat(loads).set_index(pd.MultiIndex.from_tuples(multiindex, names=index_names))
    all_responses = pd.concat(responses).set_index(pd.MultiIndex.from_tuples(multiindex, names=index_names))
    return all_loads, all_responses

def get_index(file: Path) -> tuple[int, int]:
    """Parse trial filenames and get the temperature and trial."""
    temperatures = {"T1": 0, "T2": 10, "T3": 20}
    # TODO: Implement this
    return temperature, trial_index

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    #! Source: https://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')


def print_dataframe_pls(dataframe):
    with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(dataframe)


def trim_data(filename: str):
    # sourcery skip: use-fstring-for-formatting
    """
    Returns a trimmed DataFrame of pvc gel temperature experiment trial with 650 data points. The last 250 data
    points of the experiment are omitted, and are not included in the 650 data points. 
    The data is trimmed at the stopping point, which is identified when the load dramatically changes 
    indicating that the plunger has been lifted off of the gel quickly (which is what happens when
    the experiment is finished)
    """

    first_test = pd.read_csv(filepath_or_buffer = r"C:\Users\asenn\OneDrive\School\Research\MSIPP (Georgia 2023)\Raw Temperature Data\{}".format(filename), skiprows=18)
    split_df_index_location = first_test.diff().multiply(-1).idxmax()[0]

    load_channel_raw = first_test.iloc[:split_df_index_location,:].dropna(axis=1)
    # Drop last row in load_channel so that load_channel and pvc_channel have the same length 
    load_channel_raw.drop([len(load_channel_raw)-1], inplace=True)
    # Multiply to make sure that Load is in grams 10 mV = 250g 
    load_channel = load_channel_raw.multiply(other= [1, -1000 * 25])

    # Sort pvc data into separate DataFrame to combine later 
    pvc_channel = first_test.iloc[split_df_index_location:,:].dropna(axis=1).drop(columns=['Relative Time']).reset_index(drop = True)  * -1000 # Convert V to mV 

    # Combine DataFrames into n x 3 DataFrame() with Time, Load and PVC Response 
    main_df_untrimmed = pd.concat((load_channel, pvc_channel), axis=1)

    stopping_point = main_df_untrimmed.diff().multiply(-1).idxmax()[1]

    main_df_trimmed = main_df_untrimmed[stopping_point - 900:stopping_point-250]

    # Rename columns from CH1XX to Load and Response
    main_df_trimmed.rename({'CH110':'Load (g)', 'CH108':'Response (mV)'}, inplace=True, axis = 1)

    return main_df_trimmed

if __name__ == "__main__":
    main()