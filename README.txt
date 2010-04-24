OpenOpenGraph
=============

This is an open source implementation of Facebook's Open Graph protocol.

Example
-------

$ curl -F 'username=ericflo' http://127.0.0.1:8000/
{
    "id": 1,
    "username": "ericflo"
}

$ curl http://127.0.0.1:8000/1
{
    "id": 1,
    "username": "ericflo"
}

$ curl http://127.0.0.1:8000/1/feed
{
    "data": []
}

$ curl -F 'link=http://github.com/ericflo/openopengraph' -F 'message=Cool Project!' http://127.0.0.1:8000/1/feed
{
    "id": 2,
    "link": "http://github.com/ericflo/openopengraph",
    "message": "Cool Project!"
}

$ curl http://127.0.0.1:8000/1/feed
{
    "data": [
        {
            "id": 2,
            "link": "http://github.com/ericflo/openopengraph",
            "message": "Cool Project!"
        }
    ]
}

$ curl http://127.0.0.1:8000/2
{
    "id": 2,
    "link": "http://github.com/ericflo/openopengraph",
    "message": "Cool Project!"
}

Installation
------------

First check out the source:

    git clone git://github.com/ericflo/openopengraph.git

Then make sure you have werkzeug, simplejson, and redis-py installed. If 
you're a pip user, you can just do:

    pip install -U -r requirements.txt

Make sure you have Redis installed, and running.

    curl -O http://redis.googlecode.com/files/redis-1.2.6.tar.gz
    tar xvfz redis-1.2.6.tar.gz
    cd redis-1.2.6
    make
    ./redis-server

Running
-------

Just invoke api.py:

    python openopengraph/api.py