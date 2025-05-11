# library imports
import datetime
import pandas as pd  
import numpy as np
import math
import matplotlib.pyplot as plt 
import matplotlib.dates as mdate

def fix_csv_file(file_path, fixed_file_path):
    """
    Fixes the CSV file by replacing the first row with the correct header.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    first_line = True
    with open(fixed_file_path, 'w') as file:
        for line in lines:
            if first_line:
                file.write(line)
                first_line = False
            else:
                file.write(line.replace(' ', ''))

def interpolate_nans(arr):
    arr = arr.copy()
    arr = np.array(arr, dtype=float)
    nans = np.isnan(arr)
    if np.all(nans):
        return arr 
    x = np.arange(len(arr))
    arr[nans] = np.interp(x[nans], x[~nans], arr[~nans])
    return arr

def extract_column_with_interpol(dataset, column_name):
    """
    Extracts a column from the dataset and returns it as a list of floats.
    Also handles NaN values by interpolating them.
    """
    column_data = dataset[column_name].tolist()
    if isinstance(column_data[0], str):
        column_data = [x.strip() for x in column_data]
        column_data = [float(x) if x != "" else np.nan for x in column_data]
    return interpolate_nans(column_data)

def extract_column(dataset, column_name):
    column_data = dataset[column_name].tolist()
    return column_data

def extract_column_without_nan(dataset, column_name):
    column_data = dataset[column_name].tolist()
    column_data = [x for x in column_data if math.isnan(x) == False]
    return column_data

def plot_list(x_list, y_list, title, xlabel, ylabel):
    """
    Plots a list of values with the given title and labels.
    """
    #create a list with the timestamps
    raw = pd.to_datetime(x_list, unit='s')

    # creating the plotting environment
    fig, ax = plt.subplots()

    # formating axes, ticks and ticklabels for timestamps
    timestamps = mdate.date2num(raw)
    date_fmt = '%y-%m-%d' #for full date: date_fmt = '%d-%m-%y %H:%M:%S'
    date_formatter = mdate.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.xaxis_date()
    fig.autofmt_xdate()

    # title and x,y-labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # plot stem graphic
    plt.stem(timestamps, [(x / (10**6)) for x in y_list], linefmt='C0-', markerfmt=" ", basefmt=" ")
    plt.grid()
    plt.show()

def rep_15(source_file):
    # Load Dataset
    dataset = pd.read_csv(source_file)

    #create a list with packets_per_day
    packet_list = extract_column_with_interpol(dataset, '# Packets')
    byte_list = extract_column_with_interpol(dataset, ' # Bytes')
    uip_src_list = extract_column_with_interpol(dataset, '# Unique Source IPs')
    uip_dst_list = extract_column_with_interpol(dataset, '# Unique Destination IPs')

    print(f"Answer to subexercise 15-a to 15-c:")
    correlation_packet_uip_dst = np.corrcoef(packet_list, uip_dst_list)
    print(f"Correlation between packets and unique destination IPs: {correlation_packet_uip_dst[0, 1]}")
    correlation_packet_bytes = np.corrcoef(packet_list, byte_list)
    print(f"Correlation between packets and bytes: {correlation_packet_bytes[0, 1]}")
    correlation_uip_src_uip_dst = np.corrcoef(uip_src_list, uip_dst_list)
    print(f"Correlation between unique source IPs and unique destination IPs: {correlation_uip_src_uip_dst[0, 1]} \n")
    
    # plot_list(x_list=dataset['Timestamp'], 
    #           y_list=packet_list, 
    #           title='Number of bytes per hour (daily average)', 
    #           xlabel='days of observed time span', 
    #           ylabel='# Bytes/hour [millions]')

def rep_15_diagrams(source_file):
    # Load Dataset
    dataset = pd.read_csv(source_file)
    
    timestamp_list = extract_column(dataset, "timestamp")
    timestamp_list = pd.to_datetime(timestamp_list, unit='s')
    timestamps = mdate.date2num(timestamp_list)

    pkt_list = extract_column_with_interpol(dataset, "# Packets")
    bytes_list = extract_column_with_interpol(dataset, " # Bytes")
    uip_src_list = extract_column_with_interpol(dataset, "# Unique Source IPs")
    uip_dst_list = extract_column_with_interpol(dataset, "# Unique Destination IPs")

    plot_dict = {
        "Packets": {
            "title": "Number of packets per hour (daily average)",
            "ylabel": "#pkts/hour [millions]",
            "values": pkt_list
        },
        "Bytes": {
            "title": "Number of bytes per hour (daily average)",
            "ylabel": "#bytes/hour [millions]",
            "values": bytes_list
        },
        "Unique IP sources": {
            "title": "Number of Unique IP sources per hour (daily average)",
            "ylabel": "#bytes/hour [millions]",
            "values": uip_src_list
        },
        "Unique IP destinations": {
            "title": "Number of Unique IP destinations per hour (daily average)",
            "ylabel": "#bytes/hour [millions]",
            "values": uip_dst_list
        },
    }

    for plot_name in plot_dict:
        # creating the plotting environment
        fig, ax = plt.subplots()
        
        date_fmt = '%y-%m-%d' #for full date: date_fmt = '%d-%m-%y %H:%M:%S'
        date_formatter = mdate.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.xaxis_date()
        fig.autofmt_xdate()

        plt.title(plot_dict[plot_name]["title"])
        plt.ylabel(plot_dict[plot_name]["ylabel"])

        # plot stem graphic
        plt.stem(timestamps, [(x / (10**6)) for x in plot_dict[plot_name]["values"]], linefmt='C0-', markerfmt=" ", basefmt=" ")

        plt.tight_layout()
        plt.grid()
        plt.show()

def rep_16(source_file):
    # Load Dataset
    dataset = pd.read_csv(source_file)

    print(f"Answer to subexercise 16:")
    uip_src_list = extract_column_without_nan(dataset, '# Unique Source IPs')
    uip_src_median = np.median(uip_src_list)
    uip_dst_list = extract_column_without_nan(dataset, '# Unique Destination IPs')
    uip_dst_median = np.median(uip_dst_list)

    uid_src_uid_dst_ratio_median = uip_dst_median/uip_src_median
    print(f"Median of the ratio between unique source IPs and unique destination IPs: {uid_src_uid_dst_ratio_median} \n")

def rep_17(source_file):
    # Load Dataset
    dataset = pd.read_csv(source_file)
    
    uip_src_list = extract_column(dataset, '# Unique Source IPs')
    timestamp_list = extract_column(dataset, 'timestamp')

    # Find max value and its index
    max_index = 0
    for i, value in enumerate(uip_src_list):
        if (not math.isnan(value)) and (value > uip_src_list[max_index]):
            max_index = i

    max_value_timestamp = timestamp_list[max_index]

    date_obj = datetime.datetime.fromtimestamp(max_value_timestamp)
    
    print(f"Answer to subexercise 17:")
    print("Max # Unique Source IPs: " + str(uip_src_list[max_index]))
    print("Timestamp of # Unique Source IPs: " + str(max_value_timestamp))
    print("Date of max # Unique Source IPs: " + date_obj.strftime("%d-%m-%Y %H"))

if __name__ == "__main__":
    # loading data from CSV file
    source_file_path = 'workfiles/global_last10years.csv'
    fixed_file_path = 'workfiles/global_last10years_fixed.csv'

    # Fix File
    fix_csv_file(source_file_path, fixed_file_path)
    
    # =================================================================================
    # === Rep-15
    # =================================================================================
    # rep_15(fixed_file_path)

    rep_15_diagrams(fixed_file_path)

    # =================================================================================
    # === Rep-16
    # =================================================================================
    # rep_16(fixed_file_path)
    
    # =================================================================================
    # === Rep-17
    # =================================================================================
    # rep_17(fixed_file_path)