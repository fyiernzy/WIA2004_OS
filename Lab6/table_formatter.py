class TableFormatter:
    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows
        self.column_widths = self._calculate_column_widths()

    def _calculate_column_widths(self):
        """Calculate the maximum width for each column based on headers and row content."""
        widths = [
            len(header) + 4 for header in self.headers]  # Start with header widths
        for row in self.rows:
            for i, item in enumerate(row):
                widths[i] = max(widths[i], len(str(item)) + 4)
        return widths

    def display_table(self):
        if not self.rows:
            print("Table is empty.")
            return

        # Adjust the format string to include padding for aesthetics
        header_format = "|".join(f"{{:^{w + 2}}}" for w in self.column_widths)
        row_format = "|".join(f"{{:^{w + 2}}}" for w in self.column_widths)

        # Print the table header
        print(header_format.format(*self.headers))
        print('-' * sum(self.column_widths + [3 * (len(self.headers) - 1)]))

        # Print each row
        for row in self.rows:
            print(row_format.format(*[str(item) for item in row]))
        print()
