Frog
===================
rain node api

Setup
------------

Install Deluged

    > apt-get install software-properties-common
    > add-apt-repository ppa:deluge-team/ppa
    > apt-get update
    > apt-get install deluged deluge-web

Change Deluged configure:

    http://${IP}:8112 default password `deluge`

Install openresty https://openresty.org/en/installation.html

    (for ubuntu without nginx) https://github.com/mengskysama/ops/tree/master/openresty)

Change configure:

    /src/config.py
    /config/frog.conf

Test and Reload OpenResty with config:

    > ln -s ${PATH_TO_REPO}/config/frog.conf ${PATH_TO_OPENRESTY}/nginx/conf/site-enabled/
    > nginx -t
    > nginx -s reload

Install python env:

    > apt-get install python-dev python-pip
    > pip install -r requirements.txt

Run api:

    > cd /src
    > python frog.py

Check backend api:

    > curl "http://127.0.0.1:9019/api/node/tasks?token=${API_TOKEN}"

Check OpenResty configure:

    > curl "${YOUR_NODE_DOMAIN}/api/node/tasks?token=${API_TOKEN}"

Contributing
------------

Contributions, complaints, criticisms, and whatever else are welcome. The source
code and issue tracker can be found on GitHub.

License
-------

Deluge: https://github.com/deluge-torrent/deluge
Flask: https://github.com/pallets/flask
