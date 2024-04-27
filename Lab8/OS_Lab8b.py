class MainMemory:
    def __init__(self, frame_count=4):
        self.loaded_pages = {f'pfn_{i}': None for i in range(frame_count)}

    def remove_page(self, vpn):
        for pfn, loaded_vpn in self.loaded_pages.items():
            if loaded_vpn == vpn:
                self.loaded_pages[pfn] = None
                break

    def load_page(self, vpn):
        for pfn, loaded_page in self.loaded_pages.items():
            if loaded_page is None:
                self.loaded_pages[pfn] = vpn
                return pfn
        return None

    def is_page_loaded(self, vpn):
        for loaded_vpn in self.loaded_pages.values():
            if loaded_vpn is not None and loaded_vpn == vpn:
                return True
        return False


class FIFO():
    def __init__(self):
        self.vpn_registry = {}

    def find_replacement_vpn(self):
        return max(self.vpn_registry, key=self.vpn_registry.get, default=None)

    def update_load_reference(self, vpn: str):
        self.vpn_registry = {key: (0 if key == vpn else value + 1)
                             for key, value in self.vpn_registry.items()}

    def replace_vpn(self, old_vpn: str, new_vpn: str):
        self.vpn_registry.pop(old_vpn, None)
        self.vpn_registry[new_vpn] = 0


class VirtualMemoryManager:
    def __init__(self):
        self.mm = MainMemory()
        self.fifo = FIFO()

    def load_page_to_main_memory(self, vpn):
        self.mm.load_page(vpn) or self._handle_page_fault(vpn)
        self.fifo.vpn_registry[vpn] = 0
        self.fifo.update_load_reference(vpn)

    def _handle_page_fault(self, vpn):
        replaced_vpn = self.fifo.find_replacement_vpn()
        self.mm.remove_page(replaced_vpn)
        self.fifo.replace_vpn(old_vpn=replaced_vpn, new_vpn=vpn)
        return self.mm.load_page(vpn)

    def execute_demand_paging(self, required_vpn: list):
        page_faults = 0
        for vpn in required_vpn:
            if not self.mm.is_page_loaded(vpn):
                page_faults += 1
                self.load_page_to_main_memory(vpn)

            self.display_current_state(vpn)

        return page_faults

    def display_current_state(self, current_vpn: str):
        print("-" * 35)
        print("current_vpn = " + current_vpn)
        print("-" * 35)
        print("VPN Registry:")
        for vpn, ref in self.fifo.vpn_registry.items():
            print(f"{vpn} -> {ref}")

        print("\nLoaded Pages:")
        for pfn, page in self.mm.loaded_pages.items():
            print(f"{pfn} -> {page or 'None'}")
        print()


def main():
    required_vpn = ['vpn2', 'vpn3', 'vpn7', 'vpn1', 'vpn2', 'vpn4', 'vpn5']
    vmm = VirtualMemoryManager()
    print(f'Total page faults: {vmm.execute_demand_paging(required_vpn)}')


if __name__ == '__main__':
    main()
