import sys
import os

# Add your project directory to sys.path
path = '/home/kdornadula/planventure/planventure-api'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()
