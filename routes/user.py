from flask import Blueprint, render_template, request, redirect, url_for
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():
    # データ取得
    users = User.select()
    return render_template('user_list.html', title='ユーザー一覧', items=users)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        point = request.form['point']

        User.create(
            name=name,
            age=age,
            birth_date=birth_date,
            gender=gender,
            point=point
        )

        return redirect(url_for('user.list'))

    return render_template('user_add.html')



@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.birth_date = request.form['birth_date']
        user.gender = request.form['gender']
        user.point = request.form['point']
        user.save()


        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)
