from abc import ABC, abstractmethod


class Process:
    """Represents a single process."""

    def __init__(self, process_id: str, arrival_time: float, burst_time: float):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.turnaround_time = 0
        self.waiting_time = 0

    def update_times(self, start_time: float):
        self.waiting_time = max(0, start_time - self.arrival_time)
        self.turnaround_time = self.waiting_time + self.burst_time


class Scheduler(ABC):
    """Abstract base class for scheduling algorithms."""

    def __init__(self, process_list: list[Process]):
        self.process_list = process_list
        self.current_time = 0
        self.completed_processes = []

    @abstractmethod
    def execute(self):
        pass

    def update(self, process: Process):
        process.update_times(self.current_time)
        self.current_time += process.burst_time
        self.completed_processes.append(process)

    def show(self):
        """Prints the process list information."""
        print("{:>12}{:>15}{:>13}{:>18}{:>15}".format("Process ID",
                                                      "Arrival Time", "Burst Time", "Turnaround Time", "Waiting Time"))
        for process in self.completed_processes:
            print(f"{process.process_id:>12}{process.arrival_time:>15}{process.burst_time:>13}{process.turnaround_time:>18}{process.waiting_time:>15}")


class FCFS(Scheduler):
    """First-Come, First-Served (FCFS) scheduling algorithm."""

    def __init__(self, process_list: list[Process]):
        super().__init__(process_list)

    def execute(self):
        self.process_list.sort(key=lambda process: process.arrival_time)
        for process in self.process_list:
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            self.update(process)

def main():
    process_list = [
        Process("P1", 0, 7),
        Process("P2", 0, 4),
        Process("P3", 0, 1),
        Process("P4", 0, 4),
    ]

    print("FCFS Scheduling:")
    fcfs = FCFS(process_list[:])
    fcfs.execute()
    fcfs.show()

if __name__ == "__main__":
    main()
