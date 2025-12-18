from flask import Flask, render_template
from peewee import fn
from models import initialize_database
from models.user import User
from models.point_history import PointHistory
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ポイント用Blueprint
from routes.point import point_bp
app.register_blueprint(point_bp)


@app.route('/')
def index():
    # ユーザー別ポイント消費ランキング（TOP5）
    ranking = (
        User
        .select(
            User.name,
            fn.SUM(PointHistory.used_point).alias('total_point')
        )
        .join(PointHistory)
        .group_by(User.id)
        .order_by(fn.SUM(PointHistory.used_point).desc())
        .limit(5)
    )

    labels = [r.name for r in ranking]
    values = [r.total_point for r in ranking]

    # ★ ここが重要
    ranking_data = list(zip(labels, values))

    return render_template(
        'index.html',
        labels=labels,
        values=values,
        ranking_data=ranking_data
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
