import os
config_path = os.path.abspath(os.path.dirname(__file__))
#獲取當前文件的絕對路徑 

#集中化管理所有設定值
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","sqlite:///" + os.path.join(config_path, 'twittor.db'))
    #設置一個環境變數方便未來隨時更改DATABASE的URL
    #當有設置DATABASE_URL='其他路徑' 就會改走其他路徑
    # SQLALCHEMY_DATABASE_URI = "sqlite:///twittor.db" 原相對路徑寫法
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #以上兩段原本寫於__init__裡的create app
    
    SECRET_KEY = 'abc123'

    TWEET_PER_PAGE = 3
    #一頁顯示幾則

    MAIL_DEFAULT_SENDER = 'noreoly@twittor.com'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'photour.tw'
    MAIL_PASSWORD = 'aMan1338'
    MAIL_SUBJECT_RESET_PASSWORD = '[Twittor] Please Reset Your Password'
    MAIL_SUBJECT_USER_ACTIVATE = '[Twittor] Please Activate Your Accout'