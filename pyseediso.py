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
    arg_parser = argparse.ArgumentParser(
        description='Generates Debian preseed configuration and attaches it to the specified ISO image.',
        formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('INPUT_ISO', help='specify which ISO to preseed')
    arg_parser.add_argument('-o', help='name of a newly preseeded ISO', metavar='OUTPUT_ISO')
    arg_parser.add_argument('--hostname', help='hostname for installed system')
    arg_parser.add_argument('--domain', help='domain for installed system')
    arg_parser.add_argument(
        '--net', help='IP and prefix to be used during system install eg --network 10.0.0.2/24')
    arg_parser.add_argument('--gw', help='gateway IP to be used during system install')
    arg_parser.add_argument(
        '--dns', help="nameservers for installed system eg --dns '8.8.8.8 8.8.4.4'")
    arg_parser.add_argument(
        '--disks', help="disks, which should be used for install eg --disks '/dev/sda /dev/sdb'")
    arg_parser.add_argument('--raid', help='if software raid should be used and what type', choices=[0, 1, 10])
    arg_parser.add_argument(
        '--primary', 
        help="list of primary partitions to create eg --primary '/boot 500M ext4; \
/data 5G xfs'\ndo not specify LVM as primary partition, use --lvm option instead")
    arg_parser.add_argument(
        '--lvm', 
        help="list of LVs to create eg --lvm '/ 2G ext4; /var 3G xfs; /home 1G xfs'")
    arg_parser.add_argument('--grub', help="where to install GRUB eg --grub '/dev/sda'")
    arg_parser.add_argument(
        '--poweroff', help='shutdown system after installation instead of restarting it', action='store_true')
    args = arg_parser.parse_args()

    env = Environment(loader=PackageLoader('pyseediso', 'templates'))
    template = env.get_template('preseed.j2')
    config = Config()

    def update_attr(obj, args):
        attributes = {
            'hostname': args.hostname,
            'domain': args.domain,
            'disks': args.disks,
            'grub': args.grub,
            'poweroff': args.poweroff}

        for key, value in attributes.iteritems():
            if value:
                obj.update(key, value) 

    update_attr(config, args)

    if bool(args.net) ^ bool(args.gw):
        arg_parser.error('--net and --gw options must be used together')
    elif args.net and args.gw:
        config.update('configure_networking', 'true')
        config.update('disable_autoconfig', 'true')
        config.update('network', parse_network_string(args.net))
        config.update('gateway', args.gw)

    if args.dns:
        config.update('dns', args.dns)

    print template.render(config=config)
