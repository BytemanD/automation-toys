import prettytable
from easy2use.common import table

try:
    from rich import table as rich_table
except ImportError:
    rich_table = None


# TODO: Move this code ot easy2use
class RichTable(object):

    def __init__(self, headers, title=None, col_style=None):
        self.headers = headers
        self.table = rich_table.Table(title=title)
        self.col_style = col_style

        for header in self.headers:
            self.table.add_column(header, style=col_style, no_wrap=True)

    def add_row(self, cols):
        self.table.add_row(*cols)

    def dumps(self):
        from rich import console              # noqa

        console.Console().print(self.table)


def get_table(headers, csv=False):
    if not csv and rich_table:
        return RichTable(headers)
    return csv and table.CSVTable(headers) or prettytable.PrettyTable(headers)
