import calendar
import datetime
import json
import pandas as pd  
import numpy as np
import math

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

def extract_column(dataset, column_name):
    """
    Extracts a column from the dataset and returns it as a list of floats.
    """
    column_data = dataset[column_name].tolist()
    column_data = [x for x in column_data if math.isnan(x) == False]
    return column_data

def get_list_statistic_dict(value_list):
    statistic_dict = {}
    # statistic_dict["total_sum"] = np.sum(value_list)
    # statistic_dict["mean"] = np.nanmean(value_list)
    statistic_dict["median"] = np.median(value_list)/1000_000
    # statistic_dict["std_dev"] = np.std(value_list)

    return statistic_dict

def get_start_timestamp(year, month):
    date_time = datetime.datetime(year, month, 1, 0, 0)
    start_timestamp = datetime.datetime.timestamp(date_time)

    return start_timestamp

def get_end_timestamp(year, month):
    day = calendar.monthrange(year, month)[1]
    date_time = datetime.datetime(year, month, day, 23, 59)
    end_timestamp = datetime.datetime.timestamp(date_time)

    return end_timestamp

def create_statistic_json():
    source_B_file_path = "workfiles/global_last10years.csv"
    source_B_fixed_file_path = "workfiles/global_last10years_fixed.csv"

    source_B_temp_file_path = "workfiles/global_last10years_temp.csv"
    source_B_temp_fixed_file_path = 'workfiles/global_last10years_temp_fixed.csv'
    statistic_B_json_file = 'exercise3_rep_18b_years_statistic.json'

    # Fix File
    fix_csv_file(source_B_file_path, source_B_fixed_file_path)

    # 1267315200  =>  28.02.2010 00:00:00 (Start of day)
    # 1267401600  =>  01.03.2010 00:00:00 (Start of day)
    # start_timestamp = 1267315200
    # end_timestamp   = 1267401599
    # day_in_sec = 86400

    year = 2010
    month = 3

    # Extract all lines from year.csv
    year_entries = []
    with open(source_B_fixed_file_path, 'r') as file:
        year_entries = file.readlines()

    statistic_years_dict = {}
    while not((year == 2020) and (month == 4)):
        start_timestamp = get_start_timestamp(year, month)
        end_timestamp = get_end_timestamp(year, month)

        # Save entries from a given month into the entry
        first_line = True
        with open(source_B_temp_fixed_file_path, 'w') as file:
            for line in year_entries:
                if first_line:
                    file.write(line)
                    first_line = False
                else:
                    line_parts = line.split(",")
                    timestamp = int(line_parts[0])
                    # 1577833200
                    if (timestamp >= start_timestamp) and (timestamp <= end_timestamp):
                        file.write(line)

        # Fix File
        # fix_csv_file(source_B_temp_file_path, source_B_temp_fixed_file_path)

        # Load Dataset
        dataset_B_year_month = pd.read_csv(source_B_temp_fixed_file_path)

        #create a list with packets_per_day
        packet_list = extract_column(dataset_B_year_month, '# Packets')
        byte_list = extract_column(dataset_B_year_month, ' # Bytes')
        uip_src_list = extract_column(dataset_B_year_month, '# Unique Source IPs')
        uip_dst_list = extract_column(dataset_B_year_month, '# Unique Destination IPs')

        statistic_bytes = get_list_statistic_dict(byte_list)

        if statistic_bytes["median"] < 1579.9:
            entry_key = f"{year}-{month}"
            statistic_years_dict[entry_key] = {}
            statistic_years_dict[entry_key]["#start_timestamp"] = start_timestamp
            statistic_years_dict[entry_key]["#end_timestamp"] = end_timestamp

            statistic_years_dict[entry_key]["#bytes"] = get_list_statistic_dict(byte_list)

        # try:
        #     statistic_years_dict[entry_key]["#packets"] = get_list_statistic_dict(packet_list)
        #     statistic_years_dict[entry_key]["#bytes"] = get_list_statistic_dict(byte_list)
        #     statistic_years_dict[entry_key]["#unique_IP_sources"] = get_list_statistic_dict(uip_src_list)
        #     statistic_years_dict[entry_key]["#unique_IP_destinations"] = get_list_statistic_dict(uip_dst_list)
        # except Exception as e:
        #     print(f"Error at {entry_key}: {e}")

        # Set values for next month
        month += 1
        if month > 12:
            year += 1
            month = 1

    # Save result in json file
    with open(statistic_B_json_file, "w") as file:
        json.dump(statistic_years_dict, file, indent="\t")

def create_bytes_list():
    source_B_file_path = "workfiles/global_last10years.csv"
    source_B_fixed_file_path = "workfiles/global_last10years_fixed.csv"

    bytes_file = "bytes_list.txt"

    # Fix File
    fix_csv_file(source_B_file_path, source_B_fixed_file_path)

    year_entries = []
    with open(source_B_fixed_file_path, 'r') as file:
        year_entries = file.readlines()

    first_line = True
    bytes_list = []
    for line in year_entries:
        if first_line:
            first_line = False
        else:
            line_parts = line.split(",")
            if line_parts[1] == "":
                continue
            bytes_hour = float(line_parts[1])/1_000_000
            if bytes_hour < 1580.0:
                bytes_hour = round(bytes_hour, 1)
                bytes_list.append(bytes_hour)

    bytes_list.sort(reverse=True)
    
    with open(bytes_file, "w") as file:
        for bytes_hour in bytes_list:
            file.write(f"{bytes_hour}\n")

def create_bytes_month_list(year, month):
    source_B_file_path = "workfiles/global_last10years.csv"
    source_B_fixed_file_path = "workfiles/global_last10years_fixed.csv"

    bytes_file = f"bytes_list_{year}_{month}.txt"

    # Fix File
    fix_csv_file(source_B_file_path, source_B_fixed_file_path)

    year_entries = []
    with open(source_B_fixed_file_path, 'r') as file:
        year_entries = file.readlines()

    start_timestamp = get_start_timestamp(year, month)
    end_timestamp = get_end_timestamp(year, month)

    first_line = True
    bytes_list = []
    for line in year_entries:
        if first_line:
            first_line = False
        else:
            line_parts = line.split(",")
            if line_parts[1] == "":
                continue
            bytes_hour = float(line_parts[1])/1_000_000

            
            timestamp = int(line_parts[0])
            if (timestamp < start_timestamp) or (timestamp > end_timestamp):
                continue
            if bytes_hour < 1580.0:
                bytes_hour = round(bytes_hour, 1)
                bytes_list.append(bytes_hour)

    bytes_list.sort(reverse=True)
    
    with open(bytes_file, "w") as file:
        for bytes_hour in bytes_list:
            file.write(f"{bytes_hour}\n")

if __name__ == "__main__":

    # Create json file with statistic
    # create_statistic_json()

    # Get list of all #bytes/hour smaller than 1580.0
    # create_bytes_list()

    create_bytes_month_list(2019, 1)
    