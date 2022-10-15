# -*- coding: utf-8 -*-
import glob
import getpass
import logging
import os

from easy2use.globals import cli
from easy2use.globals import log
from easy2use.globals import i18n

from autotoys.common import utils
from autotoys.common.tickets import traffic

LOG = logging.getLogger(__name__)

_ = i18n._

DEFAULT_RENAME = '{{code}}+{{number}}+{}'.format(getpass.getuser())


class ParseTrafficTickets(cli.SubCli):
    NAME = 'parse-traffic-tickets'
    HELP = _('parse PDF tracffic tickets')
    ARGUMENTS = log.get_args() + [
        cli.Arg('pdf', nargs='+', help='PDF路径, 目录或者文件'),
        cli.Arg('-c', '--csv', action='store_true', help='输出csv格式'),
        cli.Arg('-r', '--rename', help=f'重命名格式, 例如：{DEFAULT_RENAME}'),
        cli.Arg('-n', '--check-code-num', default=6, type=int,
                help='校验码后n位数量, 默认值: 6'),
        cli.Arg('-N', '--no-footer', action='store_true', help='不显示合计行'),
        cli.Arg('-m', '--merge', action='store_true',
                help='merger tickets to pdf'),
    ]

    def __call__(self, args):
        pdf_list = []
        for pdf_path in args.pdf:
            LOG.debug('check path %s', pdf_path)
            if os.path.isdir(pdf_path):
                pdf_list.extend(glob.glob(os.path.join(pdf_path, '*.pdf')))
            elif os.path.isfile(pdf_path):
                pdf_list.append(pdf_path)
            else:
                LOG.warning('pdf not exists %s', pdf_path)

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
            number = ticket.number
            code = ticket.code
            date = ticket.date
            check_code = ticket.check_code
            check_code = check_code[
                (len(check_code) - args.check_code_num-1):-1]
            if args.rename:
                new_name = args.rename.format(code=code, number=number,
                                              date=date, check_code=check_code)
                ticket.rename(new_name)
            table.add_row([ticket.name, ticket.code, ticket.number,
                           ticket.date, check_code, money])
            total_money += float(ticket.money)

        if not args.no_footer:
            table.add_row([_('Total')] + ['-'] * 4 +
                          ['{:.2f}'.format(total_money)])
        print(table)
        if args.merge:
            traffic.screenshot_and_merge(pdf_list)


def main():
    cli_parser = cli.SubCliParser('Python Automation Utils',
                                  title='Subcommands')
    cli_parser.register_clis(ParseTrafficTickets)
    cli_parser.call()


if __name__ == '__main__':
    main()
