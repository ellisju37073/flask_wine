#Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175


from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__, static_url_path='')

#connect to database
conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='wine',
                               buffered = True)
cursor = conn.cursor()

#Search zipcode database
@app.route('/searchwine/<searchwine>')
def searchwine(searchwine):
    # Get data from database
    cursor.execute("SELECT * FROM `wine` WHERE wine = %s", [searchwine])
    test = cursor.rowcount
    if test == 0:
        return searchwine + " was not found"
    else:
        searched = cursor.fetchall()
        return render_template('search.html', searched=searched)
    return render_template('search.html')

#update zipcode database population for a specified zip code
@app.route('/addwine/<updatewine> <updatebottles> <updatetype>')
def addbottles(updatewine, updatebottles, updatetype):
    cursor.execute("SELECT * FROM `wine` WHERE wine = %s and type = %s", [updatewine, updatetype])
    test = cursor.rowcount
    if test == 0:
        cursor.execute("INSERT INTO `wine` (bottles, wine, type" ") VALUES(%s, %s, %s);",
                       [updatebottles, updatewine, updatetype])
        return updatewine + "was added"
    
    else:
        cursor.execute("UPDATE `wine` SET bottles = (bottles + %s) WHERE wine = %s and type = %s;", [updatebottles, updatewine, updatetype])
        cursor.execute("SELECT * FROM `wine` WHERE wine = %s AND type = %s;", [updatewine,updatetype])
        test1 = cursor.rowcount
        if test1 == 0:
            return updatewine + "  failed to update"
        else:
            return 'Wine has been updated successfully for wine: %s' % updatewine

@app.route('/minuswine/<updatewinem> <updatebottlesm> <updatetypem> ')
def minusbottles(updatewinem, updatebottlesm, updatetypem):
    cursor.execute("SELECT * FROM `wine` WHERE wine = %s", [updatewinem])
    test = cursor.rowcount
    if test == 0:
        return updatewine + " was not found"
    
    else:
        cursor.execute("UPDATE `wine` SET bottles = (bottles - %s) WHERE wine = %s and type = %s;", [updatebottlesm, updatewinem, updatetypem])
        cursor.execute("SELECT * FROM `wine` WHERE wine = %s AND type = %s;", [updatewinem,updatetypem])
        test1 = cursor.rowcount
        if test1 == 0:
            return updatewine + "  failed to update"
        else:
            return 'Wine has been updated successfully for wine: %s' % updatewinem


#update webpage
@app.route('/add',methods = ['POST'])
def add():
       user = request.form['uwine']
       user2 = request.form['ubot']
       user3 = request.form['utype']

       return redirect(url_for('addbottles', updatewine=user, updatebottles=user2, updatetype=user3))

@app.route('/minus',methods = ['POST'])
def minus():
       user = request.form['uwinem']
       user2 = request.form['ubotm']
       user3 = request.form['utypem']

       return redirect(url_for('minusbottles', updatewinem=user, updatebottlesm=user2, updatetypem=user3))

#search page
@app.route('/search', methods=['GET'])
def search():
       user = request.args.get('swine')
       return redirect(url_for('searchwine', searchwine=user))


#root of web server and gots to template (login.html)
@app.route('/')
def root():
   return render_template('login.html')

#main
if __name__ == '__main__':
   app.run(debug = True, use_reloader=False)
