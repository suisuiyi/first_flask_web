# -*- coding: utf-8 -*-

"""
@author: peter.dai
@project: first_flask_web
@file: app.py.py
@time: 2019/11/10 09:59
@desc:
"""

from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/home")
def hello():
    return '<h1> Hello Totoro!<h1> <img src ="http://helloflask.com/totoro.gif">'


@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name


@app.route('/test')
def test_url_for():
    print(url_for('hello'))

    print(url_for('user_page', name='nano'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))

    print(url_for('test_url_for', num=2))

    return 'Test Page'


if __name__ == '__main__':
    app.run(debug=True)