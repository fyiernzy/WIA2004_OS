import numpy as np
from utilities.table_formatter import TableFormatter


class Sequence:
    def __init__(self, process_id: str, need, allocation, available_before, available_after):
        self.process_id = process_id
        self.need = need
        self.allocation = allocation
        self.available_before = available_before
        self.available_after = available_after


class Case:
    def __init__(self, case_id: str, available, allocation, max_workload):
        self.case_id = case_id
        self.available = available
        self.allocation = allocation
        self.max_workload = max_workload

    def run(self):
        print(f"Case - {self.case_id}")
        banker = Banker.create_banker(
            self.available, self.allocation, self.max_workload)
        banker.run_allocation()
        banker.show_run_result()
        print()


class Banker:
    def __init__(self, available: np.array, allocation: np.array, max_workload: np.array):
        self.available = available
        self.allocation = allocation
        self.max_workload = max_workload
        self.need = max_workload - allocation
        self.status = np.zeros(allocation.shape[0], dtype=int)
        self.sequence_table = []

    @classmethod
    def create_banker(cls, available, allocation, max_workload):
        available_arr = np.array(available, dtype=int)
        allocation_arr = np.array(allocation, dtype=int)
        max_workload_arr = np.array(max_workload, dtype=int)

        # Validate shapes to ensure 'available' matches the resource count and 'allocation' matches 'max_workload'
        if available_arr.ndim != 1:
            raise ValueError("Available resources must be a 1D array.")
        if allocation_arr.shape != max_workload_arr.shape:
            raise ValueError(
                "Allocation and max_workload arrays must have the same shape.")
        if available_arr.size != allocation_arr.shape[1]:
            raise ValueError(
                "The size of 'available' must match the number of resources in 'allocation'.")

        return cls(available_arr, allocation_arr, max_workload_arr)

    def is_allocation_safe(self, process_index):
        """Check if allocating resources to the given process is safe."""
        need = self.need[process_index]
        return np.all(need <= self.available)

    def update_resources(self, process_index):
        """Update resources after allocating to the specified process."""
        available_before = np.array(self.available)
        self.available += self.allocation[process_index]
        self.status[process_index] = 1
        available_after = np.array(self.available)
        self.sequence_table.append(Sequence(
            f'P{process_index}', self.need[process_index], self.allocation[process_index], available_before, available_after))

    def run_allocation(self):
        """Attempt to allocate resources to all processes safely."""
        try:
            while not np.all(self.status):
                for i in range(len(self.status)):
                    if not self.status[i] and self.is_allocation_safe(i):
                        self.update_resources(i)

            if np.all(self.status):
                print("All processes have been allocated resources successfully.")
            else:
                print("Unable to allocate resources to all processes safely.")
        except Exception as e:
            print(f"An error occurred during allocation: {e}")

    def show_run_result(self):
        # Prepare data for the table
        headers = ["Process ID", "Need", "Allocation",
                   "Available (Before)", "Available (After)"]
        rows = []

        for seq in self.sequence_table:
            row = [seq.process_id, np.array2string(seq.need), np.array2string(seq.allocation),
                   np.array2string(seq.available_before), np.array2string(seq.available_after)]
            rows.append(row)

        # Create and display the table
        table_formatter = TableFormatter(headers, rows)
        table_formatter.display_table()


def main():
    Case('case1',
         available=[3, 3, 2],
         allocation=[[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [
                     0, 0, 2]],
         max_workload=[[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]).run()

    Case('case2',
         available=[1, 5, 2, 0],
         allocation=[[0, 0, 1, 2], [1, 0, 0, 0], [
             1, 3, 5, 4], [0, 6, 3, 2], [0, 0, 1, 4]],
         max_workload=[[0, 0, 1, 2], [1, 7, 5, 0], [2, 3, 5, 6], [0, 6, 5, 2], [0, 6, 5, 6]]).run()


if __name__ == '__main__':
    main()
