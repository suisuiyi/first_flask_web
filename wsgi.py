# -*- coding: utf-8 -*-

"""
@author: peter.dai
@project: first_flask_web
@file: wsgi.py
@time: 2019/11/13 21:44
@desc:
"""
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app

