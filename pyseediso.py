#!/usr/bin/env python

import sys
import time
import argparse
from defaults import Defaults
from jinja2 import Environment, PackageLoader
from pyseediso import helpers


class Config(Defaults):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.network = helpers.parse_network_string(self.network)

    def update(self, item, value):
        setattr(self, item, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates Debian preseed configuration and attaches it to the specified ISO image.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_iso', metavar='<input_iso>', help='input ISO')
    parser.add_argument('-o', metavar='<output>', dest='output', help='output ISO/file')
    parser.add_argument('--preseed', metavar='<file>', help='complete preseed to attach to ISO')
    parser.add_argument('--gen-only', help='only generate preseed file', action='store_true')
    parser.add_argument('--poweroff', help='shutdown machine after install', action='store_true')

    netopt = parser.add_argument_group('network arguments')
    netopt.add_argument('--name', metavar='<hostname>', help='system hostname')
    netopt.add_argument('--domain', metavar='<domain>', help='system domain')
    netopt.add_argument('--net', metavar='<network>', help='IP/prefix (ex. --net 10.0.0.2/24)')
    netopt.add_argument('--gw', metavar='<gateway>', help='gateway IP')
    netopt.add_argument('--dns', metavar='<nameservers>', help="nameservers (ex. --dns '8.8.8.8 8.8.4.4')")

    dskopt = parser.add_argument_group('disk arguments')
    dskopt.add_argument('--disks', metavar='<disks>', help="install disks (ex. --disks '/dev/sda /dev/sdb')")
    dskopt.add_argument('--raid', metavar='<raid-type>', choices=['0', '1', '10'], help='software raid (ex. --raid=1)')
    dskopt.add_argument('--primary', metavar='<part>', help="primary partitions (ex. --primary '/boot 500M ext4')")
    dskopt.add_argument('--lvm', metavar='<lvs>', help="logical volumes (ex. --lvm '/ 2G ext4; /var 3G xfs;')")
    dskopt.add_argument('--grub', metavar='<device>', help="GRUB destination (ex. --grub '/dev/sda /dev/sdb')")
    args = parser.parse_args()

    if bool(args.net) ^ bool(args.gw):
        parser.error('--net and --gw options must be used together')
        sys.exit(1)

    if args.raid:
        if not (args.primary or args.lvm):
            parser.error('either --primary, --lvm or both need to be used with --raid option')
            sys.exit(1)

    config = Config()
    attributes = {
        'hostname': args.name,
        'domain': args.domain,
        'dns': args.dns,
        'disks': args.disks,
        'grub': args.grub,
        'poweroff': args.poweroff
    }

    if args.net and args.gw:
        attributes.update({
            'configure_networking': 'true',
            'disable_autoconfig': 'true',
            'network': helpers.parse_network_string(args.net),
            'gateway': args.gw
        })

    for key, value in attributes.iteritems():
        if value:
            config.update(key, value)

    if args.raid or args.primary or args.lvm:
        if args.raid:
            config.update('method', 'raid')
            config.update('raid_type', args.raid)
        elif args.lvm:
            config.update('method', 'lvm')
        elif args.primary:
            config.update('method', 'regular')
        config.update('primary', args.primary)
        config.update('lvm', args.lvm)

    if not args.preseed:
        env = Environment(loader=PackageLoader('pyseediso', 'templates'))
        template = env.get_template('preseed.j2')

        if args.gen_only and not args.output:
            print template.render(config=config)
            sys.exit(0)
        elif args.gen_only and args.output:
            with open(args.output, 'w') as f:
                template.stream(config=config).dump(f)
            sys.exit(0)
        else:
            args.preseed = '/tmp/pyseed-preseed-cfg-{}'.format(time.time())
            with open(args.preseed, 'w') as f:
                template.stream(config=config).dump(f)
