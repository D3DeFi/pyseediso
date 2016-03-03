#!/usr/bin/env python

import argparse
from defaults import Defaults
from jinja2 import Environment, PackageLoader
from netaddr import IPNetwork, AddrFormatError


class Config(Defaults):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.network = parse_network_string(self.network)

    def update(self, item, value):
        if hasattr(self, item):
            setattr(self, item, value)


def parse_network_string(netstr):
    try:
        ip = IPNetwork(netstr)
        return [ip.ip, ip.netmask]
    except AddrFormatError:
        return ['']*2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates Debian preseed configuration and attaches it to the specified ISO image.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('INPUT_ISO', metavar='<input_iso>', help='input ISO')
    parser.add_argument('-o', metavar='<output_iso>', default='pyseed.iso', dest='output', help='output ISO')
    parser.add_argument('--preseed', metavar='<file>', default='', help='complete preseed to attach to ISO')
    parser.add_argument('--gen-only', metavar='<file>', default='', help='only generate preseed file')
    netopt = parser.add_argument_group('network arguments')
    netopt.add_argument('--name', metavar='<hostname>', help='system hostname')
    netopt.add_argument('--domain', metavar='<domain>', help='system domain')
    netopt.add_argument('--net', metavar='<network>', help='IP/prefix (ex. --net 10.0.0.2/24)')
    netopt.add_argument('--gw', metavar='<gateway>', help='gateway IP')
    netopt.add_argument('--dns', metavar='<nameservers>', help="nameservers (ex. --dns '8.8.8.8 8.8.4.4')")
    diskopt = parser.add_argument_group('disk arguments')
    diskopt.add_argument('--disks', metavar='<disks>', help="install disks (ex. --disks '/dev/sda /dev/sdb')")
    diskopt.add_argument('--raid', metavar='<raid-type>', choices=[0, 1, 10], help='software raid (ex. --raid=1)')
    diskopt.add_argument('--primary', metavar='<part>', help="primary partitions (ex. --primary '/boot 500M ext4')")
    diskopt.add_argument('--lvm', metavar='<lvs>', help="logical volumes (ex. --lvm '/ 2G ext4; /var 3G xfs;')")
    diskopt.add_argument('--grub', metavar='<device>', help="GRUB destination (ex. --grub '/dev/sda /dev/sdb')")
    parser.add_argument('--poweroff', help='shutdown machine after install', action='store_true')
    args = parser.parse_args()

    def update_attr(obj, args):
        attributes = {
            'hostname': args.name,
            'domain': args.domain,
            'disks': args.disks,
            'grub': args.grub,
            'poweroff': args.poweroff
        }
        for key, value in attributes.iteritems():
            if value:
                obj.update(key, value) 

    if not args.preseed:
        env = Environment(loader=PackageLoader('pyseediso', 'templates'))
        template = env.get_template('preseed.j2')
        config = Config()

        update_attr(config, args)

        if bool(args.net) ^ bool(args.gw):
            parser.error('--net and --gw options must be used together')
        elif args.net and args.gw:
            config.update('configure_networking', 'true')
            config.update('disable_autoconfig', 'true')
            config.update('network', parse_network_string(args.net))
            config.update('gateway', args.gw)

        if args.dns:
            config.update('dns', args.dns)

        print template.render(config=config)
