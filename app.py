from flask import Flask
from flask import render_template
#pip freeze >>requirement.txt可以創建環境檔
#git init 創造一個空的git
#git checkout -b 0.2  建立分支
#此為舊版 正式文件用manager.py取代了此文件
app= Flask(__name__)

@app.route('/')
def hello():
     name={'user':'Root'}
     return render_template('index.html',name=name)
     

@app.route('/test-for')
def testfor():
    #name="Aman"
    #return render_template('index.html',name=name)
    #從預設值的templates資料夾內讀取index.html 裡的name變數用name:Aman取代
    name={'user':'Root'}
    rows=[
        {'fname':'Chao','lname':'Chung-Yen',"age":27},
        {'fname':'Li','lname':'Buy',"age":70},
        {'fname':'Wang','lname':'Perryn',"age":35},
        {'fname':'Li','lname':'Mouse',"age":50},
        {'fname':'Wang','lname':'Da-Chung',"age":85}
    ]
    #給html跑的for迴圈
    return render_template('index1.html',name=name,rows=rows)
    #從預設值的templates資料夾內讀取index.html 裡的name變數用字典user:Root取代

if __name__=="__main__":
    app.run()