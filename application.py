'''
© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''
import os

# AWS EB default is to look for flask instance variable called application.
from app import app as application

if __name__ == "__main__":
    if 'nt' in os.name:
        application.run(debug=True)
    else:
        application.run()