from flask import Flask, request, jsonify, send_from_directory, render_template
import mysql.connector
import os

# 确保 templates 文件夹路径正确
app = Flask(__name__)

# 配置 MySQL 数据库连接
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database',
    'raise_on_warnings': True
}

@app.route('/')
def index():
    return render_template('indax.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/saveCase', methods=['POST'])
def save_case():
    try:
        # 获取前端发送的案件数据
        data = request.get_json()
        case_name = data.get('case_name')
        judgment_content = data.get('judgment_content')
        case_process = data.get('case_process')
        trial_process = data.get('trial_process')

        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 插入案件数据到数据库
        insert_query = "INSERT INTO cases (case_name, judgment_content, case_process, trial_process) VALUES (%s, %s, %s, %s)"
        values = (case_name, judgment_content, case_process, trial_process)
        cursor.execute(insert_query, values)

        # 提交更改并关闭连接
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Case added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getCases', methods=['GET'])
def get_cases():
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 查询所有案件数据
        select_query = "SELECT * FROM cases"
        cursor.execute(select_query)
        cases = cursor.fetchall()

        # 关闭连接
        cursor.close()
        conn.close()

        return jsonify(cases), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/deleteCase/<int:case_id>', methods=['DELETE'])
def delete_case(case_id):
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 删除指定 ID 的案件
        delete_query = "DELETE FROM cases WHERE id = %s"
        cursor.execute(delete_query, (case_id,))

        # 提交更改并关闭连接
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Case deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    