from table_formatter import TableFormatter
from abc import ABC, abstractmethod


class Page:
    def __init__(self, vpn, content, access_bit=0):
        self.vpn = vpn  # Virtual Page Number
        self.content = content  # Simulating the page content
        self.access_bit = access_bit  # Indicate if the page is loaded in main memory

    def __str__(self):
        content_preview = self.content[:20] + \
            '...' if len(self.content) > 20 else self.content
        return (f"Page VPN: {self.vpn}, "
                f"Content: '{content_preview}' "
                f"Access Bit: {self.access_bit}")


class MainMemory:
    def __init__(self, frame_count=4):
        self.loaded_pages = {f'pfn_{i}': None for i in range(frame_count)}

    def remove_page_by_pfn(self, pfn):
        self.loaded_pages[pfn] = None

    def load_page(self, page: Page) -> str:
        for pfn, loaded_page in self.loaded_pages.items():
            if loaded_page is None:
                self.loaded_pages[pfn] = page
                return pfn
        return None


class PageMapTable:
    def __init__(self):
        self.page_map_table = {}

    def map(self, vpn, pfn):
        self.page_map_table[vpn] = pfn

    def translate(self, vpn) -> str:
        return self.page_map_table.get(vpn)

    def delete(self, vpn):
        return self.page_map_table.pop(vpn, None)

    def display_table(self):
        rows = [(vpn, pfn) for vpn, pfn in sorted(self.page_map_table.items())]
        formatter = TableFormatter(["VPN", "PFN"], rows)
        formatter.display_table()


class MemoryMapTable:
    def __init__(self, main_memory: MainMemory):
        self.memory_map_table = {
            pfn: {
                'vpn': page.vpn if page else None,
                'status': int(bool(page))}
            for pfn, page in main_memory.loaded_pages.items()
        }

    def update(self, pfn, vpn, status):
        self.memory_map_table[pfn] = {'vpn': vpn, 'status': status}

    def display_table(self):
        rows = [(pfn,
                 entry['vpn'] if entry['vpn'] is not None else 'None',
                 entry['status'] if entry['status'] is not None else 'None')
                for pfn, entry in self.memory_map_table.items()]
        formatter = TableFormatter(["PFN", "VPN", "Status"], rows)
        formatter.display_table()


class ReplacementAlgorithm(ABC):

    def __init__(self):
        self.vpn_registry = {}

    def find_replacement_vpn(self):
        return max(self.vpn_registry, key=self.vpn_registry.get, default=None)

    def update_reference(self, vpn: str):
        self.vpn_registry = {key: (0 if key == vpn else value + 1)
                             for key, value in self.vpn_registry.items()}

    def replace_vpn(self, old_vpn: str, new_vpn: str):
        self.vpn_registry.pop(old_vpn, None)
        self.vpn_registry[new_vpn] = 0

    @abstractmethod
    def update_load_reference(self, vpn: str):
        pass

    @abstractmethod
    def update_access_reference(self, vpn: str):
        pass

    def display_vpn_registry(self):
        TableFormatter(
            headers=["VPN", "Reference Count"],
            rows=list(self.vpn_registry.items())).display_table()


class LRU(ReplacementAlgorithm):
    def __init__(self):
        super().__init__()
        self.just_replaced = False

    def update_load_reference(self, vpn: str):
        super().update_reference(vpn)
        self.just_replaced = True

    def update_access_reference(self, vpn: str):
        if self.just_replaced:
            self.just_replaced = False
        else:
            super().update_reference(vpn)


class FIFO(ReplacementAlgorithm):
    def update_load_reference(self, vpn: str):
        super().update_reference(vpn)

    def update_access_reference(self, vpn: str):
        pass


class VirtualMemoryManager:
    def __init__(self, replacement_algorithm: ReplacementAlgorithm):
        self.mm = MainMemory()
        self.pmt = PageMapTable()
        self.mmt = MemoryMapTable(self.mm)
        self.ra = replacement_algorithm

    def load_page_to_main_memory(self, page):
        # Attempt to load the page, handle a page fault if necessary
        pfn = self.mm.load_page(page) or self._handle_page_fault(page)
        self.ra.vpn_registry[page.vpn] = 0
        self.ra.update_load_reference(page.vpn)

        # Update page access information
        self._update_page_access(page, pfn)

    def _handle_page_fault(self, page):
        replaced_vpn = self.ra.find_replacement_vpn()
        replaced_pfn = self.pmt.translate(replaced_vpn)

        self.mm.loaded_pages[replaced_pfn].access_bit = 0

        # Remove the page from Main Memory
        self.mm.remove_page_by_pfn(replaced_pfn)

        # Update Memory Map Table for the LRU page
        self.mmt.update(replaced_pfn, None, 0)
        self.pmt.delete(replaced_vpn)

        # Update Replacement Algorithm for vpn registry
        self.ra.replace_vpn(old_vpn=replaced_vpn, new_vpn=page.vpn)

        # Load the requested page into main memory
        return self.mm.load_page(page)

    def _update_page_access(self, page, pfn):
        # Update access bit for the page
        page.access_bit = 1

        self.pmt.map(page.vpn, pfn)

        # Update the Memory Map Table for the new page
        self.mmt.update(pfn, page.vpn, 1)

    def execute_demand_paging(self, required_vpn: list):
        page_faults = 0
        for vpn in required_vpn:
            if self.pmt.translate(vpn) is None:
                page_faults += 1
                page = Page(vpn=vpn, content=f"This is {vpn}", access_bit=1)
                self.load_page_to_main_memory(page)

            self.ra.update_access_reference(vpn)
            self.display_current_state()

        return page_faults

    def display_current_state(self):
        """Displays the current state of the page map table, memory map table, and loaded pages."""
        print("Page Map Table:")
        self.pmt.display_table()
        print("\nMemory Map Table:")
        self.mmt.display_table()

        print("\nVPN Registry:")
        self.ra.display_vpn_registry()
        print("\nLoaded Pages:")
        for pfn, page in self.mm.loaded_pages.items():
            if page is not None:
                print(f"PFN: {pfn}, Page: {page}")
            else:
                print(f"PFN: {pfn}, Page: None")

        print("\n" + "-"*40 + "\n")


def main():
    required_vpn = ['vpn2', 'vpn3', 'vpn7', 'vpn1', 'vpn2', 'vpn4', 'vpn5']
    vmm = VirtualMemoryManager(LRU())
    print(f'Total page faults: {vmm.execute_demand_paging(required_vpn)}')


if __name__ == '__main__':
    main()
