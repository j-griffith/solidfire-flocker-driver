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


def get_expected_disk_path(ip, iqn):
    return '/dev/disk/by-path/ip-%s-iscsi-%s-lun-0' % (ip,
                                                       iqn)


def get_device_file_from_path(disk_by_path):
    device = None
    if os.path.exists(disk_by_path):
        device = os.readlink(disk_by_path)
    return device.replace('../../', '/dev/')


def iscsi_logout(tgt_ip, tgt_iqn):
    cmd = 'iscsiadm -m node -p %s -T %s -u' % (tgt_ip, tgt_iqn)
    subprocess.check_output(shlex.split(cmd))

    cmd = 'iscsiadm -m node -o delete -T %s' % (tgt_iqn)
    subprocess.check_output(shlex.split(cmd))


def iscsi_login(tgt_ip, tgt_iqn):
    attached_at = None
    path = get_expected_disk_path(tgt_ip, tgt_iqn)
    cmd = 'iscsiadm -m node -p %s -T %s --login' % (tgt_ip, tgt_iqn)
    subprocess.check_output(shlex.split(cmd))
    if path_exists(path, 5):
        attached_at = path
    return attached_at


def iscsi_discovery(portal):
    cmd = 'iscsiadm -m discovery -t sendtargets -p %s' % portal
    output = subprocess.check_output(shlex.split(cmd))
    return output.split('\n')
