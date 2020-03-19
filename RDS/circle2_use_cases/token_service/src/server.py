from src import bootstrap

if __name__ == "__main__":
    app = bootstrap("UseCaseTokenStorage", all=True)

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    app.run(port=8080, server='gevent')
