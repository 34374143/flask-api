from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, abort
import mysql.connector

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# 設置MySQL數據庫連接
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="farm"
)

# 創建數據庫游標
cursor = cnx.cursor()

# 定義API端點，查詢使用者資料
@app.route('/')
def index_page():
    cursor.execute(f"SELECT * FROM temhum")
    data = cursor.fetchall()
    title = ['sensor_id', 'location','temperature','humidity','timestamp']
    for i in range(len(data)):
        data[i] = dict(zip(title, data[i]))

    return render_template('index.html', data=data)

@app.route('/api/data', methods=['POST'])
def get_data():
    token = request.json['token']
    if token == '123456':
        cursor.execute(f"SELECT * FROM temhum")
        data = cursor.fetchall()
        title = ['sensor_id', 'location','temperature','humidity','timestamp']
        for i in range(len(data)):
            data[i] = dict(zip(title, data[i]))
        if data is None:
            return jsonify({'error': '資料不存在'})
        else:
            return jsonify(data)
        
@app.route('/api/add', methods=['POST'])
def add_data():
    token = request.json['token']
    if token == '123456':
        cursor.execute(f"INSERT INTO temhum (location, temperature, humidity) VALUES ('{request.json['location']}', '{request.json['temperature']}', '{request.json['humidity']}')")
        cnx.commit()
        return jsonify({'success': '資料新增成功'})
    else:
        return jsonify({'error': '權限不足'})
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)


