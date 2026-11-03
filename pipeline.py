import time
import random
import json
import re
import argparse
from datetime import datetime

TARGET_PROFILES = {
    "vpn": {
        "log_path": "simulated_vpn.log",
        "indicators": ["KILLSWITCH_DEADLOCK", "CAPTIVE_PORTAL_BLOCK", "PACKET_JITTER_DROP"],
        "playbook": {
            "KILLSWITCH_DEADLOCK": (
                "1. Force-close stuck VPN processes. "
                "2. Flush DNS cache and reset TCP/IP & Winsock stacks. "
                "3. Verify virtual adapter state."
            ),
            "CAPTIVE_PORTAL_BLOCK": (
                "1. Disable VPN virtual adapter and set DNS to automatic. "
                "2. Authenticate via local captive portal. "
                "3. Re-enable VPN using Standard Kill Switch."
            ),
            "PACKET_JITTER_DROP": (
                "1. Audit local network stability. "
                "2. Switch VPN protocol from UDP to TCP or Stealth to tolerate jitter."
            )
        },
        "sample_events": [
            "INFO: Tunnel established via WireGuard on interface tun0.",
            "WARN: High latency detected on local gateway 192.168.1.1.",
            "ERROR: [KILLSWITCH_DEADLOCK] Virtual adapter tap0 unresponsive; traffic halted.",
            "ERROR: [CAPTIVE_PORTAL_BLOCK] DNS resolution hijacked by 10.0.0.1; handshake stalled.",
            "CRITICAL: [PACKET_JITTER_DROP] Keepalive timeout exceeded on 185.159.157.1."
        ]
    },
    
    "ssh": {
        "log_path": "simulated_auth.log",
        "indicators": ["FAILED_LOGIN", "ROOT_BRUTE_FORCE"],
        "playbook": {
            "FAILED_LOGIN": "Verify user credentials and check source IP against known subnet.",
            "ROOT_BRUTE_FORCE": "Block source IP via ufw/iptables and disable PermitRootLogin in sshd_config."
        },
        "sample_events": [
            "INFO: Accepted publickey for user from 192.168.1.50 port 54322 ssh2",
            "WARN: [FAILED_LOGIN] Failed password for invalid user admin from 203.0.113.42 port 39102",
            "CRITICAL: [ROOT_BRUTE_FORCE] 50 failed login attempts for root from 198.51.100.17"
        ]
    }
}

def generate_synthetic_logs(target_key, iterations=5, delay=2):
    """Generates synthetic log entries based on the selected target profile."""
    
    if target_key not in TARGET_PROFILES:
        print(f"[!] Error: Target '{target_key}' is not configured.")
        return

    profile = TARGET_PROFILES[target_key]
    log_file = profile["log_path"]
    events = profile["sample_events"]

    print(f"[*] Starting Log Generator for target: '{target_key.upper()}' -> Writing to {log_file}")

    for _ in range(iterations):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chosen_event = random.choice(events)
        log_entry = f"{timestamp} | {chosen_event}\n"

        with open(log_file, "a") as file:
            file.write(log_entry)
            
        print(f"  [+] Logged: {log_entry.strip()}")
        time.sleep(delay)

def tail_log(log_path):
    """Acts like 'tail -f' in Linux, yielding new lines as they are written."""
    
    with open(log_path, "r") as file:
        file.seek(0, 2)
        
        while True:
            line = file.readline() 
            
            if not line:
                time.sleep(0.5)
                continue
                
            yield(line) 

def scan_for_threats(log_line, target_indicators):
    """Checks if a new log line contains any of our known threat indicators."""
    
    for indicator in target_indicators:
        if indicator in log_line:
            return indicator
            
    return None

def extract_iocs(log_line):
    """Uses Regular Expressions (regex) to isolate IPs and specific fault codes."""
    
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    indicator_pattern = r"\[(.*?)\]"
    
    extracted_ips = re.findall(ip_pattern, log_line) 
    extracted_indicators = re.findall(indicator_pattern, log_line) 
    
    return {
        "source_ip": extracted_ips[0] if extracted_ips else "Unknown",
        "fault_code": extracted_indicators[0] if extracted_indicators else "Unknown"
    }

def format_alert(extracted_data, playbook_steps):
    """Translates extracted IOCs and playbook rules into a structured JSON alert."""
    
    alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    alert_payload = {
        "timestamp": alert_time,
        "target_ip": extracted_data["source_ip"], 
        "detected_anomaly": extracted_data["fault_code"],
        "recommended_action": playbook_steps 
    }
    
    formatted_json = json.dumps(alert_payload, indent=4)
    
    return formatted_json

def main():
    """Central execution block for the detection pipeline."""
    parser = argparse.ArgumentParser(description="Unified Detection Pipeline")
    parser.add_argument("--target", required=True, help="Target profile (e.g., vpn, ssh)")
    parser.add_argument("--test", action="store_true", help="Generate synthetic logs before scanning")
    args = parser.parse_args()

    target = args.target.lower()
    
    if target not in TARGET_PROFILES:
        print(f"[!] Error: Target '{target}' is not configured.")
        return

    if args.test:
        generate_synthetic_logs(target)

    profile = TARGET_PROFILES[target]
    print(f"[*] Monitoring {profile['log_path']} for {target.upper()} threats...")

    if args.test:
        with open(profile["log_path"], "r") as file:
            for line in file:
                threat = scan_for_threats(line, profile["indicators"])
                if threat:
                    extracted_data = extract_iocs(line)
                    playbook_steps = profile["playbook"].get(threat, "No resolution mapped.")
                    final_alert = format_alert(extracted_data, playbook_steps)
                    print("\n[!] THREAT DETECTED:")
                    print(final_alert)
    else:
        for line in tail_log(profile["log_path"]):
            threat = scan_for_threats(line, profile["indicators"])
            if threat:
                extracted_data = extract_iocs(line)
                playbook_steps = profile["playbook"].get(threat, "No resolution mapped.")
                final_alert = format_alert(extracted_data, playbook_steps)
                print("\n[!] THREAT DETECTED:")
                print(final_alert)

if __name__ == "__main__":
    main()
