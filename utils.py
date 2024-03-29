import os
import time
import sys
import subprocess
import tensorflow as tf

def create_export_dir(export_dir, model_name):

    def create_dir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    _export_dir = os.path.join(export_dir, model_name)
    _path = ''

    for path in [export_dir, model_name]:
        _path = os.path.join(_path, path)
        create_dir(_path)
 
    return _export_dir

def concat_timestamp(export_dir):
    return os.path.join(export_dir, str(int(time.time())))


def tar(export_base_dir, export_dir, model_name):
    def get_timestamp(path):
        plist = path.split(os.sep)
        return plist[-1]
    if os.path.exists(export_dir):
        cwd = os.path.abspath(export_base_dir)
        timestamp = get_timestamp(export_dir)
        proc = subprocess.Popen(
            ['tar', 'cvfz', '{0}_{1}.tar.gz'.format(model_name, timestamp), './{0}'.format(timestamp)],
            cwd=cwd)
        out, err = proc.communicate()
        print(out)


PS_OPS = ['Variable', 'VariableV2', 'AutoReloadVariable']

def assign_to_device(device, ps_device='/cpu:0'):
    def _assign(op):
        node_def = op if instance(op, tf.NodeDef) else op.node_def
        if node_def.op in PS_OPS:
            return "/" + ps_device
        else:
            return device
    return _assign

