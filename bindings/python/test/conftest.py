import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))  # bindings/python/test
CONFORMANCE = os.path.join(ROOT, "conformance")
sys.path.insert(0, CONFORMANCE)                 # conformance/generate.py builds the reference scenes
