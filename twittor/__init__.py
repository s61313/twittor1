from flask import Flask
from flask_sqlalchemy import SQLAlchemy #引入SQLalchemy
from flask_migrate import Migrate
from flask_login import LoginManager #flask_login用來記憶用戶登入狀況
from flask_mail import Mail

from twittor.config import Config #從twittor.config引入方法Config

db=SQLAlchemy() 
migrate=Migrate()
login_manager= LoginManager()
login_manager.login_view = 'login' #未login的使用者會自動進入login頁面(會記得跳轉前頁面)
mail=Mail()

from twittor.route import index, login ,logout ,register ,user ,\
    page_not_found , edit_profile, reset_password_request, password_reset,\
    explore, user_activate
#已經初始化ab才能讀入route.py的index(),login()...不然會出錯
#因為route會引入models 而models又會引入db
def create_app():
    app=Flask(__name__)
    app.config.from_object(Config) 
    #下面那段已經改寫入config.py裡=========
    #app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql+pymysql://u462349867_pytho:pythontest01@sql26.main-hosting.eu/u462349867_pytho"
    #透過pymysql連結遠端的資料庫
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///twittor.db" 
    #將SQLAlchemy的資料庫路徑設為文件twittor.db
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #修正這個變量避免錯誤
    #====================================
    db.init_app(app) #初始化SQLAlchemy
    migrate.init_app(app, db) #初始化Migrate
    login_manager.init_app(app)#初始化login關聯
    mail.init_app(app) #初始化mail服務

    app.add_url_rule('/index', 'index',methods=['GET','POST']) #相當於裝飾器 @app.rout('/') 路徑,名字,方法
    app.add_url_rule('/', 'index', index ,methods=['GET','POST']) #增加根目錄沒輸入index時的相容
    app.add_url_rule('/login' ,'login', login, methods=['GET','POST']) 
    #用url_for的方式做連結 只要名稱不改 路徑修改不會斷練
    #註冊login頁面 
    # methods=['GET','POST'] 預設只有GET增加對POST方法的支援
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register ,methods=['GET','POST'])
    app.add_url_rule('/<username>', 'profile', user, methods=['GET','POST'])
    #<小括號> 可以帶入變數 ,名稱,方法
    app.add_url_rule('/edit_profile', 'edit_profile', edit_profile ,methods=['GET','POST'])
    app.add_url_rule(
        '/reset_password_request','reset_password_request',
        reset_password_request,methods=['GET','POST']
    )
    app.add_url_rule( 
        '/password_reset/<token>',
        'password_reset',
        password_reset,
        methods=['GET','POST']
    )
    app.add_url_rule('/explore', 'explore', explore)
    app.add_url_rule('/activate/<token>', 'user_activate', user_activate)
    app.register_error_handler(404, page_not_found)
    #錯誤代碼
    return app



