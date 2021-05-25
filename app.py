"""Blogly application."""

from flask import Flask,render_template,request,redirect,session
from models import db, connect_db,User,Post,Tag,PostTag

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route('/')
def get_users():
    users = User.query.all()
    tags = Tag.query.all()
    return render_template('home.html',users=users,tags=tags)
    
@app.route('/adduser')
def add_user():
    return render_template('adduser.html')

@app.route('/user',methods = ["POST"])
def submit_user():
    first_name = request.form["fnametxt"]
    last_name = request.form["lnametxt"]
    url = request.form["urltxt"]

    user = User(first_name = first_name,last_name = last_name,img_url= url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/user/{user.id}")

@app.route('/user/<int:user_id>')
def details(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    session["firstname"]=user.first_name 
    session["lastname"]=user.last_name
    session["userid"]=user.id
    session["img_url"] = user.img_url
    
    return render_template('details.html',posts=posts)

@app.route('/user/edit')
def edit_user():
    return render_template('edituser.html')

@app.route('/edituser',methods=["POST"])
def edit_user_btn():
    edituser = User.query.get(session['userid'])
    edituser.first_name = request.form["fname"]
    edituser.last_name = request.form["lname"]
    edituser.img_url = request.form["url"]
    db.session.add(edituser)
    db.session.commit()
    return redirect(f'/user/{edituser.id}')


@app.route('/user/delete')
def delete_user():
    User.query.filter_by(id = session['userid']).delete()
    db.session.commit()
    return redirect('/')

# START FOR POST

@app.route('/post/<int:post_id>')
def post_details(post_id):
    post = Post.query.get(post_id)

    return render_template('post_details.html',post=post)

@app.route('/post/add/<int:user_id>')
def post_add(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    
    return render_template('post_add.html',user = user,tags=tags)

@app.route('/post/submit/<int:user_id>',methods=["POST","GET"])
def post_submit(user_id):
    title = request.form["title"]
    content = request.form["content"]
    newPost = Post(title=title,content= content,user_id=user_id)
    db.session.add(newPost)
    db.session.commit()
    tags = request.form.getlist('taglist')
    for t in tags:
        pt = PostTag(post_id = newPost.id,tag_id=t)
        db.session.add(pt)
        db.session.commit()
    return redirect(f"/user/{user_id}")

@app.route('/post/edit/<int:post_id>')
def post_edit(post_id):
    post = Post.query.get(post_id)
    TagInPost = post.tags
    tags = Tag.query.all()
    return render_template('post_edit.html',post = post,tags = tags,taginpost = TagInPost)

@app.route('/editpost/<int:post_id>',methods = ["POST"])
def post_edit_submit(post_id):
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    posttag = post.tags
    for tag in posttag:
        PostTag.query.filter(PostTag.post_id == post_id,PostTag.tag_id == tag.id).delete()
        db.session.commit()
    
    tags = request.form.getlist('taglist')
    for t in tags:
        pt = PostTag(post_id = post.id,tag_id=t)
        db.session.add(pt)
        db.session.commit()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/post_tag_details/{post_id}")



@app.route('/post/delete/<int:post_id>')
def post_delete(post_id):
    Post.query.filter_by(id = post_id).delete()
    db.session.commit()
    posts = Post.query.filter(Post.user_id == session["userid"]).all()
    return render_template('details.html',posts=posts)
    

@app.route('/post/cancel/<int:post_id>')
def post_cancel(post_id):
    posts = Post.query.filter(Post.user_id == session["userid"]).all()
    return render_template('details.html',posts=posts)

# START FOR TAG

@app.route('/addtag')
def addtag():
    return render_template('create_tag.html')

@app.route('/createtag',methods=["POST"])
def createtag():
    tag = request.form["txt-tag"]
    t = Tag(name=tag)
    db.session.add(t)
    db.session.commit()
    return redirect('/')


@app.route('/showposttag/<int:tagid>')
def showposttag(tagid):
    posttag = Tag.query.get(tagid)
    posts = posttag.posts
    return render_template('view_post_tag.html',posttag = posttag,tagid = tagid,posts=posts)

@app.route('/tag/edit/<int:tagid>')
def editTag(tagid):
    tag = Tag.query.get(tagid)
    return render_template('edit_tag.html',tag=tag)

@app.route('/edittag/<int:tagid>', methods=["POST"])
def editSubmitTag(tagid):
    tag = Tag.query.get(tagid)
    tag.name = request.form['txt-tag']
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/showposttag/{tagid}')




@app.route('/tag/delete/<int:tagid>')
def deleteTag(tagid):
    Tag.query.filter_by(id=tagid).delete()
    return redirect('/')

@app.route('/post_tag_details/<int:pid>')
def postTagDetails(pid):
    post = Post.query.get(pid)
    user = User.query.get(post.user_id)
    tags = post.tags
    return render_template('post_tag_details.html',
                                post = post,
                                user = user,
                                tags = tags)

