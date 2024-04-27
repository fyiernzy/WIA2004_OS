from abc import ABC, abstractmethod


class Process:
    def __init__(self, process_id: str, process_size: int):
        self.id = process_id
        self.size = process_size


class Memory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
            cls._instance.init_blocks()
        return cls._instance

    def init_blocks(self):
        self.PARTITIONS = [15, 25, 20, 35, 30, 10, 50]
        self.block_registry = {f'B{i}': {'Block Size': size, 'Status': 0, 'Process ID': None, 'Process Size': None}
                               for i, size in enumerate(self.PARTITIONS)}

    def allocate(self, block_id: str, process: Process):
        block = self.block_registry[block_id]
        block.update({'Status': 1, 'Process ID': process.id,
                     'Process Size': process.size})

    def clear(self):
        for block in self.block_registry.values():
            block.update(
                {'Status': 0, 'Process ID': None, 'Process Size': None})

    def show(self):
        header = f"{'Block ID':<10} | {'Size':<5} | {'Status':<10} | {'Process ID':<10} | {'Process Size':<12} | {'Internal Frag.':<14}"
        print(header)
        print('-' * len(header))  # Print a separator line
        for block_id, info in self.block_registry.items():
            status = 'Free' if info['Status'] == 0 else 'Occupied'
            internal_frag = 0 if info['Status'] == 0 else info['Block Size'] - (
                info['Process Size'] or 0)
            line = f"{block_id:<10} | {info['Block Size']:<5} | {status:<10} | {info['Process ID'] or 'None':<10} | {info['Process Size'] or 'None':<12} | {internal_frag:<14}"
            print(line)


class AllocationStrategy(ABC):

    @abstractmethod
    def process(self, processes: list[Process]):
        pass


class BestFit(AllocationStrategy):
    def process(self, processes: list[Process]):
        memory = Memory()
        for process in processes:
            best_fit_block_id, best_fit_size_diff = None, float('inf')
            for block_id, block in memory.block_registry.items():
                if block['Status'] == 0 and block['Block Size'] >= process.size:
                    size_diff = block['Block Size'] - process.size
                    if size_diff < best_fit_size_diff:
                        best_fit_block_id, best_fit_size_diff = block_id, size_diff
            if best_fit_block_id:
                memory.allocate(best_fit_block_id, process)


class FirstFit(AllocationStrategy):
    def process(self, processes: list[Process]):
        memory = Memory()
        for process in processes:
            for block_id, block in memory.block_registry.items():
                if block['Status'] == 0 and block['Block Size'] >= process.size:
                    memory.allocate(block_id, process)
                    break


def main():
    processes = [
        Process("P1", 10),
        Process("P2", 20),
        Process("P3", 30),
        Process("P4", 15),
        Process("P5", 5)
    ]

    print("Best Fit:")
    bf = BestFit()
    bf.process(processes)
    Memory().show()
    Memory().clear()

    print("\nFirst Fit:")
    ff = FirstFit()
    ff.process(processes)
    Memory().show()


if __name__ == '__main__':
    main()
