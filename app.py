import pymysql

# 连接数据库
mydb = pymysql.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

# 创建游标
mycursor = mydb.cursor()

# 创建案件表
mycursor.execute("CREATE TABLE IF NOT EXISTS cases (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), judgment TEXT, process TEXT, trial TEXT)")

# 插入案件数据
case = ("Case Name", "Judgment Content", "Case Process", "Trial Process")
sql = "INSERT INTO cases (name, judgment, process, trial) VALUES (%s, %s, %s, %s)"
mycursor.execute(sql, case)

# 提交更改
mydb.commit()

# 查询案件数据
mycursor.execute("SELECT * FROM cases")
cases = mycursor.fetchall()
for case in cases:
    print(case)

# 关闭连接
mydb.close()
