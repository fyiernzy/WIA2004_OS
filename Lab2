def main():
    n = int(input("Enter the number of processes: "))
    processes = []
    for i in range(n):
        burst_time = int(input(f"Enter burst time for process {i + 1}: "))
        # Create a Process object with an ID of (i + 1) and burst time entered by the user
        processes.append(Process((i + 1), burst_time)) 

    # Sort the processes according to their burst time
    processes = sorted(processes, key=lambda x: x.burst_time)

    calculate_waiting_time(processes)
    calculate_turnaround_time(processes)
    display_result(processes)


class Process:
    def __init__(self, process_id, burst_time):
        self.process_id = process_id
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0


def calculate_waiting_time(processes):
    wt = 0;
    for process in processes:
        process.waiting_time = wt
        wt += process.burst_time

def calculate_turnaround_time(processes):
    for process in processes:
        process.turnaround_time = process.waiting_time + process.burst_time

def display_result(processes):
    print("Processes  Burst Time  Waiting Time  Turnaround Time")
    
    for process in processes:
        print(f"{process.process_id}\t\t{process.burst_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")

main()
