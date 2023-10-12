from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_USER"] = "sql11652827"
app.config["MYSQL_PASSWORD"] = "dF6bVt3XGq"
app.config["MYSQL_HOST"] = "sql11.freemysqlhosting.net"
app.config["MYSQL_DB"] = "sql11652827"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

mysql.init_app(app)


@app.route("/")
def CONNECT_DB():
    CS = mysql.connection.cursor()
    CS.execute("""CREATE TABLE Users (id INTEGER, name VARCHAR(20))""")
    CS.execute('''INSERT INTO Users VALUES (1, 'Harry')''')
    CS.execute('''INSERT INTO Users VALUES (2, 'Arthor')''')
    mysql.connection.commit()
    return 'Executed successfully'

    # CS.execute("""SELECT * FROM Users""")
    # Executed_DATA = CS.fetchall()
    # print(Executed_DATA)
    # return str(Executed_DATA[1]["name"])


if __name__ == "__main__":
    app.run(debug=True)