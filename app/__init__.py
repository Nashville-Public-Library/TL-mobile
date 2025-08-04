'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

from app.booth import views
from app.misc import views
from app.pwa import views
from app.status import views
from app.stream import views