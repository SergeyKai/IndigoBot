from flask import Flask, render_template

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


admin = Admin(app, name='Панель Администратора', template_mode='bootstrap4')

admin.add_view(ModelView())

if __name__ == '__main__':
    app.run()
