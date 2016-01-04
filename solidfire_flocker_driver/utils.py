import os.path
import shlex
import subprocess
import time


def path_exists(path, counter=1):
    for i in xrange(counter):
        if os.path.exists(path):
            return True
        time.sleep(1)
    return False


def find_device_file(path):
    device = None
    if os.path.exists(path):
        device = os.readlink(path)
    return device


def iscsi_logout(tgt_ip, tgt_iqn):
    cmd = 'iscsiadm -m node -p %s -T %s -u' % (tgt_ip, tgt_iqn)
    subprocess.check_output(shlex.split(cmd))

    cmd = 'iscsiadm -m node -o delete -T %s' % (tgt_iqn)
    subprocess.check_output(shlex.split(cmd))


def iscsi_login(tgt_ip, tgt_iqn):
    attached_at = None
    path = '/dev/disk/by-path/ip-%s-iscsi-%s-lun-0' % (tgt_ip,
                                                       tgt_iqn),
    cmd = 'iscsiadm -m node -p %s -T %s --login' % (tgt_ip, tgt_iqn)
    subprocess.check_output(shlex.split(cmd))
    if path_exists(path, 5):
        attached_at = path
    return attached_at


def iscsi_discovery(portal):
    cmd = 'iscsiadm -m discovery -t sendtargets -p %s' % portal
    output = subprocess.check_output(shlex.split(cmd))
    return output.split('\n')
