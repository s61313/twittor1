from flask_script import Manager
from flask_migrate import MigrateCommand
from twittor import create_app
#重新架構的程式
#呼叫已組件程式於teittor
#實際網頁的內容變數寫在route.py裡面
#使用flask_script
#from flask_migrate import MigrateCommand 匯入命令部分如下
#init        1.初始化 python manager.py db init 會創造migrations資料夾與文件
#revision    Create a new revision file.
#migrate     2.python manager.py db migrate -m "create user" 創造類似GET訊息
#edit        Edit current revision.
#merge       Merge two revisions together. Creates a new migration file
#current     查詢當前的migrate版本
app=create_app()
manager=Manager(app)
manager.add_command('db', MigrateCommand)
if __name__=="__main__":
    manager.run()

#啟動參數為python manager.py runserver
#後面接-d可以開啟除錯模式 修改代碼會自動更新 不用重啟

#安裝flask-sqlalchemy 支援SQL在開發過程中使用SQLite但完成用MSQL 
#安裝 Flask-Migrate 方便對開發過程中對數據庫的擴展新增