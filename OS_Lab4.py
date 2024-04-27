class Process:
    def __init__(self, process_id: str, process_size: int):
        self.id = process_id
        self.size = process_size


class Memory:
    FREE = 'Free'
    OCCUPIED = 'Occupied'

    def __init__(self):
        self.PARTITIONS = [15, 25, 20, 35, 30, 10, 50]
        self.block_registry = {f'B{i}': {
            'Block Size': size,
            'Status': Memory.FREE,
            'Process ID': None,
            'Process Size': None}
            for i, size in enumerate(self.PARTITIONS)}

    def allocate(self, block_id: str, process: Process):
        block = self.block_registry[block_id]
        block.update({
            'Status': Memory.OCCUPIED,
            'Process ID': process.id,
            'Process Size': process.size})


class BestFit():
    def process(self, memory, processes: list[Process]):
        for process in processes:
            best_fit_block_id, best_fit_size_diff = None, float('inf')

            for block_id, block in memory.block_registry.items():

                # If the block is free and has enough size to fit the process
                if block['Status'] == Memory.FREE and block['Block Size'] >= process.size:
                    size_diff = block['Block Size'] - process.size

                    # If the current block has smaller size difference than the previous best fit block
                    # then update the best fit block
                    if size_diff < best_fit_size_diff:
                        best_fit_block_id, best_fit_size_diff = block_id, size_diff

            # If there is a best fit block, allocate the process to the block
            if best_fit_block_id:
                memory.allocate(best_fit_block_id, process)


def show(memory):
    FORMAT = "{:<10} | {:<5} | {:<10} | {:<10} | {:<12} | {:<14}"
    header = FORMAT.format('Block ID', 'Size', 'Status',
                           'Process ID', 'Process Size', 'Internal Frag.')
    print(header)
    print('-' * len(header))

    for bid, info in memory.block_registry.items():
        bsize = info.get('Block Size')
        status = info.get('Status')
        pid = info.get('Process ID') or 'None'
        psize = info.get('Process Size') or 'None'
        internal_frag = 0 if status == Memory.FREE else bsize - psize
        line = FORMAT.format(bid, bsize, status, pid, psize, internal_frag)
        print(line)


def main():
    processes = [
        Process("P1", 10), Process("P2", 20), Process("P3", 30),
        Process("P4", 15), Process("P5", 5)
    ]

    memory = Memory()
    print("Best Fit:")
    BestFit().process(memory, processes)
    show(memory)


if __name__ == '__main__':
    main()
