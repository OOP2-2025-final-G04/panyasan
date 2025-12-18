from flask import Flask, render_template,jsonify
from models import initialize_database,User
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

@app.route('/api/stats/age-gender')
def get_age_gender_stats():
    # データベースから全ユーザーを取得
    users = User.select()

    # グラフの横軸ラベル (0代〜90代以上)
    labels = [f'{i*10}代' for i in range(10)]
    
    # 性別ごとのカウント用リスト (初期値すべて0)
    # インデックス 0=0代, 1=10代, ... 9=90代以上
    counts = {
        'M': [0] * 10, # 男性
        'F': [0] * 10, # 女性
        'O': [0] * 10  # その他
    }

    for user in users:
        # 年齢を取得 (未設定なら0歳扱い)
        age = user.age if user.age is not None else 0
        
        # 年代インデックスを計算 (例: 25歳//10 = 2)
        idx = int(age // 10)
        
        # 90代以上はすべて最後の枠(9)にまとめる
        if idx >= 10:
            idx = 9
            
        # 性別判定してカウントアップ
        gender = user.gender # M, F, O
        if gender in counts:
            counts[gender][idx] += 1

    # グラフ描画用データをJSON形式で返す
    return jsonify({
        'labels': labels,
        'datasets': [
            {
                'label': '男性',
                'data': counts['M'],
                'backgroundColor': 'rgba(54, 162, 235, 0.6)', # 青
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            },
            {
                'label': '女性',
                'data': counts['F'],
                'backgroundColor': 'rgba(255, 99, 132, 0.6)', # 赤
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            },
            {
                'label': 'その他',
                'data': counts['O'],
                'backgroundColor': 'rgba(75, 192, 192, 0.6)', # 緑
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
        ]
    })


# ホームページのルート
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
