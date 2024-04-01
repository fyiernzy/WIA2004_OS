import math


class File:
    def __init__(self, size: int, name: str):
        self.size = size
        self.name = name


class Disk:
    FREE = 0
    OCCUPIED = 1
    _instance = None

    @staticmethod
    def get_instance():
        if Disk._instance is None:
            Disk._instance = Disk()
        return Disk._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.total_size = 12288  # Disk size in bytes
            self.block_size = 512    # Block size in bytes
            self.total_blocks = self.total_size // self.block_size
            self.block_status = [Disk.FREE] * self.total_blocks
            self.free_blocks = self.total_blocks
            self.file_registry = {}

    def add_file(self, file_name, start_block, blocks_used):

        if file_name in self.file_registry:
            raise ValueError(f"File '{file_name}' already exists.")

        self.file_registry[file_name] = {
            "start_block": start_block,
            "blocks_used": blocks_used
        }

        self.update_block_status(start_block, blocks_used, Disk.OCCUPIED)

    def delete_file(self, file_name):
        if file_name not in self.file_registry:
            raise KeyError(f"File '{file_name}' not found.")
        file_info = self.file_registry.pop(file_name)
        self.update_block_status(
            file_info["start_block"], file_info["blocks_used"], Disk.FREE)

    def update_block_status(self, start_block, blocks_used, status):
        for i in range(blocks_used):
            self.block_status[start_block + i] = status
        self.free_blocks += blocks_used if status == Disk.FREE else -blocks_used


class FileManager:
    """Manages file allocations on the disk."""

    def allocate(self, file: File):
        disk = Disk.get_instance()
        needed_blocks = math.ceil(file.size / disk.block_size)

        if needed_blocks > disk.free_blocks:
            # print("Not enough space.")
            return False

        for start_block in range(disk.total_blocks - needed_blocks + 1):
            if all(disk.block_status[i] == Disk.FREE for i in range(start_block, start_block + needed_blocks)):
                disk.add_file(file.name, start_block, needed_blocks)
                # print(f"Allocated {file.name}")
                return True

        return False

    def delete(self, file_name: str):
        try:
            Disk.get_instance().delete_file(file_name)
            # print(f"Deleted {file_name}")
        except KeyError as e:
            print(e)


def main():
    fm = FileManager()
    operations = ['add-file1-1024', 'add-file2-1024', 'add-file3-4098',
                  'add-file4-5120', 'del-file1', 'del-file2', 'add-file5-1024']
    for opr in operations:
        action, name, *size = opr.split("-")
        if action == 'add':
            fm.allocate(File(int(size[0]), name))
        elif action == 'del':
            fm.delete(name)

    print(Disk.get_instance().file_registry)


if __name__ == '__main__':
    main()
