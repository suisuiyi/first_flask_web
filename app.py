# -*- coding: utf-8 -*-

"""
@author: peter.dai
@project: first_flask_web
@file: app.py.py
@time: 2019/11/10 09:59
@desc:
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', name=name, movies=movies)


name = 'peter'
movies = [
    {'title': '流浪地球', 'year': '2019'},
    {'title': '千与千寻', 'year': '2001'},
    {'title': '海上钢琴师', 'year': '1998'},
    {'title': '复仇者联盟4', 'year': '2019'},
    {'title': '疯狂的外星人', 'year': '2019'},
    {'title': '寄生虫', 'year': '2019'}
]


if __name__ == '__main__':
    app.run(debug=True)