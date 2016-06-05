from flask import Flask, render_template
from flask import request
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from flask_wtf import Form
from wtforms import SelectField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'

db = SQLAlchemy(app)


#  категория
class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(1024))

    def __repr__(self):
        return '<Category %s>' % self.name

    def __unicode__(self):
        return self.name


#  подкатегория
class SubCategory(db.Model):
    __tablename__ = 'sub_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(1024))
    category_id = db.Column(Integer, ForeignKey('category.id'))
    category = db.relationship("Category", backref="Ctegory.id")

    def __repr__(self):
        return '<SubCategory %s>' % self.name

    def __unicode__(self):
        return self.name

#  создание таблиц
db.create_all()
#  заполнение базы
#  если записи отсутствуют
if len(Category.query.all()) is 0:
    for name in ['фрукты', 'напитки', 'молочные продукты']:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()

if len(SubCategory.query.all()) is 0:
    for name in ['апельсины', 'яблоки', 'груши']:
        sub_category = SubCategory(category_id=1, name=name)
        db.session.add(sub_category)

    for name in ['сок', 'вода', 'газировка']:
        sub_category = SubCategory(category_id=2, name=name)
        db.session.add(sub_category)

    for name in ['молоко', 'сметана', 'масло']:
        sub_category = SubCategory(category_id=3, name=name)
        db.session.add(sub_category)
    db.session.commit()


class FormCategory(Form):
    category = SelectField(u'Категория', coerce=int)
    sub_category = SelectField(u'Под категория', coerce=int)

    def __init__(self, *args, **kwargs):
        super(FormCategory, self).__init__(*args, **kwargs)
        self.category.choices = \
            [(g.id, u"%s" % g.name) for g in Category.query.order_by('name')]
        #  выбранное поле по умолчанию
        self.category.choices.insert(0, (0, u"Не выбрана"))

        self.sub_category.choices = list()
        #  выбранное поле по умолчанию
        self.sub_category.choices.insert(0, (0, u"Не выбрана"))


@app.route('/')
def index():
    form = FormCategory()
    return render_template('index.html',
                           form=form
                           )


@app.route('/get_sub_category', methods=('GET', 'POST'))
def get_sub_category():
    category_id = request.form['category']
    item_list = SubCategory.query.filter_by(category_id=category_id).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.name
    return json.dumps(result_list)

if __name__ == '__main__':
    app.run(debug=True)
