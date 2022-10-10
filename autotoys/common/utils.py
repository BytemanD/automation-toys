import prettytable
from easy2use.common import table


def get_table(headers, csv=False):
    return csv and table.CSVTable(headers) or prettytable.PrettyTable(headers)
