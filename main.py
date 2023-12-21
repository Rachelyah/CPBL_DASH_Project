from flask import Flask,render_template,url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app1 import dash1
from dash_file.dash_index import index

application = DispatcherMiddleware(
    index.server,
    {"/dash/index": index.server,
    "/dash/app1": dash1.server,
    }
)

if __name__ == "__main__":
    run_simple("localhost", 8080, application, use_debugger=True, use_reloader=True)