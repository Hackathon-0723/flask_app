# test接続確認用,OK
import pymysql

print("データベース接続確認")

connection = pymysql.connect(
    host="localhost",
    db="test",
    user="root",
    password="",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

# 以下テーブルに合わせて変更
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM post"
        cursor.execute(sql)

        dbdata = cursor.fetchall()
        for rows in dbdata:
            print(rows)

finally:
    connection.close()

