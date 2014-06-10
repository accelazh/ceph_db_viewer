import pprint
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from ceph_db_viewer import util
from ceph_db_viewer.hex_bytes import HexBytes

import leveldb

TMP_DB_LOCATION_FILE = '/tmp/ceph_db_viewer.data'

def index(request):
    return HttpResponse("You're at the mon_db index.")

def overview(request):
    OVERVIEW_LENGTH = 64
    
    response = []
    base_tmpl = loader.get_template('mon_db/base.html')
    response.append(base_tmpl.render(RequestContext(request)))

    mon_name_tmpl = loader.get_template('mon_db/mon.html')
    object_overview_tmpl = loader.get_template('mon_db/object.html')

    dbs = util.snapshot_mon_db() # leveldb cannot be read while ceph is using, so we have to snapshot it

    # TODO bad way to share data
    with open(TMP_DB_LOCATION_FILE, 'w') as db_loc_file:
        db_loc_file.write(json.dumps(dbs))

    for mon_name, db_path in dbs.iteritems():
        context = RequestContext(request, {
                'mon_name': mon_name
            })
        response.append(mon_name_tmpl.render(context))
        db = leveldb.LevelDB(db_path)
        for o in db.RangeIter():
            obj = util.KVObject(o[0], o[1], 128)
            context = RequestContext(request, {
                    'mon_name_hex': mon_name.encode("hex"),
                    'object': obj
                })
            response.append(object_overview_tmpl.render(context))

    return HttpResponse(''.join(response))

def detail(request):
    object_key = request.GET.get('object_key_hex', '').decode("hex")
    mon_name = request.GET.get('mon_name_hex', '').decode("hex")

    # where is db snapshorts
    dbs = None
    with open(TMP_DB_LOCATION_FILE) as db_loc_file:
        dbs = json.loads(db_loc_file.read())
        # what if file doesn't exists?

    db = leveldb.LevelDB(dbs[mon_name])
    value = db.Get(object_key)
    obj = util.KVObject(object_key, value)

    response = []
    base_tmpl = loader.get_template('mon_db/base.html')
    response.append(base_tmpl.render(RequestContext(request)))

    mon_name_tmpl = loader.get_template('mon_db/mon.html')
    object_overview_tmpl = loader.get_template('mon_db/object.html')    
    response.append(mon_name_tmpl.render(RequestContext(request, {
                'mon_name': mon_name
            })))
    response.append(object_overview_tmpl.render(RequestContext(request, {
                'mon_name_hex': mon_name.encode("hex"),
                'object': obj
            })))

    return HttpResponse(''.join(response))

