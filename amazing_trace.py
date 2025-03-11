import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import time
import os
import subprocess
import platform
import re

def execute_traceroute(destination):
    system_platform = platform.system().lower() #lowers all the characters to clean up the destination
    try: #trys
        # Add the -I flag for ICMP packets
        routed = subprocess.run(["traceroute", "-I", destination], capture_output=True, text=True, check=True) #sends a traceroute request to the destination
        # print(routed.stdout)  # Print actual traceroute output
        return routed.stdout  # Return output for further processing #returns the output as a standard output

    except subprocess.CalledProcessError as e:
        print(f"Error executing traceroute: {e}")
        return None

        """
        Executes a traceroute to the specified destination and returns the output.

        Args:
            destination (str): The hostname or IP address to trace

        Returns:
            str: The raw output from the traceroute command
        """
    # Your code here
    # Hint: Use the subprocess module to run the traceroute command
    # Make sure to handle potential errors

    # Remove this line once you implement the function,
    # and don't forget to *return* the output
    pass


def parse_traceroute(traceroute_output): #defines the function and takes in the output from our traceroute
    hops_results = [] #sets up an array for our hops dictionaries
    lines = traceroute_output.splitlines() #creates lines variable that is equal to the traceroute output splits on lines

    for line in lines: #sets up loop for line in lines
        pieces = line.split() #sets variable pieces equal to the lines split
        if len(pieces) < 2: #if the length of pieces is less than 2 then there is a problem
            continue  # Skip malformed lines

        print(pieces)  # Debugging output

        try: #trys
            hop_num = int(pieces[0])  #Takes the first index and sets it as an itegar because it is our hop number

            # Initialize IP and hostname
            ip, hostname = None, None #starts ip and hostname as nothing to start off

            # Look for timeout pattern ('*')
            if pieces[1:4] == ['*', '*', '*']: #if indexs 1-4 are "*" then ip and hostname should be none
                ip = None #ip is none
                hostname = None #hostname is none
                rtt_values = [None if part == '*' else None for part in pieces[2:]]  #makes all RTTs are None for timeouts
            else:
                if pieces[1] == "*" and pieces[2] != "*": #if index 1 is an "*" and piece 2 is not an "*" then we move the "*" to the end and continue
                    pieces.pop(1)  #Removes the first "*"
                    pieces.append("*")  #Add one "*" at the end

                # Look for IP in parentheses (e.g., "router1 (10.0.0.1)")
                match = re.search(r'\(([\d\.]+)\)', line) #serches for parenthesis
                if match: #if there is one
                    ip = match.group(1)  # Extract IP inside parentheses
                    possible_hostname = pieces[1] #the possible hostname is index 1
                    if possible_hostname != ip: #if the possible hostname isnt equal to the ip then
                        hostname = possible_hostname  #Assign hostname only if it's different from IP

                # If no parentheses, check if second item is an IP
                elif re.match(r'^\d+\.\d+\.\d+\.\d+$', pieces[1]): #else if match
                    ip = pieces[1] #set ip to index 1

                # If second item is not an IP, treat it as a hostname
                elif re.match(r'^[a-zA-Z0-9.-]+$', pieces[1]): #else if match with letters
                    hostname = pieces[1] #set hostname to index 1

                # Handle RTTs (remove 'ms' and handle timeouts *)
                rtt_values = [] #set up empty array for our route times
                for part in pieces[2:]: #loop for every part in pieces 2 or more
                    if part == '*': #if part is "*" 
                        rtt_values.append(None)  # Timeout case
                    else:
                        try:
                            rtt_values.append(float(part))  # Convert RTTs to float
                        except ValueError:
                            continue  # Ignore non-numeric values

            # Ensure RTT list has exactly 3 values, filling with None if necessary
            while len(rtt_values) < 3:
                rtt_values.append(None)

            # Append the parsed hop
            hops_results.append({
                'hop': hop_num, #sets up hop in our dictionary
                'ip': ip, #sets up ip in our dictionary
                'hostname': hostname, #sets up hostname in our dictionary
                'rtt': rtt_values #sets up route times in our dictionary
            })

        except ValueError:
            print("Error parsing line:", line)
            continue  # Skip malformed lines

    print(hops_results)  # Debugging output
    return hops_results




    """
    Parses the raw traceroute output into a structured format.

    Args:
        traceroute_output (str): Raw output from the traceroute command

    Returns:
        list: A list of dictionaries, each containing information about a hop:
            - 'hop': The hop number (int)
            - 'ip': The IP address of the router (str or None if timeout)
            - 'hostname': The hostname of the router (str or None if same as ip)
            - 'rtt': List of round-trip times in ms (list of floats, None for timeouts)

    Example:
    ```
        [
            {
                'hop': 1,
                'ip': '172.21.160.1',
                'hostname': 'HELDMANBACK.mshome.net',
                'rtt': [0.334, 0.311, 0.302]
            },
            {
                'hop': 2,
                'ip': '10.103.29.254',
                'hostname': None,
                'rtt': [3.638, 3.630, 3.624]
            },
            {
                'hop': 3,
                'ip': None,  # For timeout/asterisk
                'hostname': None,
                'rtt': [None, None, None]
            }
        ]
    ```
    """
    # Your code here
    # Hint: Use regular expressions to extract the relevant information
    # Handle timeouts (asterisks) appropriately

    # Remove this line once you implement the function,
    # and don't forget to *return* the output
    pass

# ============================================================================ #
#                    DO NOT MODIFY THE CODE BELOW THIS LINE                    #
# ============================================================================ #
def visualize_traceroute(destination, num_traces=3, interval=5, output_dir='output'):
    """
    Runs multiple traceroutes to a destination and visualizes the results.

    Args:
        destination (str): The hostname or IP address to trace
        num_traces (int): Number of traces to run
        interval (int): Interval between traces in seconds
        output_dir (str): Directory to save the output plot

    Returns:
        tuple: (DataFrame with trace data, path to the saved plot)
    """
    all_hops = []

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Running {num_traces} traceroutes to {destination}...")

    for i in range(num_traces):
        if i > 0:
            print(f"Waiting {interval} seconds before next trace...")
            time.sleep(interval)

        print(f"Trace {i+1}/{num_traces}...")
        output = execute_traceroute(destination)
        hops = parse_traceroute(output)

        # Add timestamp and trace number
        timestamp = time.strftime("%H:%M:%S")
        for hop in hops:
            hop['trace_num'] = i + 1
            hop['timestamp'] = timestamp
            all_hops.append(hop)

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_hops)

    # Calculate average RTT for each hop (excluding timeouts)
    df['avg_rtt'] = df['rtt'].apply(lambda x: np.mean([r for r in x if r is not None]) if any(r is not None for r in x) else None)

    # Plot the results
    plt.figure(figsize=(12, 6))

    # Create a subplot for RTT by hop
    ax1 = plt.subplot(1, 1, 1)

    # Group by trace number and hop number
    for trace_num in range(1, num_traces + 1):
        trace_data = df[df['trace_num'] == trace_num]

        # Plot each trace with a different color
        ax1.plot(trace_data['hop'], trace_data['avg_rtt'], 'o-',
                label=f'Trace {trace_num} ({trace_data.iloc[0]["timestamp"]})')

    # Add labels and legend
    ax1.set_xlabel('Hop Number')
    ax1.set_ylabel('Average Round Trip Time (ms)')
    ax1.set_title(f'Traceroute Analysis for {destination}')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Make sure hop numbers are integers
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()

    # Save the plot to a file instead of displaying it
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_dest = destination.replace('.', '-')
    output_file = os.path.join(output_dir, f"trace_{safe_dest}_{timestamp}.png")
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to: {output_file}")

    # Return the dataframe and the path to the saved plot
    return df, output_file

# Test the functions
if __name__ == "__main__":
    # Test destinations
    destinations = [
        "google.com",
        "amazon.com",
        "bbc.co.uk"  # International site
    ]

    for dest in destinations:
        df, plot_path = visualize_traceroute(dest, num_traces=3, interval=5)
        print(f"\nAverage RTT by hop for {dest}:")
        avg_by_hop = df.groupby('hop')['avg_rtt'].mean()
        print(avg_by_hop)
        print("\n" + "-"*50 + "\n")

    execute_traceroute("google.com")