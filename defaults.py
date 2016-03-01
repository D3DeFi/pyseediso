class Defaults(object):
    """Default configuration for pyseediso."""

    def __init__(self):
        # Localization
        self.locale = 'en_US.UTF-8'                 # Locale
        self.language = 'en'                        # System language
        self.country = 'US'                         # Country
        self.keymap = 'us'                          # Keyboard mapping

        # Network
        self.hostname = 'debian-preseed'            # Hostname for installed system
        self.domain = 'local.domain'                # Domain for installed system
        self.default_interface = 'eth0'             # Select default network interface
        self.configure_networking = 'true'          # Do not skip network configuration
        self.disable_autoconfig = 'false'           # Use DHCP, if set to false, 
                                                    # following 3 directives will be ignored:
        self.network = '10.0.0.2/24'                # IP address + network prefix 
        self.gateway = '10.0.0.1'                   # Default gateway
        self.dns = '8.8.8.8 8.8.4.4'                # Nameservers to use

        # Firmware
        self.load_firmware = 'true'                 # Load non-free firmware if available

        # Mirrors
        self.network_mirror = 'true'                # Use network mirror
        self.mirror_local = 'httpredir.debian.org'  # Debian repo to use
        self.mirror_dir = '/debian/'                # Dir where to find repo
        self.mirror_suite = 'jessie'                # Which debian suite to use
        self.mirror_proxy = ''                      # If needed, specify proxy as follows:
                                                    # http://proxy:port/
        self.use_nonfree = 'false'                  # Install non-free software
        self.use_contrib = 'false'                  # Install contrib software

        # Accounts
        self.root_pass = 'changeme'                 # CHANGE immediately after install !!
        self.create_user = 'false'                  # Create less privileged user
        self.user_fullname = 'Debian user'          # Fullname for a new user
        self.user_name = 'debian'                   # Login name for a new user
        self.user_pass = 'changeme'                 # CHANGE immediately after install !!

        # Time
        self.use_utc = 'true'                       # UTC time
        self.use_ntp = 'true'                       # Sync time via ntp
        self.ntp_server = '0.debian.pool.ntp.org'   # NTP server to sync time to
        self.timezone = 'US/Eastern'                # Time zone

        # Disks
        self.disks = '/dev/sda'                     # Disks to use for install
        self.method = 'lvm'                         # Regular, lvm, raid
        self.vg_name = 'vg'                         # Name of volume group
        self.primary = '/boot 500M ext4'            # Primary partitions outside lvm
        self.lvm = '/ 2G ext4; /var 4G xfs'         # Logical volumes inside lvm
        self.remove_previous_lvm = 'true'           # If neccessary installer will remove
        self.remove_previous_md = 'true'            # any previous sw raids or lvms

        # Packages
        self.packages = [
            'openssh-server', 'build-essential', 'ssh', 'ca-certificates', 'curl',
            'vim', 'lvm2', 'bc', 'dnsutils', 'postfix', 'lsof', 'wget', 'mc', 'ntp',
            'screen', 'zip', 'unzip', 'wget'
        ]
        self.upgrade_mode = 'full-upgrade'          # Upgrade packages after debootstrap

        # Grub
        self.grub = '/dev/sda'                      # Where to install GRUB
        self.poweroff = 'false'                     # Poweroff system after install
