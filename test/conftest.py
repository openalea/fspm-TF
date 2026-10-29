import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFORMANCE = os.path.join(ROOT, "conformance")
sys.path.insert(0, CONFORMANCE)                 # conformance/generate.py builds the reference scenes
