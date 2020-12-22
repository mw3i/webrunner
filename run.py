from app import app
import config 

from waitress import serve
serve(app, host=config.host, port=config.port, threads = 6)

