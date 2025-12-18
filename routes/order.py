from flask import jsonify
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


# 日別売上合計を返すAPI
@order_bp.route('/api/sales/daily')
def daily_sales():
    # Orderテーブルから日付ごとに売上合計を集計
    from peewee import fn # 集計関数を使用するため（SUMとか）
    query = (Order
        .select(Order.order_date, fn.SUM(Product.price * Order.count).alias('total'))
        .join(Product) # OrdeerテーブルとProductテーブルを結合
        .group_by(fn.DATE(Order.order_date)) # 日付ごとにグループ化
        .order_by(Order.order_date)) # 日付順に並べ替え
    labels = [] # グラフX軸
    data = [] # グラフY軸
    for row in query:
        date_str = row.order_date.strftime('%Y-%m-%d') # 日付を文字列に変換
        if date_str not in labels: # その日付がまだX軸になければ追加
            labels.append(date_str)
            data.append(float(row.total))
        else: # 同じ日付が複数回出てきた場合は合算
            idx = labels.index(date_str)
            data[idx] += float(row.total)
    return jsonify({"labels": labels, "data": data})  # 日付リスト、売上リストをJSON形式で変換