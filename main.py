import functools
import time

from flask import Flask, session
from flask import redirect
from flask import request, make_response
from flask import render_template
from flask import url_for

from db import *

# 生成一个app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'lab3'

# 对app执行请求页面地址到函数的绑定
@app.route("/", methods=("GET", "POST"))
@app.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        # 客户端在login页面发起的POST请求
        username = request.form["username"]
        password = request.form["password"]
        ipaddr   = request.form["ipaddr"]
        database = request.form["database"]

        db = db_login(username, password, ipaddr, database)

        if db == None:
            return render_template("login_fail.html")
        else:
            session['username'] = username
            session['password'] = password
            session['ipaddr'] = ipaddr
            session['database'] = database

            return redirect(url_for('table'))
    else :
        # 客户端GET 请求login页面时
        return render_template("login.html")

# 请求url为host/table的页面返回结果
@app.route("/table", methods=(["GET", "POST"]))
def table():
    # 出于简单考虑，每次请求都需要连接数据库，可以尝试使用其它context保存数据库连接
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])

    else:
        return redirect(url_for('login'))
    
    banks = db_showbanks(db)
    assists = db_showassists(db)

    db_close(db)
    if request.method == "POST":
        if 'clear' in request.form:
            return render_template("table.html", banks='', assists='')
        elif 'search' in request.form:
            return render_template("table.html", banks=banks, assists=assists)
        elif 'cli_add' in request.form:
            return redirect(url_for("cli_add"))
        elif 'cli_del' in request.form:
            return redirect(url_for("cli_del"))
        elif 'cli_alt' in request.form:
            return redirect(url_for("cli_alt"))
        elif 'cli_search' in request.form:
            return redirect(url_for("cli_search"))
        elif 'acc_open' in request.form:
            return redirect(url_for("acc_open"))
        elif 'acc_close' in request.form:
            return redirect(url_for("acc_close"))
        elif 'acc_alt' in request.form:
            return redirect(url_for("acc_alt"))
        elif 'acc_search' in request.form:
            return redirect(url_for("acc_search"))
        elif 'debt_add' in request.form:
            return redirect(url_for("debt_add"))
        elif 'debt_del' in request.form:
            return redirect(url_for("debt_del"))
        elif 'debt_search' in request.form:
            return redirect(url_for("debt_search"))
        elif 'debt_pay' in request.form:
            return redirect(url_for("debt_pay"))
        elif 'by_types' in request.form:
            return redirect(url_for("by_types"))
        elif 'by_time' in request.form:
            return redirect(url_for("by_time"))

    else:
        return render_template("table.html", banks=banks, assists=assists)

# 客户管理
@app.route("/cli/cli_add", methods=("GET", "POST"))
def cli_add():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'cli_add' in request.form:
            cli_id = request.form["cli_id"]
            name = request.form["cli_name"]
            tel = request.form["cli_tel"]
            addr = request.form["cli_addr"]
            con_name = request.form["con_name"]
            con_tel = request.form["con_tel"]
            con_email = request.form["con_email"]
            con_relat = request.form["con_relat"]
            assist_id = request.form["assist_id"]
            if assist_id != "":
                sql = 'INSERT INTO Clients VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'\
                     % (cli_id, name, tel, addr, con_name, con_tel, con_email, con_relat, assist_id)
            else:
                sql = 'INSERT INTO Clients VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", null)'\
                     % (cli_id, name, tel, addr, con_name, con_tel, con_email, con_relat)

            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("cli/cli_add_fail.html")
    
    else:
        return render_template("cli/cli_add.html")

@app.route("/cli/cli_del", methods=("GET", "POST"))
def cli_del():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'cli_del' in request.form:
            cli_id = request.form["cli_id"]
            sql = 'DELETE FROM Clients WHERE id = "%s"' % (cli_id)
            print(sql)

            try:
                cursor.execute(sql)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("cli/cli_del_fail.html")

    else:
        return render_template("cli/cli_del.html")

@app.route("/cli/cli_alt", methods=("GET", "POST"))
def cli_alt():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        else:
            sql = ''
            if 'alt_cli' in request.form:
                cli_id = request.form["cli_id"]
                tel = request.form["cli_tel"]
                addr = request.form["cli_addr"]
                sql = 'UPDATE Clients SET tel = "%s", addr = "%s" \
                       WHERE id = "%s"' % (tel, addr, cli_id)
            elif 'alt_con' in request.form:
                cli_id = request.form["cli_id"]
                name = request.form["con_name"]
                tel = request.form["con_tel"]
                email = request.form["con_email"]
                relat = request.form["con_relat"]
                sql = 'UPDATE Clients  SET con_name = "%s", con_tel = "%s", \
                       con_email = "%s", con_relat = "%s" \
                       WHERE id = "%s"' % (name, tel, email, relat, cli_id)
            elif 'alt_assist' in request.form:
                cli_id = request.form["cli_id"]
                assist_id = request.form["assist_id"]
                if assist_id != "":
                    sql = 'UPDATE Clients SET assist_id = "%s" \
                           WHERE id = "%s"' % (assist_id, cli_id)
                else:
                    sql = 'UPDATE Clients SET assist_id = null \
                           WHERE id = "%s"' % (cli_id)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("cli/cli_alt_fail.html")

    else:
        return render_template("cli/cli_alt.html")


@app.route("/cli/cli_search", methods=("GET", "POST"))
def cli_search():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        else:
            sql = ''
            if 'by_id' in request.form:
                cli_id = request.form["cli_id"]
                sql = 'SELECT * FROM Clients WHERE id = "%s"' % (cli_id)
            elif 'by_name' in request.form:
                name = request.form["cli_name"]
                sql = 'SELECT * FROM Clients WHERE name = "%s"' % (name)
            elif 'search_all' in request.form:
                sql = 'SELECT * FROM Clients'

            print(sql)
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return render_template('cli/cli_search.html', rows = rows)
            except MySQLdb.Error as e:
                print("失败")
                return render_template('cli/cli_search.html', rows = '')

    else:
        return render_template("cli/cli_search.html")

@app.route("/acc/acc_open", methods=("GET", "POST"))
def acc_open():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'acc_open' in request.form:
            sql_accounts = ""
            bank_name = '"' + request.form["bank_name"] + '"'
            date = '"' + time.strftime("%Y-%m-%d", time.localtime()) + '"'
            cli_id = ["", "", "", "", ""]
            if request.form["cli_id1"] == "":
                cli_id[0] = None
            else:
                cli_id[0] = '"' + request.form["cli_id1"] + '"'

            if request.form["cli_id2"] == "":
                cli_id[1] = None
            else:
                cli_id[1] = '"' + request.form["cli_id2"] + '"'

            if request.form["cli_id3"] == "":
                cli_id[2] = None
            else:
                cli_id[2] = '"' + request.form["cli_id3"] + '"'

            if request.form["cli_id4"] == "":
                cli_id[3] = None
            else:
                cli_id[3] = '"' + request.form["cli_id4"] + '"'

            if request.form["cli_id5"] == "":
                cli_id[4] = None
            else:
                cli_id[4] = '"' + request.form["cli_id5"] + '"'
            
            if request.form["acc_type"] == "save":
                acc_type = '"' + "save" + '"'
                int_rate = request.form["int_rate"]
                cur_type = request.form["cur_type"]
                cur_type = int(cur_type)
                if int_rate=="":
                    return render_template("acc/acc_open_fail.html")
                else:
                    int_rate = float(int_rate)
            elif request.form["acc_type"] == "check":
                acc_type = '"' + "check" + '"'
                overdraft = request.form["overdraft"]
                if overdraft == "":
                    return render_template("acc/acc_open_fail.html")
                else:
                    overdraft = float(overdraft)
            
            try:
                sql_accounts = 'INSERT INTO Accounts VALUES(null, %s, 0.0, %s, %s, %s)'\
                               % (bank_name, date, date, acc_type)
                print(sql_accounts)
                cursor.execute(sql_accounts)
                acc_num = db.insert_id()
                acc_num = int(acc_num)
                sql_acc_type = ""
                if request.form["acc_type"] == "save":
                    sql_acc_type = 'INSERT INTO Save_accounts VALUES(%s, %f, %d)'\
                                   % (acc_num, int_rate, cur_type)
                elif request.form["acc_type"] == "check":
                    sql_acc_type = 'INSERT INTO Check_accounts VALUES(%s, %f)'\
                                   % (acc_num, overdraft)
                print(sql_acc_type)
                cursor.execute(sql_acc_type)
                for i in range(5):
                    if cli_id[i] != None:
                        sql_cli_acc = 'INSERT INTO Cli_Acc VALUES(%s, %d)'\
                                      % (cli_id[i], acc_num)
                        print(sql_cli_acc)
                        cursor.execute(sql_cli_acc)
                        sql_cba = 'INSERT INTO Cli_Bank_Acctype VALUES(%s, %s, %d, %s)'\
                                  % (cli_id[i], bank_name, acc_num, acc_type)
                        print(sql_cba)
                        cursor.execute(sql_cba)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("acc/acc_open_fail.html")
    
    else:
        return render_template("acc/acc_open.html")

@app.route("/acc/acc_close", methods=("GET", "POST"))
def acc_close():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'acc_close' in request.form:
            acc_num = int(request.form["acc_num"])
            cli_id = request.form["cli_id"]
            sql_get = 'SELECT balance, acc_type FROM Accounts, Cli_Acc \
                      WHERE Accounts.acc_num = Cli_Acc.acc_num \
                      AND Accounts.acc_num = %d AND Cli_Acc.cli_id = "%s"'\
                      % (acc_num, cli_id)
            print(sql_get)
            try:
                cursor.execute(sql_get)
                balance, acc_type = cursor.fetchall()[0]
                balance = float(balance)
                if balance != 0:
                    return render_template("acc/acc_close_fail.html")
            except:
                return render_template("acc/acc_close_fail.html")

            sql1 = 'DELETE FROM Cli_Bank_Acctype WHERE acc_num = %d' % (acc_num)
            sql2 = 'DELETE FROM Cli_Acc WHERE acc_num = %d' % (acc_num)
            if acc_type == "save":
                sql3 = 'DELETE FROM Save_accounts WHERE acc_num = %d' % (acc_num)
            elif acc_type == "check":
                sql3 = 'DELETE FROM Check_accounts WHERE acc_num = %d' % (acc_num)
            sql4 = 'DELETE FROM Accounts WHERE acc_num = %d' % (acc_num)
            print(sql1)
            print(sql2)
            print(sql3)
            print(sql4)
            try:
                cursor.execute(sql1)
                cursor.execute(sql2)
                cursor.execute(sql3)
                cursor.execute(sql4)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("acc/acc_close_fail.html")

    else:
        return render_template("acc/acc_close.html")

@app.route("/acc/acc_alt", methods=("GET", "POST"))
def acc_alt():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        else:
            sql_list = []
            if 'save' in request.form:
                acc_num = int(request.form["acc_num"])
                amount = float(request.form["amount"])
                if amount < 0:
                    return render_template("acc/acc_alt_fail.html")
                sql_get = 'SELECT balance FROM Accounts WHERE acc_num = %d' \
                          % acc_num
                try:
                    cursor.execute(sql_get)
                    balance = cursor.fetchall()[0][0]
                    balance = float(balance)
                except:
                    return render_template("acc/acc_alt_fail.html")
                date = time.strftime("%Y-%m-%d", time.localtime())
                sql = 'UPDATE Accounts SET balance = %f, visit_date = "%s" \
                       WHERE acc_num = %d' % (balance+amount, date, acc_num)
                sql_list.append(sql)
            
            elif 'exploit' in request.form:
                acc_num = int(request.form["acc_num"])
                cli_id = request.form["cli_id"]
                amount = float(request.form["amount"])
                sql_get = 'SELECT balance FROM ( SELECT balance \
                           FROM Accounts , Cli_Acc \
                           WHERE Accounts.acc_num = Cli_Acc.acc_num \
                           AND Accounts.acc_num = %d AND Cli_Acc.cli_id = %s) a' \
                           % (acc_num, cli_id)
                try:
                    cursor.execute(sql_get)
                    balance = cursor.fetchall()[0][0]
                    balance = float(balance)
                except:
                    return render_template("acc/acc_alt_fail.html")
                sql_get = 'SELECT acc_type FROM Accounts \
                           WHERE acc_num = %d' % (acc_num)
                print(sql_get)
                cursor.execute(sql_get)
                acc_type = cursor.fetchall()[0][0]
                if acc_type == 'save':
                    if balance < amount or amount < 0:
                        return render_template("acc/acc_alt_fail.html")
                elif acc_type == 'check':
                    sql_get = 'SELECT overdraft FROM Check_accounts \
                              WHERE acc_num = %d' % (acc_num)
                    print(sql_get)
                    cursor.execute(sql_get)
                    overdraft = cursor.fetchall()[0][0]
                    overdraft = float(overdraft)
                    if overdraft+balance < amount or amount < 0:
                        return render_template("acc/acc_alt_fail.html")
                date = time.strftime("%Y-%m-%d", time.localtime())
                sql = 'UPDATE Accounts SET balance = %f, visit_date = "%s" \
                       WHERE acc_num = %d' % (balance-amount, date, acc_num)
                sql_list.append(sql)
            
            elif 'alt_bank' in request.form:
                acc_num = int(request.form["acc_num"])
                bank_name = request.form["bank_name"]
                sql1 = 'UPDATE Cli_Bank_Acctype SET bank_name = "%s" \
                      WHERE acc_num = %d' % (bank_name, acc_num)
                sql2 = 'UPDATE Accounts SET bank_name = "%s" \
                      WHERE acc_num = %d' % (bank_name, acc_num)
                sql_list.append(sql1)
                sql_list.append(sql2)

            elif 'add_cli' in request.form:
                acc_num = int(request.form["acc_num"])
                cli_id = request.form["cli_id"]
                sql_get = 'SELECT bank_name, acc_type FROM Accounts \
                           WHERE Accounts.acc_num = %d' % (acc_num)
                print(sql_get)
                try:
                    cursor.execute(sql_get)
                    bank_name, acc_type = cursor.fetchall()[0]
#                    print(bank_name, acc_type)
                except:
                    return render_template("acc/acc_alt_fail.html")
                sql1 = 'INSERT INTO Cli_Bank_Acctype VALUES("%s", "%s", %d, "%s")' \
                       % (cli_id, bank_name, acc_num, acc_type)
                sql2 = 'INSERT INTO Cli_Acc VALUES ("%s", %d)' % (cli_id, acc_num)
                sql_list.append(sql1)
                sql_list.append(sql2)

            elif 'del_cli' in request.form:
                acc_num = int(request.form["acc_num"])
                cli_id = request.form["cli_id"]
                sql_get = 'SELECT COUNT(*) FROM Cli_Acc \
                          WHERE acc_num = %d' % (acc_num)
                print(sql_get)
                try:
                    cursor.execute(sql_get)
                    sum = cursor.fetchall()[0][0]
                    sum = int(sum)
                    if sum == 0:
                        return render_template("acc/acc_alt_fail.html")
                except:
                    return render_template("acc/acc_alt_fail.html")
                sql1 = 'DELETE FROM Cli_Bank_Acctype \
                       WHERE cli_id = "%s" and acc_num = %d' % (cli_id, acc_num)
                sql2 = 'DELETE FROM Cli_Acc \
                       WHERE cli_id = "%s" and acc_num = %d' % (cli_id, acc_num)
                sql_list.append(sql1)
                sql_list.append(sql2)

            try:
                for sql in sql_list:
                    print(sql)
                    cursor.execute(sql)
                    db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("acc/acc_alt_fail.html")

    else:
        return render_template("acc/acc_alt.html")


@app.route("/acc/acc_search", methods=("GET", "POST"))
def acc_search():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        else:
            sql = ''
            if 'by_acc_num' in request.form:
                acc_num = int(request.form["acc_num"])
                sql = 'SELECT * FROM Accounts, Cli_Acc \
                      WHERE Accounts.acc_num = Cli_Acc.acc_num \
                      and Accounts.acc_num = "%d"' % (acc_num)
            elif 'by_bank' in request.form:
                bank_name = request.form["bank_name"]
                sql = 'SELECT * FROM Accounts, Cli_Acc \
                      WHERE Accounts.acc_num = Cli_Acc.acc_num \
                      and Accounts.bank_name = "%s"' % (bank_name)
            elif 'by_cli_id' in request.form:
                cli_id = request.form["cli_id"]
                sql = 'SELECT * FROM Accounts, Cli_Acc \
                      WHERE Accounts.acc_num = Cli_Acc.acc_num \
                      and cli_id = "%s"' % (cli_id)
            elif 'search_all' in request.form:
                sql = 'SELECT * FROM Accounts, Cli_Acc \
                      WHERE Accounts.acc_num = Cli_Acc.acc_num'
            print(sql)
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
#                print(rows)
                return render_template('acc/acc_search.html', rows = rows)
            except MySQLdb.Error as e:
                print("失败")
                return render_template('acc/acc_search.html', rows = '')

    else:
        return render_template("acc/acc_search.html")

@app.route("/debt/debt_add", methods=("GET", "POST"))
def debt_add():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'debt_add' in request.form:
            sql_debts = ""
            bank_name = '"' + request.form["bank_name"] + '"'
            amount = float(request.form["amount"])
            cli_id = ["", "", "", "", ""]
            if request.form["cli_id1"] == "":
                cli_id[0] = None
            else:
                cli_id[0] = '"' + request.form["cli_id1"] + '"'

            if request.form["cli_id2"] == "":
                cli_id[1] = None
            else:
                cli_id[1] = '"' + request.form["cli_id2"] + '"'

            if request.form["cli_id3"] == "":
                cli_id[2] = None
            else:
                cli_id[2] = '"' + request.form["cli_id3"] + '"'

            if request.form["cli_id4"] == "":
                cli_id[3] = None
            else:
                cli_id[3] = '"' + request.form["cli_id4"] + '"'

            if request.form["cli_id5"] == "":
                cli_id[4] = None
            else:
                cli_id[4] = '"' + request.form["cli_id5"] + '"'
            
            sql_debts = 'INSERT INTO Debts VALUES(null, %s, %f, 0.0)'\
                           % (bank_name, amount)
            print(sql_debts)
            try:
                cursor.execute(sql_debts)
                debt_num = db.insert_id()
                debt_num = int(debt_num)
                for i in range(5):
                    if cli_id[i] != None:
                        sql_cli_debt = 'INSERT INTO Cli_Debt VALUES(%s, %d)'\
                                      % (cli_id[i], debt_num)
                        print(sql_cli_debt)
                        cursor.execute(sql_cli_debt)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("debt/debt_add_fail.html")
    
    else:
        return render_template("debt/debt_add.html")

@app.route("/debt/debt_del", methods=("GET", "POST"))
def debt_del():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'debt_del' in request.form:
            debt_num = int(request.form["debt_num"])
            cli_id = request.form["cli_id"]
            sql_get = 'SELECT amount, paid_amount FROM Debts \
                      WHERE debt_num = %d' % (debt_num)
            print(sql_get)
            try:
                cursor.execute(sql_get)
                amount, paid_amount = cursor.fetchall()[0]
                amount = float(amount)
                paid_amount = float(paid_amount)
                if amount != paid_amount:
                    return render_template("debt/debt_del_fail.html")
            except:
                return render_template("debt/debt_del_fail.html")

            sql1 = 'DELETE FROM Debts_pay WHERE debt_num = %d' % (debt_num)
            sql2 = 'DELETE FROM Cli_Debt WHERE debt_num = %d' % (debt_num)
            sql3 = 'DELETE FROM Debts WHERE debt_num = %d' % (debt_num)
            print(sql1)
            print(sql2)
            print(sql3)
            try:
                cursor.execute(sql1)
                cursor.execute(sql2)
                cursor.execute(sql3)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("debt/debt_del_fail.html")
    else:
        return render_template("debt/debt_del.html")

@app.route("/debt/debt_search", methods=("GET", "POST"))
def debt_search():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        else:
            sql = ''
            if 'by_debt_num' in request.form:
                debt_num = int(request.form["debt_num"])
                sql = 'SELECT Debts.debt_num, bank_name, amount, paid_amount, cli_id \
                      FROM Debts, Cli_Debt \
                      WHERE Debts.debt_num = Cli_Debt.debt_num \
                      and Debts.debt_num = %d' % (debt_num)
            elif 'by_cli_id' in request.form:
                cli_id = request.form["cli_id"]
                sql = 'SELECT Debts.debt_num, bank_name, amount, paid_amount, cli_id \
                      FROM Debts, Cli_Debt \
                      WHERE Debts.debt_num = Cli_Debt.debt_num \
                      and cli_id = "%s"' % (cli_id)
            elif 'by_bank_name' in request.form:
                bank_name = request.form["bank_name"]
                sql = 'SELECT Debts.debt_num, bank_name, amount, paid_amount, cli_id \
                      FROM Debts, Cli_Debt \
                      WHERE Debts.debt_num = Cli_Debt.debt_num \
                      and bank_name = "%s"' % (bank_name)
            elif 'search_all' in request.form:
                sql = 'SELECT Debts.debt_num, bank_name, amount, paid_amount, cli_id \
                      FROM Debts, Cli_Debt \
                      WHERE Debts.debt_num = Cli_Debt.debt_num'

            print(sql)
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return render_template('debt/debt_search.html', rows = rows)
            except MySQLdb.Error as e:
                print("失败")
                return render_template('debt/debt_search.html', rows = '')

    else:
        return render_template("debt/debt_search.html")

@app.route("/debt/debt_pay", methods=("GET", "POST"))
def debt_pay():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('table'))
        elif 'debt_pay' in request.form:
            debt_num = int(request.form["debt_num"])
            pay_date = '"' + time.strftime("%Y-%m-%d", time.localtime()) + '"'
            pay_sum = float(request.form["pay_sum"])
            sql_get = 'SELECT amount, paid_amount FROM Debts WHERE debt_num = %d' \
                      % (debt_num)
            try:
                cursor.execute(sql_get)
                amount, paid_amount = cursor.fetchall()[0]
                amount = float(amount)
                paid_amount = float(paid_amount)
            except:
                return render_template("debt/debt_pay_fail.html")
            if pay_sum <= 0 or pay_sum+paid_amount > amount:
                return render_template("debt/debt_pay_fail.html")

            sql1 = 'INSERT INTO Debts_pay VALUES(%d, %s, %f)' \
                   % (debt_num, pay_date, pay_sum)
            sql2 = 'UPDATE Debts SET paid_amount = %f WHERE debt_num = %d' \
                   % (pay_sum+paid_amount, debt_num)
            print(sql1)
            print(sql2)
            try:
                cursor.execute(sql1)
                cursor.execute(sql2)
                db.commit()
                return redirect(url_for('table'))
            except:
                db.rollback()
                return render_template("debt/debt_pay_fail.html")

    else:
        return render_template("debt/debt_pay.html")

@app.route("/by_types", methods=("GET", "POST"))
def by_types():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        return redirect(url_for('table'))
    else:        
        sql1 = 'SELECT COUNT(*) FROM Save_accounts'
        sql2 = 'SELECT COUNT(*) FROM Check_accounts'
        sql3 = 'SELECT COUNT(*) FROM Debts'
        try:
            cursor.execute(sql1)
            cnt = cursor.fetchall()[0][0]
            cnt_save = int(cnt)
            cursor.execute(sql2)
            cnt = cursor.fetchall()[0][0]
            cnt_check = int(cnt)
            cursor.execute(sql3)
            cnt = cursor.fetchall()[0][0]
            cnt_debt = int(cnt)
            print(cnt_save, cnt_check, cnt_debt)
            return render_template('/by_types.html', cnt_save=cnt_save, cnt_check=cnt_check, cnt_debt=cnt_debt)
        except:
            return render_template('/by_types.html', cnt_save=0, cnt_check=0, cnt_debt=0)

@app.route("/by_time", methods=("GET", "POST"))
def by_time():
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
        cursor = db.cursor()
    else:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        return redirect(url_for('table'))
    else:        
        sql_acc = 'SELECT open_date, COUNT(*) FROM Accounts \
                   GROUP BY open_date'
        sql_debt = 'SELECT pay_date, COUNT(*) FROM Debts_pay \
                   GROUP BY pay_date'
        try:
            cursor.execute(sql_acc)
            acc_rows = cursor.fetchall()
            print(acc_rows)
            cursor.execute(sql_debt)
            debt_rows = cursor.fetchall()
            print(debt_rows)
            return render_template('/by_time.html', acc_rows=acc_rows, debt_rows=debt_rows)
        except:
            return render_template('/by_time.html', acc_rows='', debt_rows='')

# 测试URL下返回html page
@app.route("/hello")
def hello():
    return "hello world!"

#返回不存在页面的处理
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":

    app.run(host = "0.0.0.0", debug=True)
