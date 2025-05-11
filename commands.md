
# Convert Pcap-File to CSV-File (Must use Linux)
./go-flows run features pcap2pkts.json export csv mawi_team13.csv source libpcap mawi_team13.pcap

./go-flows run features pcap2pkts.json export csv team13_A.csv source libpcap team13_A.pcap
./go-flows run features pcap2flows.json export csv team13_A_Flows.csv source libpcap team13_A.pcap