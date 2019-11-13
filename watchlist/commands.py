import click
from watchlist.models import User, Movie
from watchlist import app,db

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