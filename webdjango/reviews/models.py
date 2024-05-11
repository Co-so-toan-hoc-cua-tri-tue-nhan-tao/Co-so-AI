from django.db import models
import numpy as np
from django.contrib.auth.models import User
class Wine(models.Model):
    name = models.CharField(max_length=200)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __unicode__(self):
        return self.name
class Review(models.Model):
    RATING_CHOICES=(
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    )
    wine = models.ForeignKey(Wine,on_delete = models.DO_NOTHING)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])


'''
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Product:
    def __init__(self, name):
        self.name = name
        self.rating = 0
        self.comments = []

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.rating += rating
        else:
            raise ValueError("Rating must be between 1 and 5.")

    def add_comment(self, comment):
        self.comments.append(comment)

# Dưới đây là một số sản phẩm mẫu để demo
products = {
    "laptop": Product("Laptop"),
    "phone": Product("Phone"),
    "headphones": Product("Headphones")
}

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/product/<product_name>', methods=['GET', 'POST'])
def product_detail(product_name):
    product = products.get(product_name)
    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']
        try:
            product.add_rating(rating)
            product.add_comment(comment)
        except ValueError as e:
            return str(e)
        return redirect(url_for('product_detail', product_name=product_name))
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
'''