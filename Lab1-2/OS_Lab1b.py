class Process:
    def __init__(self, process_id, burst_time):
        self.process_id = process_id
        self.burst_time = burst_time

def main():
    processes = [Process("P1", 7), Process("P2", 4), Process("P3", 1), Process("P4", 4)]
    print("FCFS Scheduling:")
    print("{:>5}{:>12}{:>13}".format("No", "Process ID","Burst Time"))
    for index, process in enumerate(processes, 1):
        print(f"{index:>5}{process.process_id:>12}{process.burst_time:>13}")

if __name__ == '__main__':
    main()