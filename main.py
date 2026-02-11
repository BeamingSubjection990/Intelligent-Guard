import psutil
import time

def start_guard():
    print("🛡️ Intelligent-Guard is Active...")
    print("Press CTRL+C to stop monitoring.")
    
    # Take a snapshot of total network traffic right now
    old_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

    while True:
        # Wait 1 second before checking again
        time.sleep(1)
        
        # Take a new snapshot
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        
        # Calculate the difference (Data used in the last second)
        usage_bytes = new_value - old_value
        usage_kb = usage_bytes / 1024  # Convert to Kilobytes

        # Display the traffic
        print(f"Network Traffic: {usage_kb:.2f} KB/s")

        # Update the snapshot for the next loop
        old_value = new_value

if __name__ == "__main__":
    start_guard()