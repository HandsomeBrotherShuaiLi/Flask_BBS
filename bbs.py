from flask import Flask
from flask import render_template
from flask import request,jsonify
from model import user
from flask import redirect,url_for
import datetime
import os
from werkzeug.utils import secure_filename
from video import detection
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.contrib.pymongo.filters import BooleanEqualFilter
from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList
app=Flask(__name__)
app.config['SECRET_KEY'] = '123456790'

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template("index.html")
@app.route('/articles',methods=['GET','POST'])
def article():
    return render_template("articles-list.html")
@app.route('/faq',methods=['GET','POST'])
def faq():
    return render_template("faq.html")
@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template("contact.html")
@app.route('/post',methods=['GET','POST'])
def post():
    if request.method=="POST":
        topic=request.form['topic']
        title=request.form['title']
        post=request.form['post']
        user.updata({"name": globalname, "password": globalpsw},
                    {"$set": {'post':{'topic':topic,"title":title,'post':post}}})
        return redirect(url_for("article"))

    return render_template("post.html")

@app.route('/cnn',methods=['GET','POST'])
def cnn():
    if request.method=='POST':
        f=request.files['upfile']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static\\uploads', secure_filename(f.filename))
        f.save(upload_path)


        res="static\\uploads\\"+f.filename
        res2="static\\handle\\"+f.filename
        _=detection(res,res2)

        user.updata({"name": globalname, "password": globalpsw},
                    {"$set": {'media': {'origin':res,'processed':res2}}})

        return render_template('cnn.html', path1=res,path2=res2)

    return render_template('cnn.html')


@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        loginusername=request.form["loginusername"]
        loginpassword=request.form["loginpassword"]
        print(loginusername, loginpassword)
        res=user.find({'name':loginusername,'password':loginpassword})
        u=list(res)
        if len(u)==0:
            return redirect(url_for("register"))
        elif len(u)==1:
            if u[0]['isadmin']==1:
                globalname=loginusername
                globalpsw=loginpassword
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                count=u[0]['count']+1
                user.updata({"name": loginusername, "password": loginpassword}, {"$set": {"lasttime": nowTime, "count": count}})
                return redirect(url_for("admin.index"))
            else:
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                count = u[0]['count'] + 1
                user.updata({"name": loginusername, "password": loginpassword},
                            {"$set": {"lasttime": nowTime, "count": count}})
                return redirect(url_for("index"))
    return render_template("login.html")
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        regusername = request.form["regusername"]
        email = request.form['email']
        regpassword = request.form["regpassword"]
        re_regpassword = request.form["re_regpassword"]

        if regpassword!=re_regpassword:
            return render_template('register.html')
        else:
            globalname=regusername
            globalpsw=regpassword
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            count = 1
            post={}
            media={}
            user.insert({"name": regusername, "password": regpassword, "lasttime": nowTime,
                         "count": count, "isadmin": 0,"post":post,'media':media})
    return render_template("register.html")




if __name__=="__main__":
    globalname = str()
    globalpsw = str()
    app.run(debug=True)