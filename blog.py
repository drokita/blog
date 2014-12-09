from flask import Flask, render_template, request, session, \
   flash, redirect, url_for, g
import sqlite3
import os
from functools import wraps

# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = os.urandom(24) 

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

def connect_db():
   return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
   @wraps(test)
   def wrap(*args, **kwargs):
      if 'logged_in' in session:
         return test(*args, **kwargs)
      else:
          flash('You need to login first.')
          return redirect(url_for('login'))
   return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
   error = None
#   print request.method
   if request.method == 'POST':
      if request.form['username'] != app.config['USERNAME'] or \
         request.form['password'] != app.config['PASSWORD']:
         error = 'Invalid Credentials. Please try again.'
      else:
         session['logged_in'] = True
         return redirect(url_for('main'))

   return render_template('login.html', error=error)

@app.route('/main')
@login_required
def main():
   g.db = connect_db()
   cur = g.db.execute('select * from posts')
   posts = [dict(title=row[0], post=row[1]) for row in cur.fecthall()]
   g.db.close()
   return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   flash('You were logged out')
   return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(host='192.168.187.159',debug=True)
