import os
import shutil
import subprocess

BASEDIR = './tmp-pyseediso/'
LOOPDIR = 'loopdir'
INITDIR = 'initrd'
MOUNTDIR = 'cd'
TITLESCRCFG = MOUNTDIR + '/isolinux/txt.cfg'

testiso = 'test.iso'
testpreseed = 'test.cfg'


class GeneratorException(Exception):
    """Common exception for ISO generator."""
    pass


def is_executable(cmd):
    """Tests if file is executable."""
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def get_iso_label(iso):
    """Uses system's blkid command to get UUID label of specific iso."""
    if is_executable('blkid'):
        try:
            p1 = subprocess.Popen(['blkid', '-o', 'value', iso], stdout=subprocess.PIPE)
            label = p1.communicate()[0].split('\n')[0]
        except OSError as e:
            raise GeneratorException(e.message)
        return label
    else:
        raise GeneratorException('Executable blkid not found.')

ISOLABEL = get_iso_label(testiso)


def mount(src, dst, options):
    """Wrapper for Unix's mount command."""
    rc = subprocess.call(['/bin/mount', '-o', options, src, dst], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if rc != 0:
        raise GeneratorException('Unable to mount {} to {} with options: {}'.format(src, dst, options))


def umount(dst):
    """Wrapper for Unix's umount command."""
    rc = subprocess.call(['/bin/umount', dst])
    if rc != 0:
        raise GeneratorException('Unable to umount {}'.format(dst))


# Create temporary directories for ISO extraction and rebuild
if not os.path.exists(BASEDIR):
    os.mkdir(BASEDIR)
    for directory in [LOOPDIR, INITDIR, MOUNTDIR]:
        os.mkdir(BASEDIR + directory)
else:
    raise GeneratorException('Directory {} exists.'.format(BASEDIR))


print ISOLABEL
mount(testiso, BASEDIR + MOUNTDIR, 'loop')

umount(BASEDIR + MOUNTDIR)

# Cleanup
if os.path.exists(BASEDIR):
    shutil.rmtree(BASEDIR)
