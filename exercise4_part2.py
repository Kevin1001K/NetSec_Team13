import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def extract_column(dataset, column_name):
    """
    Extracts a column from the dataset and returns it as a list of floats.
    """
    column_data = dataset[column_name].tolist()
    return column_data

def rep_23():
    source_file = "workfiles/Ex2flows_team13.csv"
    
    # Extract Data Lists needed
    dataset = pd.read_csv(source_file)

    tcp_mode_list = extract_column(dataset, "mode(_tcpFlags)")
    tcp_mode_list = [str(tcp_mode) for tcp_mode in tcp_mode_list]

    tcp_mode_dict = {}
    for tcp_mode in tcp_mode_list:
        if tcp_mode == "nan":
            continue
        if tcp_mode not in tcp_mode_dict:
            tcp_mode_dict[tcp_mode] = 0
        tcp_mode_dict[tcp_mode] += 1

    # Sort by numbers of tcp mode 
    keys = list(tcp_mode_dict.keys())
    values = list(tcp_mode_dict.values())
    total_num = np.sum(values)
    sorted_value_index = np.argsort(values)
    tcp_mode_sort_dict = {keys[i]: values[i] for i in sorted_value_index}

    for tcp_mode, num in tcp_mode_sort_dict.items():
        percent = round(num*100/total_num, 4)
        print(f"{tcp_mode}: {num}, {percent}%")

    # Extract TTL
    ttl_list = extract_column(dataset, "mode(ipTTL)")

def create_histogram(source_file, column_name):
    # Extract Data Lists needed
    dataset = pd.read_csv(source_file)

    value_list = extract_column(dataset, column_name)

    plt.hist(value_list)
    plt.title("Mode of TTL")

    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    source_file = "workfiles/Ex2flows_team13.csv"

    # =================================================================================
    # === Part 2: rep-18a
    # =================================================================================
    # rep_23()

    create_histogram(source_file, "mode(ipTTL)")