ceph_db_viewer
==============

Scratchy django app to view ceph monitor's leveldb data.

How to Use
---

Download repo and set up django web server.

```
git clone https://github.com/accelazh/ceph_db_viewer.git
cd ceph_de_viewer
./manage.py runserver 0.0.0.0:8081

```

Access `mon_db/overview` to see all key-value objects in leveldb of ceph monitors.
```
http://<host>:8081`/mon_db/overview
```

Click any key name of an object, will show detail page. For example
```
http://<host>:8081/mon_db/detail?object_key_hex=617574680031&mon_name_hex=636c7573746572412d6d6f6e2e32
```

The <host> should have ceph monitor running.

Notes
---

Currently all key-value pairs are loaded to web page at once. On overview page, value is truncated by still too many.

Leveldb cannot be read while ceph is using it. So I copy ceph monitor's leveldb to /tmp and read it, every time. This is crappy.

