# -*- coding: utf-8 -*-
import glob
import getpass
import logging
import os

try:
    from rich import traceback
    traceback.install()
except ImportError:
    pass

from easy2use.globals import cli
from easy2use.globals import log

from autotoys.common import i18n
from autotoys.common import utils
from autotoys.common.tickets import traffic


LOG = logging.getLogger(__name__)

_ = i18n._

DEFAULT_RENAME = '{{code}}+{{number}}+{}'.format(getpass.getuser())

parser = cli.SubCliParser('Python Automation Utils', title='Subcommands')


@parser.add_command(
    *log.get_args(),
    cli.Arg('pdf', nargs='+', help='PDF路径, 目录或者文件'),
    cli.Arg('-c', '--csv', action='store_true', help='输出csv格式'),
    cli.Arg('-r', '--rename', action='store_true', help='重命名格式'),
    cli.Arg('-f', '--rename-format', default=DEFAULT_RENAME,
            help=f'重命名格式, 默认：{DEFAULT_RENAME}'),
    cli.Arg('-n', '--check-code-num', default=6, type=int,
            help='校验码后n位数量, 默认值: 6'),
    cli.Arg('-N', '--no-footer', action='store_true', help='不显示合计行'),
    cli.Arg('-m', '--merge', action='store_true',
            help='PDF转为图片并且合并'),
    cli.Arg('--img-width', type=int, default=90,
            help='图片宽度, 如果合并得图片被覆盖，可适当减小改选项'),
)
def parse_traffic_tickets(args):  # sourcery skip: raise-specific-error
    """Parse PDF Tracffic Tickets
    """
    pdfminer_log = logging.getLogger('pdfminer')
    pdfminer_log.setLevel(logging.INFO)

    pdf_list = []
    for pdf_path in args.pdf:
        LOG.debug('check path %s', pdf_path)
        if os.path.isfile(pdf_path):
            pdf_list.append(pdf_path)
        elif os.path.isdir(pdf_path):
            pdf_list.extend(glob.glob(pdf_path))
        else:
            pdf_list.extend(glob.glob(pdf_path))

    LOG.debug('pdf files: %s', pdf_list)
    headers = [_('File'), _('Ticket Code'), _('Ticket Number'),
               _('Invoicing Date'),
               _('Check Code(last {})').format(args.check_code_num),
               _('Money')]

    table = utils.get_table(headers, csv=args.csv)

    total_money = 0
    for path in pdf_list:
        ticket = traffic.TrafficTicket(path)
        ticket.parse()
        money = ticket.money
        if not money:
            raise RuntimeError(f'解析失败： {ticket.name}')
        number = ticket.number
        code = ticket.code
        date = ticket.date
        check_code = ticket.check_code
        check_code = check_code[(len(check_code) - args.check_code_num):]
        if args.rename:
            new_name = args.rename_format.format(
                code=code, number=number, date=date, check_code=check_code)
            ticket.rename(new_name)
        table.add_row([ticket.name, ticket.code, ticket.number,
                       ticket.date, check_code, money])
        total_money += float(money)

    if not args.no_footer:
        table.add_row([_('Total')] + ['-'] * 4 +
                      ['{:.2f}'.format(total_money)])
    if isinstance(table, utils.RichTable):
        table.dumps()
    else:
        print(table)

    if args.merge:
        traffic.screenshot_and_merge(pdf_list, img_width=args.img_width,
                                     file_name='merged.pdf')
        print('合并成功，文件路径: merged.pdf')


def main():
    parser.call()


if __name__ == '__main__':
    main()
