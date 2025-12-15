from flask import Blueprint, render_template, request, redirect, url_for
from models import User
from models.point_history import PointHistory
from models.db import db

point_bp = Blueprint('point', __name__, url_prefix='/points')


@point_bp.route('/consume', methods=['GET', 'POST'])
def consume():
    users = User.select()
    histories = (
        PointHistory
        .select()
        .join(User)
        .order_by(PointHistory.used_at.desc())
    )

    error_message = None

    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        use_point = int(request.form['use_point'])

        user = User.get_or_none(User.id == user_id)
        if not user:
            error_message = "ユーザーが存在しません"
        elif use_point <= 0:
            error_message = "消費ポイントは1以上で入力してください"
        elif user.point < use_point:
            error_message = "ポイントが不足しています"
        else:
            from models.db import db
            with db.atomic():
                user.point -= use_point
                user.save()

                PointHistory.create(
                    user=user,
                    used_point=use_point
                )

            return redirect(url_for('point.consume'))

    return render_template(
        'point_consume.html',
        users=users,
        items=histories,
        title='ポイント消費履歴',
        error_message=error_message   # ← ここが重要
    )
