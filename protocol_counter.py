import csv
from collections import Counter

def count_protocol_identifiers(csv_file_path):
    protocol_counts = Counter()

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            protocol_id = row.get('protocolIdentifier')
            if protocol_id is not None:
                protocol_counts[protocol_id] += 1

    return protocol_counts

if __name__ == "__main__":
    # Replace with your CSV file path
    file_path = "mawi_team13.csv"
    counts = count_protocol_identifiers(file_path)
    for protocol, count in counts.items():
        print(f"Protocol {protocol}: {count} occurrences")
