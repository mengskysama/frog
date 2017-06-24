#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author mengskysama

from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask import Flask
import statvfs
import os
import ulits
from flask import Blueprint, jsonify, request, abort
from deluge_client import DelugeRPCClient
monkey.patch_all()

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Blueprint('api', __name__)
u, p = ulits.get_deluge_local_auth()


@app.before_request
def before_req():
    if app.config.get('API_TOKEN') != request.args.get('token', ''):
        abort(403)


@api.route('/ping', methods=['GET', 'POST'])
def ping():
    rx, tx = ulits.InterfaceHelper('eth0').get_transfer()
    vfs = os.statvfs(app.config.get('TASK_DOWNLOAD_PATH'))
    dir(statvfs)
    available = vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]
    return jsonify({'data': {'RX': rx, 'TX': tx, 'available': available}, 'errCode': 0})


@api.route('/node/space/available', methods=['GET'])
def get_space():
    vfs = os.statvfs(app.config.get('TASK_DOWNLOAD_PATH'))
    dir(statvfs)
    available = vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]
    return jsonify({'data': {'available': available}, 'errCode': 0})


@api.route('/node/tasks', methods=['GET'])
def node_tasks():
    client = DelugeRPCClient('127.0.0.1', 58846, u, p)

    def get_task_list():
        if client.connected is False:
            client.connect()
        return client.call('core.get_torrents_status',
                           {},
                           [u'queue', u'name', u'total_size', u'state', u'progress', u'num_seeds', u'total_seeds',
                            u'num_peers', u'total_peers', u'download_payload_rate', u'upload_payload_rate', u'eta',
                            u'ratio', u'distributed_copies', u'is_auto_managed', u'time_added', u'tracker_host',
                            u'save_path', u'total_done', u'total_uploaded', u'max_download_speed', u'max_upload_speed',
                            u'seeds_peers_ratio'])

    return jsonify({'data': get_task_list(), 'errCode': 0})


@api.route('/node/task/create', methods=['POST'])
def node_task_create():

    torrent_data = request.form.get('torrent_data')
    info_hash = request.form.get('info_hash')

    client = DelugeRPCClient('127.0.0.1', 58846, u, p)
    def add_task():
        if client.connected is False:
            client.connect()
        download_location = app.config.get('TASK_DOWNLOAD_PATH') + '/' + info_hash
        try:
            os.makedirs(download_location)
        except:
            pass
        options = {'download_location': download_location}
        return client.call('core.add_torrent_file', '', torrent_data, options)
    # if torrent already in return null!
    return jsonify({'data': add_task(), 'errCode': 0})


@api.route('/node/task/delete/<string:infohash>', methods=['DELETE'])
def node_task_del(infohash):
    client = DelugeRPCClient('127.0.0.1', 58846, u, p)
    if client.connected is False:
        client.connect()
    ret = client.call('core.get_torrents_status', {'id': [infohash]}, [u'name'])
    if len(ret[infohash]) == 0:
        # clean cache
        try:
            download_location = app.config.get('TASK_DOWNLOAD_PATH') + '/' + infohash
            os.removedirs(download_location)
        except:
            pass
        res = True
    else:
        res = client.call('core.remove_torrent', infohash, True)

    return jsonify({'data': res, 'errCode': 0})


if __name__ == "__main__":
    app.register_blueprint(api, url_prefix='/api')
    WSGIServer(('127.0.0.1', 9019), app).serve_forever()
