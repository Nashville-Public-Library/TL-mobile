import subprocess
import os
import time

import pytest

@pytest.fixture(scope="session")
def server():
    
    command = ["flask", "run"]
    start = subprocess.Popen(command)
    time.sleep(9) # give it a few seconds to start up
    server_URL = "http://localhost:5000/"

    yield server_URL

    start.terminate()
    start.wait()

