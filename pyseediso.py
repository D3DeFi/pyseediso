#!/usr/bin/python

import argparse


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Generates Debian preseed configuration and attaches it to the specified ISO image.',
        formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('INPUT_ISO', help='specify which ISO to preseed')
    arg_parser.add_argument('-o', help='name of a newly preseeded ISO', metavar='OUTPUT_ISO')
    arg_parser.add_argument('--hostname', help='hostname for installed system')
    arg_parser.add_argument('--domain', help='domain for installed system')
    arg_parser.add_argument(
        '--network', help="IP and prefix to be used during system install\ne.g. --network='10.0.0.2/24'")
    arg_parser.add_argument('--gateway', help='gateway IP to be used during system install')
    arg_parser.add_argument(
        '--dns', help="nameservers for installed system\ne.g. --dns='8.8.8.8 8.8.4.4'")
    arg_parser.add_argument(
        '--raid', help="disks, which should be used for software raid\ne.g. --raid='/dev/sda /dev/sdb'",
        metavar='RAID_DISKS')
    arg_parser.add_argument('--raid-type', help='software raid type to be used', choices=[0, 1, 10])
    arg_parser.add_argument(
        '--primary', 
        help="list of primary partitions to create during system install. Do not specify LVM as primary partition, \
use --lvm option instead\ne.g. --primary='/boot 500M ext4; /data 5G xfs'")
    arg_parser.add_argument(
        '--lvm', 
        help="list of LVs to create during system install\ne.g. --lvm='/ 2G ext4; /var 3G xfs; /home 1G xfs'")
    arg_parser.add_argument('--grub', help="where to install GRUB during system install\ne.g. --grub='/dev/sda'")
    arg_parser.add_argument(
        '--poweroff', help='shutdown system after installation instead of restarting it', action='store_true')
    args = arg_parser.parse_args()
    print dir(args)
    print args.raid, args.poweroff
    print args.INPUT_ISO

