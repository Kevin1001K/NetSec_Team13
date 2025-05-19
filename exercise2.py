import csv
import json

import numpy as np
import pandas as pd

def rep_12():
    # Replace with your CSV file path
    source_file = "workfiles/mawi_team13.csv"

    # loading data from CSV file
    dataset = pd.read_csv(source_file)

    protocolID_list = dataset["protocolIdentifier"].tolist()

    protocolID_dict = {}

    for protocolID in protocolID_list:
        if protocolID not in protocolID_dict:
            protocolID_dict[protocolID] = 0
        protocolID_dict[protocolID] += 1

    # Sort by numbers of tcp mode 
    keys = list(protocolID_dict.keys())
    values = list(protocolID_dict.values())
    sorted_value_index = np.argsort(values)
    protocolID_sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

    for key, value in protocolID_dict.items():
        print(f"Protocol {key}: {value}")

def rep_13():
    file_path = "Ex2flows_team13.csv"
    json_file = "result.json"

    flow_dict = {}

    cnt_src_ip = 0
    cnt_1_dst = 0
    cnt_10_dst = 0
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cnt_src_ip += 1

            num_dest_ip = int(row.get('distinct(destinationIPAddress)'))

            if num_dest_ip == 1:
                cnt_1_dst += 1
            elif num_dest_ip > 10:
                cnt_10_dst += 1

    cnt_1_dst_percent = cnt_1_dst/cnt_src_ip
    cnt_10_dst_percent = cnt_10_dst/cnt_src_ip
    
    # Save result into json
    with open(json_file, "w") as file:
        json.dump(flow_dict, file, indent="\t")

    print(f"# source ID: {cnt_src_ip}")
    print(f"# source ID with 1 destination IP: {cnt_1_dst}, {cnt_1_dst_percent}")
    print(f"# source ID with >10 destination IP: {cnt_10_dst}, {cnt_10_dst_percent}")

if __name__ == "__main__":
    # =================================================================================
    # === Part 1: rep-12
    # =================================================================================
    rep_12()

    # =================================================================================
    # === Part 2: rep-13
    # =================================================================================
    # rep_13()