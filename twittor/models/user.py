from datetime import datetime
from flask_login import UserMixin
from hashlib import md5 #Email轉hash值用來生成頭像網址
import time

from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app
import jwt

from twittor import db ,login_manager
from twittor.models.tweet import Tweet

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
#followers Table數據只描述關係連結表 ForeignKey外鍵

class User(UserMixin,db.Model): #讓User繼承UserMixin的方法
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True) # unique=True全域唯一
    email = db.Column(db.String(64), unique=True, index=True) 
    #unique=True全域唯一  有加index搜索會比較快
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    tax= db.Column(db.String(32))
    about_me = db.Column(db.String(256))
    create_time= db.Column(db.DateTime, default=datetime.utcnow)
    is_activated = db.Column(db.Boolean , default=False)

    tweets = db.relationship("Tweet",backref="author",lazy="dynamic") 
    #不在資料表裡面而是連Tweet資料表 用來計算用戶發了多少文 1對多

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    

    def __repr__(self):
        return 'id={},username={}, email={}, password_hash={}'.format(
            self.id, self.username, self.email, self.password_hash
        )
    #設定回傳的資料
    #測試 再命令列打from twittor.models import User
    #user = User(username='admin',email='s61313@gmail.com',password_hash='12345')
    #id用Nane 以後自動生成 每次自動加1
    #user 可以測試剛生成的

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 
        #生成密碼的hash值

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
        #比較檢查資料庫裡的密碼和用戶輸入的密碼 正確符合回傳True

    def avatar(self, size=80):
        md5_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(md5_digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user) #追蹤用戶
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user) #取消追蹤用戶

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
        #對過濾後的結果再過濾 如果是1的話代表已經follow

    def own_and_followed_tweets(self):
        followed = Tweet.query.join( #從數據庫中所有的文
            followers,(followers.c.followed_id == Tweet.user_id)).filter(followers.c.follower_id == self.id) #篩選出關注的人的推文
        own = Tweet.query.filter_by(user_id=self.id) #本人發的推文
        return followed.union(own).order_by(Tweet.create_time.desc())
        #把篩選出關注的貼文和本人的發文union結合 排列order_by依據發文時間 desc降序(最新的在最前)
    
    def get_jwt(self, expire=7200):  #編碼給用戶的密碼重設
        return jwt.encode(
            {'email': self.email,'exp': time.time() + expire}, #exp用於超時
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8') #修正格式

    @staticmethod  #做成靜態方法 因為此時還不知道是哪個用戶
    def verify_jwt(token):
        try:
            email= jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            email=email['email']
        except:
            return
        return User.query.filter_by(email=email).first()


@login_manager.user_loader #login的方法
def load_user(id):
    return User.query.get(int(id)) #把id字串轉成數值
