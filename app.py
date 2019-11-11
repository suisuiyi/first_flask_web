# -*- coding: utf-8 -*-

"""
@author: peter.dai
@project: first_flask_web
@file: app.py.py
@time: 2019/11/10 09:59
@desc:
"""
import os
import sys
import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)


@app.cli.command()
def forge():
    db.create_all()

    name = "peter"
    movies = [
        {'title': '流浪地球', 'year': '2019'},
        {'title': '千与千寻', 'year': '2001'},
        {'title': '海上钢琴师', 'year': '1998'},
        {'title': '复仇者联盟4', 'year': '2019'},
        {'title': '疯狂的外星人', 'year': '2019'},
        {'title': '寄生虫', 'year': '2019'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Init database.")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route("/")
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)



if __name__ == '__main__':
    app.run(debug=True)
