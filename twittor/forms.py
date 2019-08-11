from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField ,TextAreaField
#呼叫flask wtf
#定義欄位的屬性:使用者名稱-文字欄位,密碼欄位,記住我(布林值),送出按鈕 ,文字框
from wtforms.validators import DataRequired ,Email ,EqualTo ,ValidationError ,Length
#呼叫資料檢查 .Email檢查 .EqualTo重複輸入密碼檢查 ,使用者名重複時的異常訊息 ,長度檢查
from twittor.models.user import User
#為了在新用戶註冊時能檢查是否重複用戶名 所以引入

class LoginForm(FlaskForm): #用戶登錄的表單
    class Meta:
        csrf=False #修正FlaskWTF警告訊息
    username= StringField("Username", validators=[DataRequired()]) #必備資料檢查
    password= PasswordField("Password", validators=[DataRequired()])
    remember_me= BooleanField("Remember")
    submit= SubmitField("Sign In")

class RegisterForm(FlaskForm): #新用戶註冊的表單
    username= StringField("Username", validators=[DataRequired()]) #必填資料檢查
    email= StringField("Email Address", validators=[DataRequired(),Email()]) #必填 Email資料檢查
    password= PasswordField("Password", validators=[DataRequired()])
    password2= PasswordField("Repeat Password", validators=[DataRequired(),EqualTo('password')])
    #和第一次輸入的password密碼比對檢查
    submit= SubmitField("Register")

    def validate_username(self,username): #wtforms.validators提供檢查用戶名是否重復的方法
        user = User.query.filter_by(username=username.data).first()
        #取第一個參數 檢查 如果不是None代表重複了
        if user is not None:
            raise ValidationError("請更換不同的使用者名")

    def validate_email(self,email): #wtforms.validators提供檢查用戶Email是否重復的方法
        user = User.query.filter_by(email=email.data).first()
        #取第一個參數 檢查 如果不是None代表重複了
        if user is not None:
            raise ValidationError("請更換不同的Email")

class EdiitProfileForm(FlaskForm): #編輯自我介紹
    about_me = TextAreaField('About me',validators=[Length(min=0, max=256)])
    submit = SubmitField('Save')

class TweetForm(FlaskForm):
    tweet = TextAreaField('tweet',validators=[DataRequired(),Length(min=1, max=140)])
    submit = SubmitField('Tweet')

class PasswdResetRequestForm(FlaskForm): #忘記密碼要求重設
    email = StringField('Email Address',validators=[DataRequired(),Email()])
    submit = SubmitField('Reset Password')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('沒有這個email註冊的帳號')

class PasswdResetForm(FlaskForm): #重設密碼
    password= PasswordField("Password", validators=[DataRequired()])
    password2= PasswordField("Repeat Password", validators=[DataRequired(),EqualTo('password')])
    #和第一次輸入的password密碼比對檢查
    submit = SubmitField('Submit')