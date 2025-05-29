import ipaddress
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd



def extract_column(dataset, column_name):
    """
    Extracts a column from the dataset and returns it as a list of floats.
    """
    column_data = dataset[column_name].tolist()
    return column_data

def create_scatter_plot(csv_file, title=""):
    # Extract Data Lists needed
    dataset = pd.read_csv(csv_file)

    srcIP_list = extract_column(dataset, "sourceIPAddress")
    dstIP_list = extract_column(dataset, "destinationIPAddress")
    dstPort_list = extract_column(dataset, "destinationTransportPort")

    srcIP_int_list = [int(ipaddress.IPv4Address(ip)) for ip in srcIP_list]
    dstIP_int_list = [int(ipaddress.IPv4Address(ip)) for ip in dstIP_list]

    # Create subplots for boxplot (2 rows x 4 columns)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(title, fontsize=14, weight='bold')

    # Plot: x-axis: srcIP , y-axis: dstIP
    x = np.array(srcIP_int_list)
    y = np.array(dstIP_int_list)

    ax = axes[0]
    ax.scatter(x, y, c='blue', alpha=0.1, edgecolors='black')
    ax.set_title('Scatter Plot of Source vs Destination IPs')
    ax.set_xlabel('Source IP (as integer)')
    ax.set_ylabel('Destination IP (as integer)')

    # Plot: x-axis: x-axis: srcIP , y-axis: dstPort
    x = np.array(srcIP_int_list)
    y = np.array(dstPort_list)

    ax = axes[1]
    ax.scatter(x, y, c='blue', alpha=0.1, edgecolors='black')
    ax.set_xlabel('Source IP (as integer)')
    ax.set_ylabel('Destination Port (as integer)')
    ax.set_title('Scatter Plot of Source vs Destination Port')

    # Plot: x-axis: x-axis: dstIP , y-axis: dstPort
    x = np.array(dstIP_int_list)
    y = np.array(dstPort_list)

    ax = axes[2]
    ax.scatter(x, y, c='blue', alpha=0.1, edgecolors='black')
    ax.set_xlabel('Destination IP (as integer)')
    ax.set_ylabel('Destination Port (as integer)')
    ax.set_title('Scatter Plot of Destination vs Destination Port')

    plt.tight_layout()
    plt.show()

def find_IP_with_max_traffic(csv_file):
    # Extract Data Lists needed
    dataset = pd.read_csv(csv_file)

    srcIP_list = extract_column(dataset, "sourceIPAddress")
    dstIP_list = extract_column(dataset, "destinationIPAddress")

    # FInd dst IP with most incoming traffic:
    dstIP_cnt_dict = {}

    for dstIP, srcIP in zip(srcIP_list, dstIP_list):
        if dstIP not in dstIP_cnt_dict:
            dstIP_cnt_dict[dstIP] = 0
        dstIP_cnt_dict[dstIP] += 1

    # Get IP with highest incoming traffic 
    dstIP_max_traffi = ""
    dstIP_traffi_cnt = 0
    for key in dstIP_cnt_dict:
        if dstIP_cnt_dict[key] > dstIP_traffi_cnt:
            dstIP_max_traffi = key
            dstIP_traffi_cnt = dstIP_cnt_dict[key]

    print(f"Targeted dstIP {dstIP_max_traffi}: cnt = {dstIP_traffi_cnt}")

    # FInd src IP with most outgoing traffic:
    srcIP_cnt_dict = {}

    for dstIP, srcIP in zip(srcIP_list, dstIP_list):
        if srcIP not in srcIP_cnt_dict:
            srcIP_cnt_dict[srcIP] = 0
        srcIP_cnt_dict[srcIP] += 1

    # Get IP with highest outgoing traffic
    srcIP_max_traffi = ""
    srcIP_traffi_cnt = 0
    for key in srcIP_cnt_dict:
        if srcIP_cnt_dict[key] > srcIP_traffi_cnt:
            srcIP_max_traffi = key
            srcIP_traffi_cnt = srcIP_cnt_dict[key]

    print(f"Scanning srcIP {srcIP_max_traffi}: cnt = {srcIP_traffi_cnt}")

if __name__ == "__main__":
    team13_A_file = "workfiles/team13_A.csv"
    team13_B_file = "workfiles/team13_B.csv"
    team13_C_file = "workfiles/team13_C.csv"

    # =================================================================================
    # === Part 3: rep-24
    # =================================================================================
    create_scatter_plot(team13_A_file, title="Traffic A")

    # =================================================================================
    # === Part 3: rep-25
    # =================================================================================
    create_scatter_plot(team13_B_file, title="Traffic B")
    find_IP_with_max_traffic(team13_B_file)

    # =================================================================================
    # === Part 3: rep-26
    # =================================================================================
    create_scatter_plot(team13_C_file, title="Traffic C")
    find_IP_with_max_traffic(team13_C_file)

    # print(int(ipaddress.IPv4Address("74.175.232.177")))
    


    