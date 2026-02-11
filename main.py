import psutil
import time
import os

# ANSI escape codes for coloring text in the terminal
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def get_network_usage():
    """Returns total bytes (sent + received) since boot."""
    io = psutil.net_io_counters()
    return io.bytes_sent + io.bytes_recv

def learn_baseline(seconds=10):
    """Watches traffic for a few seconds to learn what is 'normal'."""
    print(f"{GREEN}🧠 LEARNING PHASE: Analyzing your network for {seconds} seconds...{RESET}")
    
    readings = []
    old_value = get_network_usage()
    
    for _ in range(seconds):
        time.sleep(1)
        new_value = get_network_usage()
        
        speed = (new_value - old_value) / 1024  # KB/s
        readings.append(speed)
        
        print(f"   ... Sample: {speed:.2f} KB/s")
        old_value = new_value

    # Calculate average
    avg_speed = sum(readings) / len(readings)
    print(f"{GREEN}✅ BASELINE SET: Average normal traffic is {avg_speed:.2f} KB/s{RESET}")
    return avg_speed

def start_guard():
    # 1. Learn what is normal for YOUR computer
    baseline = learn_baseline(seconds=5) # fast 5s learning for testing
    
    # 2. Set the "Trap" (Threshold)
    # If traffic is 100 KB/s higher than average, we alert.
    # (In a real scenario, you might use standard deviations, but this is great for a start)
    threshold = baseline + 100 
    print(f"🛡️  Intelligent-Guard Active. Alert Threshold: > {threshold:.2f} KB/s")
    print("-------------------------------------------------------")

    old_value = get_network_usage()

    while True:
        time.sleep(1)
        new_value = get_network_usage()
        
        speed = (new_value - old_value) / 1024
        
        # 3. The "AI" Decision Logic
        if speed > threshold:
            print(f"{RED}⚠️  ANOMALY DETECTED! Traffic Spike: {speed:.2f} KB/s{RESET}")
        else:
            print(f"   Normal Activity: {speed:.2f} KB/s")
            
        old_value = new_value

if __name__ == "__main__":
    try:
        start_guard()
    except KeyboardInterrupt:
        print("\n🛑 Guard Deactivated.")