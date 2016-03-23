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
        label = subprocess.check_output('blkid -o value {} | head -1'.format(iso))
        return label
    else:
        raise GeneratorException('Executable blkid not found.')

ISOLABEL = get_iso_label(testiso)

# Create temporary directories for ISO extraction and rebuild
if not os.path.exists(BASEDIR):
    os.mkdir(BASEDIR)
    for directory in [LOOPDIR, INITDIR, MOUNTDIR]:
        os.mkdir(BASEDIR + directory)
else:
    raise GeneratorException('Directory {} exists.'.format(BASEDIR))



# Cleanup
if os.path.exists(BASEDIR):
    shutil.rmtree(BASEDIR)
