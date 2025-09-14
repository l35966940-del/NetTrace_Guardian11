import time
from collections import deque

class FirewallLiveResponse:
    """
    Simulates a live response system for a firewall detecting DDoS attacks.
    """
    def __init__(self, syn_threshold=100, udp_threshold=500, icmp_threshold=500):
        self.syn_threshold = syn_threshold
        self.udp_threshold = udp_threshold
        self.icmp_threshold = icmp_threshold
        self.syn_requests = deque(maxlen=self.syn_threshold + 10)
        self.udp_packets = deque(maxlen=self.udp_threshold + 10)
        self.icmp_packets = deque(maxlen=self.icmp_threshold + 10)

    def _check_flood(self, packet_type, packet_queue, threshold):
        """
        Generic method to check for a flood of a specific packet type.
        """
        now = time.time()
        # Remove packets older than 1 second to create a rolling window
        while packet_queue and packet_queue[0]['timestamp'] < now - 1:
            packet_queue.popleft()
        
        if len(packet_queue) > threshold:
            print(f"🚨 **ALERT:** Potential {packet_type.upper()} Flood detected!")
            print(f"**Trigger:** Rate of {len(packet_queue)} {packet_type} packets/sec exceeds threshold of {threshold}.")
            return True
        return False

    def process_packet(self, packet):
        """
        Processes an incoming network packet and checks for flood attacks.
        """
        packet_type = packet.get('type').lower()
        packet['timestamp'] = time.time()

        if packet_type == 'syn':
            self.syn_requests.append(packet)
            if self._check_flood('SYN', self.syn_requests, self.syn_threshold):
                self.live_response_action("SYN Flood")
        elif packet_type == 'udp':
            self.udp_packets.append(packet)
            if self._check_flood('UDP', self.udp_packets, self.udp_threshold):
                self.live_response_action("UDP Flood")
        elif packet_type == 'icmp':
            self.icmp_packets.append(packet)
            if self._check_flood('ICMP', self.icmp_packets, self.icmp_threshold):
                self.live_response_action("ICMP Flood")

    def live_response_action(self, attack_type):
        """
        Signals the system to take a live response action.
        This function would contain the actual logic for mitigation,
        such as blocking an IP address, rate-limiting traffic, or
        notifying an administrator.
        """
        print(f"🛑 **LIVE RESPONSE ACTION TRIGGERED:** Initiating mitigation for {attack_type}.")
        # Example mitigation actions (these are placeholders)
        if attack_type == "SYN Flood":
            print("  - Dropping incomplete SYN connections.")
            print("  - Implementing SYN cookies to validate connections.")
        elif attack_type == "UDP Flood":
            print("  - Blocking source IPs with high UDP packet rates.")
            print("  - Rate-limiting UDP traffic to specific ports.")
        elif attack_type == "ICMP Flood":
            print("  - Disabling ICMP echo responses.")
            print("  - Implementing ICMP packet rate-limiting.")
        print("-" * 50)


# --- Example Usage ---

# Initialize the firewall system with specified thresholds
firewall = FirewallLiveResponse(syn_threshold=5, udp_threshold=10, icmp_threshold=10)

print("--- Simulating a SYN Flood attack ---")
for i in range(10):
    firewall.process_packet({'type': 'syn', 'source_ip': f'192.168.1.100', 'data': f'Packet {i+1}'})
    time.sleep(0.1) # Simulate arrival time

print("\n--- Simulating a UDP Flood attack ---")
for i in range(20):
    firewall.process_packet({'type': 'udp', 'source_ip': f'192.168.1.200', 'data': f'Packet {i+1}'})
    time.sleep(0.05) # Simulate faster arrival

print("\n--- Simulating an ICMP Flood attack ---")
for i in range(20):
    firewall.process_packet({'type': 'icmp', 'source_ip': f'192.168.1.200', 'data': f'Packet {i+1}'})
    time.sleep(0.05) # Simulate faster arrival