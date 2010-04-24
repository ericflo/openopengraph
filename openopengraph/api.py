import simplejson

from werkzeug import Request, Response, run_simple
from werkzeug.exceptions import NotFound

from database import DB # FIXME: Use absolute import

db = DB()

def _pretty_dump(data):
    dumped = simplejson.dumps(data, sort_keys=True, indent='    ')
    return '\n'.join([l.rstrip() for l in dumped.splitlines()])

def handle_object_get(request):
    object_id = request.path.split('/')[1]
    fields = request.args.get('fields', '').split(',')
    resp = db.get_object_by_id(object_id, fields)
    body = _pretty_dump(resp)
    return Response(body, mimetype='text/javascript')

def handle_object_post(request):
    obj = dict(request.form.items())
    resp = db.create_object(obj)
    body = _pretty_dump(resp)
    return Response(body, mimetype='text/javascript')

def handle_connection_get(request):
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    fields = request.args.get('fields', '').split(',')
    _, object_id, connection_type = request.path.split('/')
    resp = db.get_objects_by_connection(object_id, connection_type, limit,
        offset, fields)
    body = _pretty_dump({'data': resp})
    return Response(body, mimetype='text/javascript')

def handle_connection_post(request):
    obj = dict(request.form.items())
    _, object_id, connection_type = request.path.split('/')
    resp = db.generic_post(object_id, connection_type, obj)
    body = _pretty_dump(resp)
    return Response(body, mimetype='text/javascript')

@Request.application
def application(request):
    split_path = request.path[1:].split('/')
    if request.path == '/' and request.method == 'POST':
        return handle_object_post(request)
    elif len(split_path) == 1:
        return handle_object_get(request)
    elif len(split_path) == 2:
        if request.method == 'GET':
            return handle_connection_get(request)
        elif request.method == 'POST':
            return handle_connection_post(request)
    raise NotFound()

if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, application, use_reloader=True)