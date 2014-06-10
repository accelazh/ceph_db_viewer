import os
import sys
import leveldb
import tempfile
import errno
import shutil
from hex_bytes import HexBytes

MON_DATA_PATH = '/var/lib/ceph/mon'
MON_DB_NAME = 'store.db'

def ls_mon_db():
    # {mon_name => db_path, ...}
    out = {}
    for mon_name in os.listdir(MON_DATA_PATH):
        out[mon_name] = os.path.join(MON_DATA_PATH, mon_name, MON_DB_NAME)
    return out

def snapshot_mon_db():
    # {mon_name => snapshot_db_path, ...}
    out = {}
    dir = tempfile.mkdtemp()
    for name, db_path in ls_mon_db().iteritems():
        mon_dir = os.path.join(dir, name)
        try:
            os.makedirs(mon_dir)
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(mon_dir):
                pass
            else:
                raise
        try:
            shutil.copytree(db_path, os.path.join(mon_dir, MON_DB_NAME))
        except OSError as ex:
            if ex.errno == errno.ENOTDIR:
                shutil.copy(db_path, mon_dir)
            else:
                raise
        out[name] = os.path.join(mon_dir, MON_DB_NAME)
    return out

class KVObject(object):

    def __init__(self, key='', value='', limit=-1):
        self.key = HexBytes(key, limit)
        self.value = HexBytes(value, limit)

        self.key_hex = self.key.hex()
        self.key_txt = self.key.txt()
        self.val_txt = self.value.txt(True)
        self.val_hex = self.value.hex(space=True)
        self.val_uint32 = self.value.uint32()
        self.val_uint64 = self.value.uint64()


        



