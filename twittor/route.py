#本文件為定義方法的彙整
from flask import render_template ,redirect ,url_for ,request ,abort ,current_app, flash
from flask_login import login_user , current_user ,logout_user, login_required

from twittor.forms import LoginForm ,RegisterForm ,EdiitProfileForm , TweetForm,\
     PasswdResetRequestForm, PasswdResetForm
from twittor.models.user import User, load_user 
from twittor.models.tweet import Tweet  
#從twittor.models.py匯入class類別:User Tweet 已拆開成資料夾分別引入
#載入 render_template讀樣板頁  跳轉網頁路徑redirect  url_for
#從twittor.forms.py匯入class類別:LoginForm RegisterForm ,EdiitProfileForm

from twittor.email import send_email
from twittor import db
#給register使用 存新用戶

@login_required #為index加上login_required裝飾器 讓尚未登入的用戶無法觀看 再配合__init__裡的login_manager.login_view = 'login'
def index():
    form=TweetForm()
    if form.validate_on_submit():
        #如果是用post到首頁
        t = Tweet(body=form.tweet.data, author=current_user) #Tweet表單
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    title="Twittor首頁"
    page_num = int(request.args.get('page') or 1)  #接收網址get的?page=頁數 默認在第一頁_

    # name={'username': current_user.username} 已改直接寫到模板裡了

    #posts=[
    #    {
    #        'author':{'username':'Root'},'body':"Hi! I'm Root!"
    #    },{
    #        'author':{'username':'Tester'},'body':"Hollo! I'm Tester."
    #    },{
    #        'author':{'username':'Tester2'},'body':"Hi! I'm Tester2."
    #    }
    #]
    tweets = current_user.own_and_followed_tweets().paginate(
        page=page_num, per_page=current_app.config['TWEET_PER_PAGE'], error_out=False)
    #分頁語法paginate(開始頁=page_num,每頁幾則=5,沒內容時顯示404=Flase)
    next_url=url_for('index',page=tweets.next_num) if tweets.has_next else None
    prev_url=url_for('index',page=tweets.prev_num) if tweets.has_prev else None
    #如果有下一頁才有參數否則為None
    return render_template('index.html', tweets=tweets.items, title=title ,form=form, next_url=next_url , prev_url=prev_url )
    #因為現在的路徑是在twittor下面 所以templates資料夾也要在目錄下面才能用
    #傳遞參數

#Login頁面
def login():
    if current_user.is_authenticated: #如果用戶已經被認證過了
        return redirect(url_for('index'))  #直接回首頁不需要進行後面的驗證程序
    title="登入頁面"
    form=LoginForm() #原本是csrf_enabled=False寫了才不會暴 後期改寫到forms.py內
    if form.validate_on_submit(): #如果form是透過submit點進來的
        #msg="username={},password={},remember_me={}".format(
        #    form.username.data,
        #    form.password.data,
        #    form.remember_me.data
        #    ) #把三個參數直接寫在字串裡面的寫法
        #print(msg)
        u=User.query.filter_by(username=form.username.data).first() 
        #根據suername字串去filter_by出來只有有或沒有  first()第一個結果
        if u is None or not u.check_password(form.password.data) : 
            #如果 沒有這個用戶或 密碼不符合返回 login畫面
            print('invalid username or password')
            return redirect(url_for('login')) 
        #否則就進入index 通過驗證的u ,根據用戶勾選是否記憶
        login_user(u,remember=form.remember_me.data)
        next_page = request.args.get('next')
        # request方法 獲取登入前的頁面帶的next參數
        if next_page: #如果有帶參數 代表從別的頁面跳入登陸頁 
            return redirect(next_page) #登入後返回原頁
        #return redirect('/') #路徑回根目錄
        return redirect(url_for('index'))  
        #改用url_for(函式名)的方式連結 萬一__init__.py改路徑才不用一個一個改
    return render_template('login.html', title=title, form=form)
    #需要用到flask_wtf套件包 pip install flask_wtf
    #安裝完套件請記得pip freeze 拷貝更新requirement.txt資源表

def logout(): #登出的方法
    logout_user()
    return redirect(url_for('login'))

def register(): #註冊的方法
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form= RegisterForm() #從forms.py內的RegisterForm()導入數據
    if form.validate_on_submit(): #驗證成功送出時將新使用者導入資料庫的步驟
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login')) #註冊成功跳回登錄頁面
    #如果有問題會保持在註冊頁面
    return render_template('register.html', title='Registration',form=form)

@login_required #只有已經登入的用戶才能查看其他用戶的頁面
def user(username): 
    u=User.query.filter_by(username=username).first()
    #但如果用戶不存在會發生錯誤 所以要返回404 Not Found 透過flask提供的abort(404)方法
    if u is None:
        abort(404)

    #posts=[
    #    {
    #        'author':{'username': u.username},'body':"Hi! I'm {}!".format(u.username)
    #    },{
    #        'author':{'username': u.username},'body':"Hollo! I'm {}.".format(u.username)
    #    }
    #] 原假資料
    #tweets=Tweet.query.filter_by(author=u)
    page_num = int(request.args.get('page') or 1)  #接收網址get的?page=頁數 默認在第一頁
    tweets=u.tweets.order_by(Tweet.create_time.desc()).paginate(
        page=page_num, per_page=current_app.config['TWEET_PER_PAGE'], error_out=False)
    #分頁語法paginate(開始頁=page_num,每頁幾則=5,沒內容時顯示404=Flase)
    next_url=url_for('profile',page=tweets.next_num ,username=username) if tweets.has_next else None
    prev_url=url_for('profile',page=tweets.prev_num ,username=username) if tweets.has_prev else None
    #如果有下一頁才有參數否則為None #更簡單的方法+ 照時間降幕排序

    if request.method == 'POST':
        #如果是PSOT 判斷用戶是點擊追蹤或是取消追蹤
        #print(request.form.to_dict()) #會打印tequest_button 的值 字典形式
        if request.form['request_button']=='Follow':
            current_user.follow(u) #追蹤當前用戶
            db.session.commit()
        elif request.form['request_button']=='Unfollow':
            current_user.unfollow(u) #取消追蹤當前用戶
            db.session.commit()
        else:
            flash("已寄送驗證信,請檢查信箱!") #都不是以上兩種狀況代表是點了 激活
            send_email_for_user_activate(current_user)
    return render_template('user.html',title='Profile',tweets=tweets.items ,user=u ,next_url=next_url, prev_url=prev_url)
    #posts=posts改成tweets=tweets用來接收filter_by(author=u)的資料

def send_email_for_user_activate(user):
    token = user.get_jwt() #重設的編碼
    url_user_activate = url_for(
                'user_activate',
                token=token,
                _external=True #完整的連結
    )
    send_email(
        subject=current_app.config['MAIL_SUBJECT_USER_ACTIVATE'],
        recipients=[user.email],
        text_body=render_template(
            'email/user_activate.txt',
            username=user.username,
            url_user_activate=url_user_activate
        ),
        html_body=render_template(
            'email/user_activate.html',
            username=user.username,
            url_user_activate=url_user_activate
        )
    )        

def user_activate(token):
    if current_user.is_authenticated: #如果當前用戶已經登入
        #return redirect(url_for('index'))
        if current_user.is_activated: #而且當前用戶已經激活
            msg= "已驗證通過,不需重複驗證"
            return render_template('user_activate.html',msg=msg)
    user = User.verify_jwt(token)
    if not user: #不是用戶(錯誤或過期) 引導註冊
        msg= "驗證碼已過期 請重新驗證"
    else: #驗證碼有效的處理模式
        user.is_activated = True
        db.session.commit()
        msg="成功驗證使用者信箱"
    return render_template('user_activate.html',msg=msg)

def page_not_found(e): #找不到頁面時 e參數避免報錯
    return render_template('404.html'), 404

@login_required #限制是已經登入的用戶
def edit_profile(): #編輯個人資料
    form = EdiitProfileForm()
    if request.method == 'GET':
        form.about_me.data  = current_user.about_me #填入當前用戶原始的about_me
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('profile',username=current_user.username)) #特別要注意 需要帶參數 才會回到當前用戶的頁面
    return render_template('edit_profile.html',form=form)


def reset_password_request():
    if current_user.is_authenticated: #如果當前用戶已經登入不需要重置密碼
        return redirect(url_for('index'))
    form = PasswdResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("You should soon receive an email allowing you to reset your password.\
                 find te email") #以上為運用flash頁面顯示訊息
            token = user.get_jwt() #重設的編碼
            url_password_reset = url_for(
                'password_reset',
                token=token,
                _external=True #完整的連結
            )
            url_password_reset_request = url_for(
                'reset_password_request',
                _external=True
            )
            # url='http://127.0.0.1:5000/password_reset/{}'.format(token) #組合成重設網址
            send_email(
                subject=current_app.config['MAIL_SUBJECT_RESET_PASSWORD'],
                #sender='noreply@twittor.com',
                recipients=[user.email],
                text_body=render_template(
                    'email/passwd_reset.txt',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request),
                html_body=render_template(
                    'email/passwd_reset.html',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                )
            )
        else:
            raise
        return redirect(url_for('login'))
    return render_template('password_reset_request.html',form=form)

def password_reset(token):
    if current_user.is_authenticated: #如果當前用戶已經登入不需要重置密碼
        return redirect(url_for('index'))
    user = User.verify_jwt(token)
    if not user: #不是用戶(錯誤或過期) 引導註冊
        return redirect(url_for('login'))
    form = PasswdResetForm() #經過兩關 代表有效用戶 顯示表單
    if form.validate_on_submit(): #如果重設密碼表單已經送出
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('password_reset.html', title="Password Reset", form=form)

@login_required
def explore():
    #所有使用者的貼文
    page_num = int(request.args.get('page') or 1)  #接收網址get的?page=頁數 默認在第一頁
    tweets=Tweet.query.order_by(Tweet.create_time.desc()).paginate(
        page=page_num, per_page=current_app.config['TWEET_PER_PAGE'], error_out=False)
    #分頁語法paginate(開始頁=page_num,每頁幾則=5,沒內容時顯示404=Flase)
    next_url=url_for('explore',page=tweets.next_num) if tweets.has_next else None
    prev_url=url_for('explore',page=tweets.prev_num) if tweets.has_prev else None
    return render_template('explore.html',title='Explore',tweets=tweets.items ,next_url=next_url, prev_url=prev_url)
    