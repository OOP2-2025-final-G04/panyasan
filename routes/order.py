from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, User, Product
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        order_date = datetime.now()
        order_count = request.form['order_count']
        Order.create(user=user_id, product=product_id, order_date=order_date, count=order_count)
        # ポイントを追加する
        user = User.get_by_id(user_id)
        product = Product.get_by_id(product_id)
        total_price = product.price * int(order_count)
        get_point = int(total_price / 100)
        user.point += get_point
        user.save()

        return redirect(url_for('order.list'))
    
    users = User.select()
    products = Product.select()
    return render_template('order_add.html', users=users, products=products)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    # 修正前のデータを取得
    order = Order.get_or_none(Order.id == order_id)
    user = User.get_by_id(order.user) # 購入者
    product = Product.get_by_id(order.product) # 製品

    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        # 修正前のポイントをなくす
        user.point -= int((product.price * int(order.count))/100) # 修正前に獲得していたポイントをマイナス
        user.save()
        # 修正後のデータを受け付ける
        order.user = request.form['user_id']
        order.product = request.form['product_id']
        order.count = request.form['order_count']
        order.save()
        # ポイントを追加する
        user = User.get_by_id(order.user)
        product = Product.get_by_id(order.product)
        total_price = product.price * int(order.count)
        get_point = int(total_price / 100)
        user.point += get_point
        user.save()
        return redirect(url_for('order.list'))

    users = User.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, users=users, products=products)
