import os
import sys

# Establece el directorio raíz del proyecto en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

print("syspath: ", sys.path[0])
