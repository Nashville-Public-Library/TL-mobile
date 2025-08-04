'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

from app.pwa import views
from app.errors import views
