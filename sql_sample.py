# 接続確認用
import pymysql

print("データベース接続確認")

connection = pymysql.connect(
    host="localhost",
    db="mydb",
    user="root",
    password="",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

# 以下テーブルに合わせて変更
sql = "SELECT * FROM players"
cursor = connection.cursor()
cursor.execute(sql)
players = cursor.fetchall()

cursor.close()
connection.close()

for player in players:
    print(player["name"])