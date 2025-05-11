import csv
import json
from collections import Counter

if __name__ == "__main__":
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
