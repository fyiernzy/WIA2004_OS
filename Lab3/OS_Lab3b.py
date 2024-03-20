import math

BLOCK_SIZE = 512


class File:
    def __init__(self, size: int, name: str):
        self.size = size
        self.name = name


class Disk:
    FREE = 0
    OCCUPIED = 1

    def __init__(self):
        self.total_blocks = 24
        self.block_status = [Disk.FREE] * self.total_blocks
        self.free_blocks = self.total_blocks
        self.file_registry = {}

    def add_file(self, file_name, start_block, blocks_used):
        self.file_registry[file_name] = {
            "start_block": start_block,
            "blocks_used": blocks_used
        }

        self.update_block_status(start_block, blocks_used, Disk.OCCUPIED)

    def update_block_status(self, start_block, blocks_used, status):
        for i in range(blocks_used):
            self.block_status[start_block + i] = status
        self.free_blocks += blocks_used if status == Disk.FREE else -blocks_used

    def show(self):
        print("{:>10} {:>12} {:>11}".format(
            "File Name", "Start Block", "Blocks Used"))
        
        for file_name, details in self.file_registry.items():
            print("{:>10} {:>12} {:>11}".format(
                file_name, details['start_block'], details['blocks_used']))


class FileManager:
    def __init__(self, disk: Disk):
        self.disk = disk

    def allocate(self, file: File):
        needed_blocks = math.ceil(file.size / BLOCK_SIZE)

        if needed_blocks > self.disk.free_blocks:
            return False

        for start_block in range(self.disk.total_blocks - needed_blocks + 1):
            if all(self.disk.block_status[i] == Disk.FREE for i in range(start_block, start_block + needed_blocks)):
                self.disk.add_file(file.name, start_block, needed_blocks)
                return True

        return False


def main():
    disk = Disk()
    fm = FileManager(disk)
    files = [File(1024, "file1"), File(1024, "file2"),
             File(4098, "file3"), File(5120, "file4"), File(5120, "file5")]
    for file in files:
        fm.allocate(file)
    disk.show()


if __name__ == '__main__':
    main()
