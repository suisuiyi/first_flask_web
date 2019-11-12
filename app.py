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

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login in.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login in.')
def admin(username, password):
    """create user"""
    db.create_all()
    user = User.query.first();
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user')
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('Done')



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


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('无效的输入.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash("登录成功")
            return redirect(url_for('index'))

        flash("无效的用户名和密码")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("已登出")
    return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')

            return redirect(url_for('edit', movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash("无效的输入")
            return redirect(url_for('index'))
        current_user.name = name
        db.session.commit()
        flash("设置已更新")
        return redirect(url_for('index'))
    return render_template('setting.html')

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
