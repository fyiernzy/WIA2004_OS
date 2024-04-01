from table_formatter import TableFormatter


class Page:
    def __init__(self, vpn, content, access_bit=0, ref=0):
        self.vpn = vpn  # Virtual Page Number
        self.content = content  # Simulating the page content
        self.ref = ref  # Tracks the last reference
        self.access_bit = access_bit  # Indicate if the page is loaded in main memory

    def __str__(self):
        return (f"Page VPN: {self.vpn}, "
                # Show first 20 chars of content for brevity
                f"Content: '{self.content[:20]}' "
                f"(Ref: {self.ref}, Access Bit: {self.access_bit})")


class MainMemory:
    def __init__(self):
        self.frame_count = 4
        self.loaded_pages = {f'pfn_{i}': None for i in range(self.frame_count)}

    def remove_page_by_pfn(self, pfn):
        self.loaded_pages[pfn] = None

    def load_page(self, page: Page) -> str:
        next_pfn = next(
            (pfn for pfn, page in self.loaded_pages.items() if page is None), None)
        if next_pfn is not None:
            self.loaded_pages[next_pfn] = page
            return next_pfn
        return None


class PageMapTable:
    def __init__(self):
        self.page_map_table = {}

    def map(self, vpn, pfn):
        if vpn not in self.page_map_table:
            self.page_map_table[vpn] = pfn

    def translate(self, vpn) -> str:
        return self.page_map_table.get(vpn, None)

    def delete(self, vpn):
        return self.page_map_table.pop(vpn)

    def display_table(self):
        rows = [(vpn, pfn) for vpn, pfn in sorted(self.page_map_table.items())]
        formatter = TableFormatter(["VPN", "PFN"], rows)
        formatter.display_table()


class MemoryMapTable:
    def __init__(self, mm: MainMemory):
        self.memory_map_table = {
            pfn: {
                'vpn': None if page is None else page.vpn,
                'status': 0 if page is None else 1}
            for pfn, page in mm.loaded_pages.items()
        }

    def update(self, pfn, vpn, status):
        self.memory_map_table[pfn] = {'vpn': vpn, 'status': status}

    def display_table(self):
        rows = [(pfn, entry['vpn'] if entry['vpn'] is not None else 'None',
                 entry['status'] if entry['status'] is not None else 'None')
                for pfn, entry in self.memory_map_table.items()]
        formatter = TableFormatter(["PFN", "VPN", "Status"], rows)
        formatter.display_table()


class VirtualMemoryManager:
    def __init__(self):
        self.mm = MainMemory()
        self.pmt = PageMapTable()
        self.mmt = MemoryMapTable(self.mm)

    def load_page_to_main_memory(self, page):
        # Attempt to load the page, handle a page fault if necessary
        pfn = self.mm.load_page(page) or self._handle_page_fault(page)

        # Update page access information
        self._update_page_access(page, pfn)

    def _handle_page_fault(self, page):
        # Filter out None values from loaded pages
        valid_pages = (p for p in self.mm.loaded_pages.values()
                       if p is not None)

        # Find Least Recently Used (LRU) page based on ref attribute
        lru_page = max(valid_pages, key=lambda p: p.ref)
        lru_page.access_bit = 0
        lru_pfn = self.pmt.translate(lru_page.vpn)

        # Remove the LRU page
        self.mm.remove_page_by_pfn(lru_pfn)

        # Update Memory Map Table for the LRU page
        self.mmt.update(lru_pfn, None, 0)
        self.pmt.delete(lru_page.vpn)

        # Load the requested page into main memory
        return self.mm.load_page(page)

    def _update_page_access(self, page, pfn):
        # Update reference and access bit for the page
        page.ref = 0
        page.access_bit = 1

        self.pmt.map(page.vpn, pfn)

        # Update the Memory Map Table for the new page
        self.mmt.update(pfn, page.vpn, 1)

    def execute_demand_paging(self, required_vpn: list):
        page_faults = 0
        for vpn in required_vpn:
            if self.pmt.translate(vpn) is None:
                page_faults += 1
                self.load_page_to_main_memory(
                    Page(vpn=vpn, content=f"This is {vpn}", access_bit=1, ref=0))

            for pfn, page in self.mm.loaded_pages.items():
                if page is not None:
                    page.ref = 0 if page.vpn == vpn else page.ref + 1

            self.display_current_state()

        return page_faults

    def display_current_state(self):
        """Displays the current state of the page map table, memory map table, and loaded pages."""
        print("Page Map Table:")
        self.pmt.display_table()
        print("\nMemory Map Table:")
        self.mmt.display_table()
        print("\nLoaded Pages:")
        for pfn, page in self.mm.loaded_pages.items():
            if page is not None:
                print(f"PFN: {pfn}, Page: {page}")
            else:
                print(f"PFN: {pfn}, Page: None")
        print("\n" + "-"*40 + "\n")


def main():
    required_vpn = ['vpn2', 'vpn3', 'vpn7', 'vpn1', 'vpn2', 'vpn4', 'vpn5']
    vmm = VirtualMemoryManager()
    print(f'Total page faults: {vmm.execute_demand_paging(required_vpn)}')


if __name__ == '__main__':
    main()
