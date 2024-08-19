from scapy.all import sniff, IP, TCP, UDP, Raw

# Comprehensive mapping of protocol numbers to names
protocols = {
    1: "ICMP",
    2: "IGMP",
    6: "TCP",
    17: "UDP",
    41: "IPv6",
    43: "IPv6-Route",
    44: "IPv6-Frag",
    46: "RSVP",
    47: "GRE",
    50: "ESP",
    51: "AH",
    53: "SwIPe",
    55: "MOBILE",
    58: "IPv6-ICMP",
    59: "IPv6-NoNxt",
    60: "IPv6-Opts",
    61: "",
    63: "",
    88: "EIGRP",
    89: "OSPF",
    97: "ETHERIP",
    98: "ENCAP",
    99: "",
    107: "A/N",
    108: "IPComp",
    112: "VRRP",
    114: "",
    115: "L2TP",
    124: "IS-IS over IPv4",
    132: "SCTP",
    134: "RSVP-E2E-IGNORE",
    135: "Mobility Header",
    136: "UDPLite",
    137: "MPLS-in-IP",
    139: "HIP",
    143: "Ethernet",
}

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto

        proto_name = protocols.get(proto, f"Other ({proto})")

        print(f"IP Packet: {src_ip} -> {dst_ip} ({proto_name})")

        if packet.haslayer(TCP):
            try:
                payload = packet[Raw].load
                decoded_payload = payload.decode('utf-8', 'ignore')
                print(f"TCP Payload: {decoded_payload}")
            except (IndexError, UnicodeDecodeError):
                print("Unable to decode TCP payload.")
        elif packet.haslayer(UDP):
            try:
                payload = packet[Raw].load
                decoded_payload = payload.decode('utf-8', 'ignore')
                print(f"UDP Payload: {decoded_payload}")
            except (IndexError, UnicodeDecodeError):
                print("Unable to decode UDP payload.")
        else:
            print("No TCP/UDP Payload")
    else:
        print("Non-IP Packet")

def main():
    print("Starting packet sniffer for 30 minutes or 1500 packets...")
    sniff(prn=packet_callback, store=False, timeout=1800, count=1500)  # 30 minutes or 1500 packets, whichever comes first
    print("Sniffing stopped.")

if __name__ == "__main__":
    main()
