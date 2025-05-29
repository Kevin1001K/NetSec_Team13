import json
import math
import pandas as pd  
import matplotlib.pyplot as plt
import numpy as np

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
    """
    Extracts a column from the dataset and returns it as a list of floats.
    """
    column_data = dataset[column_name].tolist()
    return column_data

def extract_column_without_nan(dataset, column_name):
    """
    Extracts a column from the dataset and returns it as a list of floats.
    """
    column_data = dataset[column_name].tolist()
    column_data = [x for x in column_data if math.isnan(x) == False]
    return column_data

def get_list_statistic_dict(value_list):
    statistic_dict = {}
    statistic_dict["total_sum"] = np.nansum(value_list)
    statistic_dict["mean"] = np.nanmean(value_list)
    statistic_dict["median"] = np.nanmedian(value_list)
    statistic_dict["std_dev"] = np.nanstd(value_list)

    return statistic_dict

def rep_18a():
    # Source Files
    source_A_file_path = "workfiles/team13_monthly.csv"
    fixed_A_file_path = "workfiles/team13_monthly_fixed.csv"
    statistic_A_json_file = "exercise3_part2_A_statistic.json"

    # Fix File
    fix_csv_file(source_A_file_path, fixed_A_file_path)

    # Load Dataset
    dataset_A_month = pd.read_csv(fixed_A_file_path)

    #create a list with packets_per_day
    month_packet_list = extract_column(dataset_A_month, "#packets")
    month_byte_list = extract_column(dataset_A_month, "#bytes")
    month_uip_src_list = extract_column(dataset_A_month, "#unique_IP_sources")
    month_uip_dst_list = extract_column(dataset_A_month, "#unique_IP_destinations")

    statistic_A_dict = {}
    statistic_A_dict["#packets"] = get_list_statistic_dict(month_packet_list)
    statistic_A_dict["#bytes"] = get_list_statistic_dict(month_byte_list)
    statistic_A_dict["#unique_IP_sources"] = get_list_statistic_dict(month_uip_src_list)
    statistic_A_dict["#unique_IP_destinations"] = get_list_statistic_dict(month_uip_dst_list)

    # Save result in json file
    with open(statistic_A_json_file, "w") as file:
        json.dump(statistic_A_dict, file, indent="\t")

    return statistic_A_dict

def rep_18b():
    source_B_file_path = "workfiles/global_last10years.csv"
    source_B_temp_file_path = "workfiles/global_last10years_temp.csv"
    fixed_B_file_path = "workfiles/global_last10years_fixed.csv"
    statistic_B_json_file = "exercise3_part2_B_statistic.json"

    # Extract entries of the given monath and save it in a temp file
    with open(source_B_file_path, "r") as file:
        lines = file.readlines()

    first_line = True
    with open(source_B_temp_file_path, "w") as file:
        for line in lines:
            if first_line:
                file.write(line)
                first_line = False
            else:
                line_parts = line.split(",")
                timestamp = int(line_parts[0])
                # Starting TImestamp of monthly.csv: 1577833200
                # Ending TImestamp of monthly.csv: 1580508000
                if (timestamp >= 1577833200) and (timestamp <= 1580508000):
                    file.write(line)

    # Fix File
    fix_csv_file(source_B_temp_file_path, fixed_B_file_path)
    
    # Load Dataset
    dataset_B_year_month = pd.read_csv(fixed_B_file_path)

    #create a list with packets_per_day
    year_packet_list = extract_column(dataset_B_year_month, "# Packets")
    year_byte_list = extract_column(dataset_B_year_month, " # Bytes")
    year_uip_src_list = extract_column(dataset_B_year_month, "# Unique Source IPs")
    year_uip_dst_list = extract_column(dataset_B_year_month, "# Unique Destination IPs")

    statistic_B_dict = {}
    statistic_B_dict["#packets"] = get_list_statistic_dict(year_packet_list)
    statistic_B_dict["#bytes"] = get_list_statistic_dict(year_byte_list)
    statistic_B_dict["#unique_IP_sources"] = get_list_statistic_dict(year_uip_src_list)
    statistic_B_dict["#unique_IP_destinations"] = get_list_statistic_dict(year_uip_dst_list)

    # Save result in json file
    with open(statistic_B_json_file, "w") as file:
        json.dump(statistic_B_dict, file, indent="\t")

    return statistic_B_dict

def rep_18b_tables():
    statistic_A_dict = rep_18a()
    statistic_B_dict = rep_18b()

    # Convert Statistic from per day top per hour
    statistic_dict = {
        "Month File Statistic": {
            "index": ["#pkts/hour", "#bytes/hour", "#uIPs/hour", "#uIPs/hour"],
            "values": statistic_A_dict,
        },
        "Year File Statistic": {
            "index": ["#pkts/day", "#bytes/day", "#uIPs/day", "#uIPs/day"],
            "values": statistic_B_dict,
        }
    }

    for title, stat_dict in statistic_dict.items():
        table_dict = {
            "total_sum": [],
            "mean": [],
            "median": [],
            "std_dev": []
        }
        for key in stat_dict["values"]:
            table_dict["total_sum"].append(stat_dict["values"][key]["total_sum"])
            table_dict["mean"].append(stat_dict["values"][key]["mean"])
            table_dict["median"].append(stat_dict["values"][key]["median"])
            table_dict["std_dev"].append(stat_dict["values"][key]["std_dev"])

        df = pd.DataFrame(table_dict, index=stat_dict["index"])
        
        fig, ax = plt.subplots(figsize=(8, 2.5))
        fig.suptitle(title, fontsize=14, weight='bold', y=0.8)
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        rowLabels=df.index,
                        cellLoc='center',
                        loc='center')
        table.scale(1, 1.5)
        plt.tight_layout()
        plt.show()

def rep_18b_diagrams():
    # Source Files
    source_A_file_path = "workfiles/team13_monthly.csv"
    fixed_A_file_path = "workfiles/team13_monthly_fixed.csv"

    source_B_file_path = "workfiles/global_last10years.csv"
    source_B_temp_file_path = "workfiles/global_last10years_temp.csv"
    source_B_temp_fixed_file_path = "workfiles/global_last10years_fixed.csv"

    # Fix File
    fix_csv_file(source_A_file_path, fixed_A_file_path)

    # Load Dataset
    dataset_A_month = pd.read_csv(fixed_A_file_path)

    # Extract entries of the given monath and save it in a temp file
    with open(source_B_file_path, "r") as file:
        lines = file.readlines()

    first_line = True
    with open(source_B_temp_file_path, "w") as file:
        for line in lines:
            if first_line:
                file.write(line)
                first_line = False
            else:
                line_parts = line.split(",")
                timestamp = int(line_parts[0])
                # Starting TImestamp of monthly.csv: 1577833200
                # Ending TImestamp of monthly.csv: 1580508000
                if (timestamp >= 1577833200) and (timestamp <= 1580508000):
                    file.write(line)

    # Fix File
    fix_csv_file(source_B_temp_file_path, source_B_temp_fixed_file_path)
    
    # Load Dataset
    dataset_B_year_month = pd.read_csv(source_B_temp_fixed_file_path)

    # Create Diagrams 
    month_packet_list = extract_column_without_nan(dataset_A_month, "#packets")
    month_packet_list = [x/1_000_000 for x in month_packet_list]
    month_byte_list = extract_column_without_nan(dataset_A_month, "#bytes")
    month_byte_list = [x/1_000_000 for x in month_byte_list]
    month_uip_src_list = extract_column_without_nan(dataset_A_month, "#unique_IP_sources")
    month_uip_src_list = [x/1_000_000 for x in month_uip_src_list]
    month_uip_dst_list = extract_column_without_nan(dataset_A_month, "#unique_IP_destinations")
    month_uip_dst_list = [x/1_000_000 for x in month_uip_dst_list]
    
    year_packet_list = extract_column_without_nan(dataset_B_year_month, "# Packets")
    year_packet_list = [x/1_000_000 for x in year_packet_list]
    year_byte_list = extract_column_without_nan(dataset_B_year_month, " # Bytes")
    year_byte_list = [x/1_000_000 for x in year_byte_list]
    year_uip_src_list = extract_column_without_nan(dataset_B_year_month, "# Unique Source IPs")
    year_uip_src_list = [x/1_000_000 for x in year_uip_src_list]
    year_uip_dst_list = extract_column_without_nan(dataset_B_year_month, "# Unique Destination IPs")
    year_uip_dst_list = [x/1_000_000 for x in year_uip_dst_list]

    data = {
        "Packets/hour (Month)":{
            "axis_title":"#Packets/h(M)",
            "values": month_packet_list
        },
        "Bytes/hour (Month)":{
            "axis_title":"#Packets/h(M)",
            "values": month_byte_list
        },
        "uIPs/hour (Month)":{
            "axis_title":"#Packets/h(M)",
            "values": month_uip_src_list
        },
        "uIPd/hour (Month)":{
            "axis_title":"#Packets/h(M)",
            "values": month_uip_dst_list
        },

        "Packets/hour (Year)":{
            "axis_title":"#Packets/h(M)",
            "values": year_packet_list
        },
        "Bytes/hour (Year)":{
            "axis_title":"#Packets/h(M)",
            "values": year_byte_list
        },
        "uIPs/hour (Year)":{
            "axis_title":"#Packets/h(M)",
            "values": year_uip_src_list
        },
        "uIPd/hour (Year)":{
            "axis_title":"#Packets/h(M)",
            "values": year_uip_dst_list
        }
    }

    # Precompute x-axis limits for each variable
    x_limits = {}
    x_limits[0] = (
        np.nanmin(data["Packets/hour (Month)"]["values"] + data["Packets/hour (Year)"]["values"]),
        np.nanmax(data["Packets/hour (Month)"]["values"] + data["Packets/hour (Year)"]["values"])
    )
    x_limits[1] = (
        np.nanmin(data["Bytes/hour (Month)"]["values"] + data["Bytes/hour (Year)"]["values"]),
        np.nanmax(data["Bytes/hour (Month)"]["values"] + data["Bytes/hour (Year)"]["values"])
    )
    x_limits[2] = (
        np.nanmin(data["uIPs/hour (Month)"]["values"] + data["uIPs/hour (Year)"]["values"]),
        np.nanmax(data["uIPs/hour (Month)"]["values"] + data["uIPs/hour (Year)"]["values"])
    )
    x_limits[3] = (
        np.nanmin(data["uIPd/hour (Month)"]["values"] + data["uIPd/hour (Year)"]["values"]),
        np.nanmax(data["uIPd/hour (Month)"]["values"] + data["uIPd/hour (Year)"]["values"])
    )

    # Create Subplots for histogram (2 rows x 4 columns)
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))

    # First row: overall distribution
    for i, key in enumerate(data):
        row = math.floor(i/4)
        column = i % 4
        ax = axes[row, column]
        values = data[key]["values"]
        ax.hist(values, bins=15)
        ax.set_xlim(x_limits[column])
        ax.set_title(key)
        ax.set_xlabel(data[key]["axis_title"])

    plt.tight_layout()
    plt.show()

    # Create subplots for boxplot (2 rows x 4 columns)
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))

    # First row: overall distribution
    for i, key in enumerate(data):
        row = math.floor(i/4)
        column = i % 4
        ax = axes[row, column]
        values = data[key]["values"]
        ax.boxplot(values, vert=True, widths=0.6, patch_artist=False)
        ax.set_title(key)
        ax.set_xlabel(data[key]["axis_title"])
        ax.set_ylabel("(Millions)")

    plt.tight_layout()
    plt.show()

def rep_20():
    # loading data from CSV file
    dataset = pd.read_csv('workfiles/team13_monthly.csv')

    #create a list with packets_per_day
    timestamps_all_nan_arr = dataset['timestamps'].tolist()
    packets_all_nan_arr = dataset['#packets'].tolist()
    uIPsource_all_nan_arr = dataset['#unique_IP_sources'].tolist()
    uIPdest_all_nan_arr = dataset['#unique_IP_destinations'].tolist()

    total_packets = 0
    total_uIPsource = 0
    total_uIPdest = 0

    for timestamp, packet, uIPsource, uIPdest in zip(timestamps_all_nan_arr, packets_all_nan_arr, uIPsource_all_nan_arr, uIPdest_all_nan_arr):
        if not np.isnan(packet):
            total_packets += packet
            total_uIPsource += uIPsource
            total_uIPdest += uIPdest

    # loading data from CSV file
    dataset = pd.read_csv('workfiles/team13_protocol.csv')

    #create a list with packets_per_day
    timestamps_3_nan_arr = dataset['timestamp'].tolist()

    packets_tcp_nan_arr = dataset['6 · # Packets'].tolist()
    uIPsource_tcp_nan_arr = dataset[' 6 · # Unique Source IPs'].tolist()
    uIPdest_tcp_nan_arr = dataset[' 6 · # Unique Destination IPs'].tolist()

    packets_udp_nan_arr = dataset['17 · # Packets'].tolist()
    uIPsource_udp_nan_arr = dataset[' 17 · # Unique Source IPs'].tolist()
    uIPdest_udp_nan_arr = dataset[' 17 · # Unique Destination IPs'].tolist()

    packets_icmp_nan_arr = dataset['  1 · # Packets'].tolist()
    uIPsource_icmp_nan_arr = dataset[' 1 · # Unique Source IPs'].tolist()
    uIPdest_icmp_nan_arr = dataset[' 1 · # Unique Destination IPs'].tolist()


    total_3_packets = 0
    total_3_uIPsource = 0
    total_3_uIPdest = 0

    for timestamp_3, packet_tcp, uIPsource_tcp, \
        uIPdest_tcp, packet_udp, uIPsource_udp, \
        uIPdest_udp, packet_icmp, uIPsource_icmp, \
        uIPdest_icmp in \
        zip(timestamps_3_nan_arr, \
        packets_tcp_nan_arr, uIPsource_tcp_nan_arr, uIPdest_tcp_nan_arr, \
        packets_udp_nan_arr, uIPsource_udp_nan_arr, uIPdest_udp_nan_arr, \
        packets_icmp_nan_arr, uIPsource_icmp_nan_arr, uIPdest_icmp_nan_arr):
        
        if not np.isnan(packet_tcp):
            total_3_packets += float(packet_tcp) + float(packet_udp) + float(packet_icmp)
            total_3_uIPsource += float(uIPsource_tcp) + float(uIPsource_udp) + float(uIPsource_icmp)
            total_3_uIPdest += float(uIPdest_tcp) + float(uIPdest_udp) + float(uIPdest_icmp)

    print("Other packets: ", ((total_packets-total_3_packets) * 100) / total_packets)
    print("Other uIPsource: ", ((total_uIPsource-total_3_uIPsource) * 100) / total_uIPsource)
    print("Other uIPdest: ", ((total_uIPdest-total_3_uIPdest) * 100) / total_uIPdest)

if __name__ == "__main__":
    
    # =================================================================================
    # === Part 2: rep-18a
    # =================================================================================
    # rep_18a()

    # =================================================================================
    # === Part 2: rep-18b
    # =================================================================================
    # rep_18b()

    rep_18b_tables()

    # rep_18b_diagrams()

