import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def fix_csv_file(file_path, fixed_file_path):
    """
    Fixes the CSV file by replacing the first row with the correct header.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    first_line = True
    with open(fixed_file_path, "w") as file:
        for line in lines:
            if first_line:
                file.write(line)
                first_line = False
            else:
                file.write(line.replace(" ", ""))

def extract_column(dataset, column_name):
    """
    Extracts a column from the dataset and returns it as a list of floats.
    """
    column_data = dataset[column_name].to_numpy()
    return column_data

def interpolate_nans(arr):
    arr = arr.copy()
    arr = np.array(arr, dtype=float)
    nans = np.isnan(arr)
    if np.all(nans):
        return arr 
    x = np.arange(len(arr))
    arr[nans] = np.interp(x[nans], x[~nans], arr[~nans])
    return arr

def rep_21():
    source_file = "workfiles/team13_protocol.csv"
    source_file_fixed = "workfiles/team13_protocol_fixed.csv"

    # Fix File
    fix_csv_file(source_file, source_file_fixed)

    # Extract Data Lists needed
    dataset = pd.read_csv(source_file_fixed)
    # dataset.iloc[:,1] <= Get List of all Values in Column 1 (6 · # Packets)
    packet_list = extract_column(dataset, "6 · # Packets")
    packet_list = interpolate_nans(packet_list)
    uIPs_list = extract_column(dataset, " 6 · # Unique Source IPs")
    uIPs_list = interpolate_nans(uIPs_list)
    
    plot_dict = {
        "Packets/hour":{
            "time_xlabel": "hours in h",
            "time_ylabel": "#Packets",
            "values": packet_list,
            "fft_title": "Amp. Spectrum for #pkts'",
            "fft_xlabel": "k",
            "fft_ylabel": "Amplitude [millions of pkts]"
        },
        "uIPs/hour":{
            "time_xlabel": "hours in h",
            "time_ylabel": "#uIPs",
            "values": uIPs_list,
            "fft_title": "Amp. Spectrum for #uIPs'",
            "fft_xlabel": "k",
            "fft_ylabel": "Amplitude [millions of uIPs]",
        }
    }

    # =============================
    # === Plot Time Diagram
    # =============================
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Time Series", fontsize=14, weight='bold')

    for column, key in enumerate(plot_dict):
        ax = axes[column]
        y = plot_dict[key]["values"]
        x = range(0, len(y))
        ax.plot(x, y)
        ax.set_title(key)
        ax.set_xlabel(plot_dict[key]["time_xlabel"])
        ax.set_ylabel(plot_dict[key]["time_ylabel"])

    plt.tight_layout()
    plt.show()

    # =============================
    # === Plot Time Diagram
    # =============================
    N = 31 * 24     # January has 31 days

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("FFT", fontsize=14, weight='bold')

    for column, key in enumerate(plot_dict):
        ax = axes[column]
        value_list = plot_dict[key]["values"]

        pkt_fft = np.fft.fft(value_list)
        pkt_amp = np.abs(pkt_fft)

        n = len(value_list)
        x = range(1, math.floor(n/2))
        y = pkt_amp[1:math.floor(n/2)]

        max_k = np.argmax(y)

        
        max_amp = y[max_k]

        ax.plot(x, y)
        ax.set_title(plot_dict[key]["fft_title"])
        ax.set_xlabel(plot_dict[key]["fft_xlabel"])
        ax.set_ylabel(plot_dict[key]["fft_ylabel"])
        ax.set_xlim(1, math.floor(n/2))
        ax.set_ylim(1, max_amp)

        # Calculate Max Amplitude and Period
        max_k = max_k + 1   
        p_k = N/max_k

        print(f"{key} FFT: ")
        max_amp = round(max_amp/1_000_000, 4)
        print(f"Max Value: {max_amp} (in Millions)")
        print(f"k of max Value: {max_k}")
        p_k = round(p_k, 4)
        print(f"Period of k: {p_k}\n")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    # =================================================================================
    # === Part 2: rep-18a
    # =================================================================================
    rep_21()