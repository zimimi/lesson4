from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Створити стовбці в таблиці
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    side = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

# Головна сторінка
@app.route('/')
def index():
    return render_template ("index.html")


@app.route('/read_posts')
def read():
    id = request.args.get('id')
    lim = request.args.get('lim')
    if id:
        articles = Article.query.filter(Article.id.contains(int(id))).all()
    elif lim:
        articles = Article.query.order_by(Article.id.desc()).limit(lim)
    else:
        #articles = Article.query.limit(0)
        articles = Article.query.order_by(Article.date.desc()).all()
    return render_template ("read_posts.html", articles=articles)


# Обробка кнопки Detail
@app.route('/read_posts/<int:id>')
def post_detail(id):
   article = Article.query.get(id)
   return render_template ("posts_detail.html", article=article)


# Видалити запис
@app.route('/read_posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/read_posts')
    except:
        return "Delete error"


# Додати новий запис
@app.route('/create_post', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        side = request.form['side']
        color = request.form['color']
        type = request.form['type']
        people = request.form['people']
        title = request.form['title']
        description = request.form['description']

        article = Article(side=side, color=color, type=type, people=people, title=title, description=description)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/read_posts')
        except:
            return 'Some Error Occur'
    else:
        return render_template('create_post.html')


# Змінити наявний запис
@app.route('/read_posts/<int:id>/update_post', methods=['POST', 'GET'])
def posts_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.side = request.form['side']
        article.color = request.form['color']
        article.type = request.form['type']
        article.people = request.form['people']
        article.title = request.form['title']
        article.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/read_posts')
        except:
            return 'Update error'
    else:
        return render_template('update_post.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
