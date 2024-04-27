from table_formatter import TableFormatter


class Page:
    def __init__(self, vpn, ref=0):
        self.vpn = vpn  # Virtual Page Number
        self.ref = ref  # Tracks the last reference

    def __str__(self):
        return (f"Page ({self.vpn}, ref = {self.ref})")


class MainMemory:
    def __init__(self):
        self.frame_count = 4
        self.loaded_pages = {f'pfn_{i}': None for i in range(self.frame_count)}

    def remove_page(self, page: Page):
        for pfn, loaded_page in self.loaded_pages.items():
            if loaded_page == page:
                self.loaded_pages[pfn] = None
                break

    def load_page(self, page: Page) -> str:
        next_pfn = next(
            (pfn for pfn, page in self.loaded_pages.items() if page is None), None)
        if next_pfn is not None:
            self.loaded_pages[next_pfn] = page
            return next_pfn
        return None

    def is_page_loaded(self, vpn) -> bool:
        for loaded_page in self.loaded_pages.values():
            if loaded_page is not None and loaded_page.vpn == vpn:
                return True
        return False


class VirtualMemoryManager:
    def __init__(self):
        self.mm = MainMemory()

    def load_page_to_main_memory(self, page):
        self.mm.load_page(page) or self._handle_page_fault(page)
        page.ref = 0

    def _handle_page_fault(self, page):
        valid_pages = (p for p in self.mm.loaded_pages.values()
                       if p is not None)
        lru_page = max(valid_pages, key=lambda p: p.ref)
        self.mm.remove_page(lru_page)
        return self.mm.load_page(page)

    def execute_demand_paging(self, required_vpn: list):
        page_faults = 0
        for vpn in required_vpn:
            if not self.mm.is_page_loaded(vpn):
                page_faults += 1
                self.load_page_to_main_memory(
                    Page(vpn=vpn, ref=0))

            for page in self.mm.loaded_pages.values():
                if page is not None:
                    page.ref = 0 if page.vpn == vpn else page.ref + 1

            self.display_current_state(current_vpn=vpn)

        return page_faults

    def display_current_state(self, current_vpn):
        print("Loaded Pages: [current_vpn = " + current_vpn + "]")
        print("-" * 35)
        for pfn, page in self.mm.loaded_pages.items():
            print(f"{pfn} -> {page or 'None'}")
        print("-" * 35 + "\n")


def main():
    required_vpn = ['vpn2', 'vpn3', 'vpn7', 'vpn1', 'vpn2', 'vpn4', 'vpn5']
    vmm = VirtualMemoryManager()
    print(f'Total page faults: {vmm.execute_demand_paging(required_vpn)}')


if __name__ == '__main__':
    main()
