from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Product, Order
from peewee import fn

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
def list():
    products = Product.select()
    return render_template('product_list.html', title='製品一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        Product.create(name=name, price=price )
        return redirect(url_for('product.list'))
    
    return render_template('product_add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.save()
        return redirect(url_for('product.list'))

    return render_template('product_edit.html', product=product)

@product_bp.route('/api')
def api():
    products = Product.select()
    price_sum = {}
    for p in products:
        name = p.name
        price = float(p.price)
        if name in price_sum:
            price_sum[name] += price
        else:
            price_sum[name] = price
    return jsonify({'products': [{'name': name, 'price': price} for name, price in price_sum.items()]})