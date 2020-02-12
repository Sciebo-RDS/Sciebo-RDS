# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
app.run(port=8080, server='gevent')
