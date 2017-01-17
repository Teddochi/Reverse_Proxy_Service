# -*- coding: utf-8 -*-
# Adds the path to the main application to allow for testing

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app