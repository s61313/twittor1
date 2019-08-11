from datetime import datetime
from twittor import db

class Tweet(db.Model):
    #從db.Model繼承
    id = db.Column(db.Integer, primary_key=True)
    #貼文的ID
    body= db.Column(db.String(140))
    #文字本體 長度限制140
    create_time= db.Column(db.DateTime, default=datetime.utcnow)
    #貼文的時間
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    #限制貼文者一定在db 使用者表裡的user.id  ForeignKey關聯

    def __repr__(self):
        return "id={},body={},create_time={},user_id={}".format(
            self.id, self.body, self.create_time, self.user_id
        )


 