from netaddr import IPNetwork, AddrFormatError


def parse_network_string(netstr):
    try:
        ip = IPNetwork(netstr)
        return [ip.ip, ip.netmask]
    except AddrFormatError:
        return ['']*2


def parse_disksize_string(diskstr):
    if diskstr.endswith('T'):
        return int(diskstr.strip('T')) * 1024 * 1024
    elif diskstr.endswith('G'):
        return int(diskstr.strip('G')) * 1024
    elif diskstr.endswith('M'):
        return int(diskstr.strip('M'))
