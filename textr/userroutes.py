import os,random,string,requests

from io import BytesIO

from flask import render_template,request,session,flash,redirect,url_for,send_file,jsonify

import json

import base64

import sqlite3

import imghdr

from sqlalchemy.sql import text,desc,asc

from sqlalchemy import or_,not_

from werkzeug.security import generate_password_hash,check_password_hash

from PIL import Image

from datetime import datetime

from textr import app,db

from textr.models import User,State,Country,CoverPhoto,ProfilePicture,Post,Like,Friends,FriendRequest,GroupMembers,Comment,Message

from jinja2 import Environment
env = Environment()
env.globals.update(len=len)


def length(value):
    return len(value)

env = Environment()
env.filters['length'] = length





def generate_name():
    filename = random.sample(string.ascii_lowercase,10)
    return ''.join(filename)




@app.route('/home')
def home():
    if session.get('user') != None:
        id = session['user']
        current_time = datetime.utcnow()
        post = Post.query.order_by(desc(Post.post_created_at)).all()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        compic = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        friends = Friends.query.filter(or_(Friends.friends_targetid==id,Friends.friends_sourceid==id)).all()
        groupmembers = GroupMembers.query.filter(GroupMembers.group_members_userid==id).all()
        like = {}
        pics = {}
        comment = {}
        for p in post:
            like[p.post_id] = Like.query.filter_by(like_user_id=id, like_post_id=p.post_id).first()
            pics[p.post_userid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==p.post_userid).first()
            comment[p.post_id] = Comment.query.order_by(desc(Comment.comment_id)).filter(Comment.comment_postid==p.post_id).first()
        return render_template('user/index.html', post=post, like=like,profile=profile,pics=pics,friends=friends,groupmembers=groupmembers,comment=comment,compic=compic,current_time=current_time,id=id)
    else:
        return redirect(url_for('login_form'))




@app.route('/like/<like_post_id>')
def like_post(like_post_id):
    if session.get('user') is None:
        return redirect(url_for('form'))

    id = session['user']
    like = Like.query.filter_by(like_user_id=id, like_post_id=like_post_id).first()

    if like is None:
        new_like = Like(like_user_id=id, like_post_id=like_post_id)
        db.session.add(new_like)
        db.session.commit()
            # Update the like dictionary
        posts = Post.query.order_by(desc(Post.post_created_at)).all()
        like_dict = {}
        for post in posts:
            likes = Like.query.filter_by(like_post_id=post.post_id).all()
            like_dict[post.post_id] = likes

        return redirect(url_for('home'))
    else:
        db.session.delete(like)
        db.session.commit()

        # Update the like dictionary
        posts = Post.query.order_by(desc(Post.post_created_at)).all()
        like_dict = {}
        for post in posts:
            likes = Like.query.filter_by(like_post_id=post.post_id).all()
            like_dict[post.post_id] = likes

        return redirect(url_for('home'))




@app.route('/profile/like/<like_post_id>')
def likes_post(like_post_id):
    if session.get('user') is None:
        return redirect(url_for('form'))

    id = session['user']
    like = Like.query.filter_by(like_user_id=id, like_post_id=like_post_id).first()

    if like is None:
        new_like = Like(like_user_id=id, like_post_id=like_post_id)
        db.session.add(new_like)
        db.session.commit()
        # Update the like dictionary
        posts = Post.query.order_by(desc(Post.post_created_at)).all()
        like_dict = {}
        for post in posts:
            likes = Like.query.filter_by(like_post_id=post.post_id).all()
            like_dict[post.post_id] = likes

        return redirect(url_for('profile'))
    else:
        db.session.delete(like)
        db.session.commit()

        # Update the like dictionary
        posts = Post.query.order_by(desc(Post.post_created_at)).all()
        like_dict = {}
        for post in posts:
            likes = Like.query.filter_by(like_post_id=post.post_id).all()
            like_dict[post.post_id] = likes

        return redirect(url_for('profile'))
    




@app.route('/textr/post/all_comments/<id>')
def comment(id):
    if session.get('user') != None:
        ids = session['user']
        current_time = datetime.utcnow()
        post = Post.query.order_by(desc(Post.post_created_at)).filter(Post.post_id==id).all()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        compic = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        friends = Friends.query.all()
        like = {}
        pics = {}
        comment = {}
        for p in post:
            like[p.post_id] = Like.query.filter_by(like_user_id=ids, like_post_id=p.post_id).first()
            pics[p.post_userid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==p.post_userid).first()
            comment[p.post_id] = Comment.query.order_by(desc(Comment.comment_id)).filter(Comment.comment_postid==p.post_id).all()
        return render_template('user/comment.html', post=post, like=like,profile=profile,pics=pics,friends=friends,comment=comment,compic=compic,current_time=current_time,ids=ids)
    else:
        return redirect(url_for('login_form'))

    




@app.route('/textr/profile_post/all_comments/<id>')
def comment_profile(id):
    if session.get('user') != None:
        ids = session['user']
        current_time = datetime.utcnow()
        post = Post.query.order_by(desc(Post.post_created_at)).filter(Post.post_id==id).all()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        compic = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        friends = Friends.query.all()
        like = {}
        pics = {}
        comment = {}
        for p in post:
            like[p.post_id] = Like.query.filter_by(like_user_id=ids, like_post_id=p.post_id).first()
            pics[p.post_userid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==p.post_userid).first()
            comment[p.post_id] = Comment.query.order_by(desc(Comment.comment_id)).filter(Comment.comment_postid==p.post_id).all()
        return render_template('user/comment_profile.html', post=post, like=like,profile=profile,pics=pics,friends=friends,comment=comment,compic=compic,current_time=current_time,ids=ids)
    else:
        return redirect(url_for('login_form'))




@app.route('/textr/post/comments/<id>',methods=['GET','POST'])
def comment_post(id):
    if session.get('user') != None:
        if request.method == 'GET':
            return redirect(url_for('home'))
        else:
            ids = session.get('user')
            comment = request.form.get('comment')
            if comment == '':
                flash('Comment Box cannot be empty')
                return redirect(url_for('home'))
            else:
                comment = Comment(comment=comment,comment_userid=ids,comment_postid=id)
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('home'))
    else:
        return redirect(url_for('login_form'))




@app.route('/textr/post/comment_profile/<id>',methods=['GET','POST'])
def comment_post_profile(id):
    if session.get('user') != None:
        if request.method == 'GET':
            return redirect(url_for('home'))
        else:
            ids = session.get('user')
            comment = request.form.get('comment')
            if comment == '':
                flash('Comment box cannot be empty')
                return redirect(url_for('profile'))
            else:
                comment = Comment(comment=comment,comment_userid=ids,comment_postid=id)
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('profile'))
    else:
        return redirect(url_for('login_form'))





@app.route('/textr/messages')
def message():
    if session.get('user') != None:
        id = session.get('user')
        friends = Friends.query.filter(or_(Friends.friends_sourceid==id,Friends.friends_targetid==id)).all()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        picsrc = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        return render_template('user/message.html',friends=friends,profile=profile,picsrc=picsrc)
    else:
        return redirect(url_for('form'))
    




@app.route('/textr/chats/<id>')
def chats(id):
    if session.get('user') != None:
        ids = session.get('user')
        user = User.query.get(ids)
        friends = Friends.query.filter(or_(Friends.friends_sourceid==ids,Friends.friends_targetid==ids)).all()
        friend = Friends.query.filter(((Friends.friends_sourceid==ids)&(Friends.friends_targetid==id))|((Friends.friends_sourceid==id)&(Friends.friends_targetid==ids))).first()
        message = Message.query.filter(((Message.message_sourceid==ids)&(Message.message_targetid==id))|((Message.message_sourceid==id)&(Message.message_targetid==ids))).all()
        one_message = Message.query.order_by(desc(Message.message_id)).filter(or_(Message.message_targetid==ids,Message.message_sourceid==ids)).first()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        picsrc = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        return render_template('user/chats.html',friends=friends,message=message,profile=profile,picsrc=picsrc,friend=friend,one_message=one_message,user=user,ids=ids)
    else:
        return redirect(url_for('form'))




@app.route('/send/message/<id>',methods=['GET','POST'])
def send_message(id):
    if request.method == 'GET':
        return redirect(url_for('message'))
    else:
        if session.get('user') != None:
            ids = session.get('user')
            chat = request.form.get('chat')
            if chat != '':
                m=Message(message=chat,message_updated_at=datetime.now(),message_sourceid=ids,message_targetid=id)
                db.session.add(m)
                db.session.commit()
                return redirect(url_for('chats',id=id))
            else:
                return redirect(url_for('chats',id=id))
        else:
            return redirect(url_for('form'))




@app.route('/')
def form():
    country = Country.query.all()
    state = State.query.all()
    return render_template('user/form.html',country=country,state=state)




@app.route('/state/<country>')
def loadstate(country):
    state = db.session.query(State).filter(State.state_countryid==country).all()
    data = '<select name="state" class="form-select form-select-md mb-1 border-dark">'
    for s in state:
        data =data+"<option>"+ s.state +"</option>"
    data = data+ "</select>"
    return data



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='GET':
        return redirect(url_for('form'))
    else:
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        uname = request.form.get('uname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        state = request.form.get('state')
        pwd = request.form.get('pwd')
        cpwd = request.form.get('cpwd')
        hashed_pwd=generate_password_hash(pwd)
        if fname == '' or lname == '' or uname == '' or email == '' or phone == '' or pwd == '':
            flash('One or more fields are empty, please complete the form')
            return redirect(url_for('form'))
        elif pwd != cpwd:
            flash('Password and Confirm Password not match')
            return redirect(url_for('form'))
        else:
            users=db.session.query(User).filter(User.user_username==uname).first()
            emails=db.session.query(User).filter(User.user_email==email).first()
            phones=db.session.query(User).filter(User.user_phone==phone).first()
            state=db.session.query(State).filter(State.state==state).first()
            if users != None:
                flash("Username Already Exists")
                return redirect(url_for('form'))
            elif emails != None:
                flash("Email Address Already Exists, Try logging in or use a different email to try again")
                return redirect(url_for('form'))
            elif phones != None:
                flash("Phone Number Already Exists, Try logging in or use a different phone number to try again")
                return redirect(url_for('form'))
            else:
                if mname == '':
                    u = User(user_fname=fname,user_lname=lname,user_username=uname,user_pwd=hashed_pwd,user_email=email,user_phone=phone,user_gender=gender,user_stateid=state.state_id)
                    db.session.add(u)
                    db.session.commit()
                    userid=u.user_id
                    session['user']=userid
                    flash('Registration Successful')
                    return redirect(url_for('home'))
                else:
                    u = User(user_fname=fname,user_mname=mname,user_lname=lname,user_username=uname,user_pwd=hashed_pwd,user_email=email,user_phone=phone,user_gender=gender,user_stateid=state.state_id)
                    db.session.add(u)
                    db.session.commit()
                    userid=u.user_id
                    session['user']=userid
                    flash('Registration Successful')
                    return redirect(url_for('home'))


@app.route('/login')
def login_form():
    return render_template('user/login_form.html')




@app.route('/home/login/',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return redirect(url_for('form'))
    else:
        text=request.form.get('text')
        pwd=request.form.get('pwd')
        logs=db.session.query(User).filter(User.user_email==text).first()
        phonelog=db.session.query(User).filter(User.user_phone==text).first()
        if text !='' and pwd !='':
            if logs != None:
                pwd_indb= logs.user_pwd
                chk=check_password_hash(pwd_indb,pwd)
                if chk == True:
                    id= logs.user_id
                    session['user']=id
                    logs.user_lastlogin = datetime.now()
                    db.session.commit()
                    return redirect(url_for('home'))
                else:
                    flash("Invalid Credentials")
                    return redirect(url_for('login_form'))
            elif phonelog != None:
                pwd_indb= phonelog.user_pwd
                chk=check_password_hash(pwd_indb,pwd)
                if chk == True:
                    id= phonelog.user_id
                    session['user']=id
                    phonelog.user_lastlogin = datetime.now()
                    db.session.commit()
                    return redirect(url_for('home'))
                else:
                    flash("Invalid Credentials")
                    return redirect(url_for('login_form'))
            else:
                flash("Invalid Credentials")
                return redirect(url_for('login_form'))
        else:
            flash("One or more fields are empty, Please complete the form")
            return redirect(url_for('login_form'))




@app.route('/textr/friends')
def friends():
    if session.get('user') != None:
        id = session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        friends = Friends.query.filter(or_(Friends.friends_targetid==id,Friends.friends_sourceid==id)).all()
        users = User.query.filter(~User.user_id.in_(Friends.query.with_entities(Friends.friends_sourceid).filter(Friends.friends_targetid == id))).filter(~User.user_id.in_(Friends.query.with_entities(Friends.friends_targetid).filter(Friends.friends_sourceid == id))).all()
        pics = {}
        pic = {}
        sugg_friends_pic = {}
        for f in friends:
            pics[f.friends_sourceid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_sourceid).first()
            pic[f.friends_targetid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_targetid).first()
        for u in users:
            sugg_friends_pic[u.user_id] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==u.user_id).first()
        return render_template('user/friends.html',friends=friends,profile=profile,pics=pics,pic=pic,id=id,users=users,sugg_friends_pic=sugg_friends_pic)
    else:
        return redirect(url_for('login_form'))




@app.route('/textr/other_friends/<id>')
def friends_friends(id):
    if session.get('user') != None:
        ids = session.get('user')
        user = User.query.get(id)
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        friends_friends = Friends.query.filter(or_(Friends.friends_targetid==id,Friends.friends_sourceid==id)).all()
        pics = {}
        pic = {}
        friendsrc = {}
        friendtgt = {}
        for f in friends_friends:
            pics[f.friends_sourceid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_sourceid).first()
            pic[f.friends_targetid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_targetid).first()
            friendsrc[f.friends_sourceid] = Friends.query.filter(((Friends.friends_sourceid==f.friends_sourceid)&(Friends.friends_targetid==ids))).first()
            friendtgt[f.friends_targetid] = Friends.query.filter(((Friends.friends_sourceid==ids)&(Friends.friends_targetid==f.friends_targetid))).first()
        return render_template('user/friends_friends.html',friends_friends=friends_friends,profile=profile,pics=pics,pic=pic,id=id,ids=ids,user=user,friendsrc=friendsrc,friendtgt=friendtgt)
    else:
        return redirect(url_for('login_form'))



@app.route('/textr/friendrequest')
def friendreq():
    if session.get('user') != None:
        id = session['user']
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        friendrequest = FriendRequest.query.order_by(desc(FriendRequest.friend_request_id)).filter(FriendRequest.friend_request_targetid==id).all()
        users = User.query.filter(~User.user_id.in_(Friends.query.with_entities(Friends.friends_sourceid).filter(Friends.friends_targetid == id))).filter(~User.user_id.in_(Friends.query.with_entities(Friends.friends_targetid).filter(Friends.friends_sourceid == id))).filter(~User.user_id.in_(FriendRequest.query.with_entities(FriendRequest.friend_request_sourceid).filter(FriendRequest.friend_request_targetid == id))).filter(~User.user_id.in_(FriendRequest.query.with_entities(FriendRequest.friend_request_targetid).filter(FriendRequest.friend_request_sourceid == id))).all()
        pics = {}
        pic = {}
        for f in friendrequest:
            pics[f.friend_request_sourceid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friend_request_sourceid).first()
        for u in users:
            pic[u.user_id] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==u.user_id).first()
        return render_template('user/friendreq.html',profile=profile,friendrequest=friendrequest,pics=pics,pic=pic,users=users,id=id)
    else:
        return redirect(url_for('login_form'))





@app.route('/textr/friend_request/send/<id>')
def friend_request_send(id):
    if session.get('user') != None:
        ids = session.get('user')
        friendreq = FriendRequest.query.filter(FriendRequest.friend_request_targetid==id).filter(FriendRequest.friend_request_sourceid==ids).all()
        if friendreq == []:
            new_req = FriendRequest(friend_request_targetid=id,friend_request_sourceid=ids)
            db.session.add(new_req)
            db.session.commit()
            flash("<p class='alert alert-success'>Friend request sent successfully</p>")
            return redirect(url_for('friendreq'))
        else:
            flash('<p class="alert alert-warning">Friend request already sent</p>')
            return redirect(url_for('friendreq'))
    else:
        return redirect(url_for('login_form'))





@app.route('/textr/recieved/requests/<id>')
def recieved_request(id):
    if session.get('user') != None:
        ids = session.get('user')
        friends = Friends.query.filter(Friends.friends_sourceid==id).filter(Friends.friends_targetid==ids).all()
        if friends == []:
            new_friend = Friends(friends_sourceid=id,friends_targetid=ids)
            db.session.add(new_friend)
            friendreq = FriendRequest.query.filter(FriendRequest.friend_request_targetid==ids).filter(FriendRequest.friend_request_sourceid==id).first()
            db.session.delete(friendreq)
            db.session.commit()
            flash("<p class='alert alert-success'>Friend request approved successfully</p>")
            return redirect(url_for('friendreq'))
        else:
            flash("<p class='alert alert-success'>Already friends with user</p>")
            return redirect(url_for('friendreq'))
    else:
        return redirect(url_for('login_form'))
    



@app.route('/textr/delete/requests/<id>')
def recieved_request_delete(id):
    if session.get('user') != None:
        ids = session.get('user')
        friendreq = FriendRequest.query.filter(FriendRequest.friend_request_targetid==ids).filter(FriendRequest.friend_request_sourceid==id).first()
        if friendreq != None:
            db.session.delete(friendreq)
            db.session.commit()
            flash("<p class='alert alert-danger'>Friend request deleted successfully</p>")
            return redirect(url_for('friendreq'))
        else:
            return redirect(url_for('friendreq'))
    else:
        return redirect(url_for('login_form'))






@app.route('/textr/bio/new_bio', methods=['GET','POST'])
def update_bio():
    if session.get('user') != None:
        if request.method =='GET':
            return redirect(url_for('profile'))
        else:
            bio = request.form.get('bio')
            userbio=db.session.query(User).get(session['user'])
            userbio.user_bio = bio
            db.session.commit()
            flash('Bio Updated')
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login_form'))



@app.route('/textr/profile/')
def profile():
    if session.get('user') != None:
        id = session.get('user')
        user = User.query.get(id)
        current_time = datetime.utcnow()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        compic = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        cover = CoverPhoto.query.order_by(desc(CoverPhoto.cover_photo_id)).filter(CoverPhoto.cover_photo_userid==id).first()
        friends = Friends.query.filter(or_(Friends.friends_sourceid == id,Friends.friends_targetid == id)).all()
        pics = {}
        pic = {}
        for f in friends:
            pics[f.friends_sourceid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_sourceid).first()
            pic[f.friends_targetid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_targetid).first()
        post = db.session.query(Post).order_by(desc(Post.post_id)).filter(Post.post_userid==id).all()
        post_pic = db.session.query(Post).filter(Post.post_userid==id).filter(Post.post_media != None).all()
        like = {}
        comment = {}
        for p in post:
            like[p.post_id] = Like.query.filter_by(like_user_id=id, like_post_id=p.post_id).first()
            comment[p.post_id] = Comment.query.order_by(desc(Comment.comment_id)).filter(Comment.comment_postid==p.post_id).first()
        return render_template('user/profile.html',user=user,profile=profile,cover=cover,post=post,like=like,comment=comment,compic=compic,current_time=current_time,friends=friends,id=id,pics=pics,pic=pic,post_pic=post_pic)
    else:
        return redirect(url_for('login_form'))
    




@app.route('/textr/userprofile/<id>')
def user_profile(id):
    if session.get('user') != None:
        ids = session['user']
        user = User.query.get(id)
        current_time = datetime.utcnow()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        user_profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        compic = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        cover = CoverPhoto.query.order_by(desc(CoverPhoto.cover_photo_id)).filter(CoverPhoto.cover_photo_userid==id).first()
        friends = Friends.query.filter(or_(Friends.friends_sourceid == id,Friends.friends_targetid == id)).all()
        pics = {}
        pic = {}
        for f in friends:
            pics[f.friends_sourceid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_sourceid).first()
            pic[f.friends_targetid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_targetid).first()
        post = db.session.query(Post).order_by(desc(Post.post_id)).filter(Post.post_userid==id).all()
        post_pic = db.session.query(Post).filter(Post.post_userid==id).filter(Post.post_media != None).all()
        like = {}
        comment = {}
        for p in post:
            like[p.post_id] = Like.query.filter_by(like_user_id=id, like_post_id=p.post_id).first()
            comment[p.post_id] = Comment.query.order_by(desc(Comment.comment_id)).filter(Comment.comment_postid==p.post_id).first()
        return render_template('user/friends_profile.html',user=user,profile=profile,cover=cover,post=post,like=like,comment=comment,compic=compic,current_time=current_time,friends=friends,id=id,pics=pics,pic=pic,post_pic=post_pic,ids=ids,user_profile=user_profile)
    else:
        return redirect(url_for('login_form'))
    




@app.route('/textr/othersprofile/<id>')
def others_profile(id):
    if session.get('user') != None:
        ids = session['user']
        user = User.query.get(id)
        current_time = datetime.utcnow()
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        others_profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        compic = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).first()
        cover = CoverPhoto.query.order_by(desc(CoverPhoto.cover_photo_id)).filter(CoverPhoto.cover_photo_userid==id).first()
        friends = Friends.query.filter(or_(Friends.friends_sourceid == id,Friends.friends_targetid == id)).all()
        pics = {}
        pic = {}
        for f in friends:
            pics[f.friends_sourceid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_sourceid).first()
            pic[f.friends_targetid] = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==f.friends_targetid).first()
        post = db.session.query(Post).order_by(desc(Post.post_id)).filter(Post.post_userid==id).all()
        post_pic = db.session.query(Post).filter(Post.post_userid==id).filter(Post.post_media != None).all()
        like = {}
        comment = {}
        for p in post:
            like[p.post_id] = Like.query.filter_by(like_user_id=id, like_post_id=p.post_id).first()
            comment[p.post_id] = Comment.query.order_by(desc(Comment.comment_id)).filter(Comment.comment_postid==p.post_id).first()
        return render_template('user/others_profile.html',user=user,profile=profile,cover=cover,post=post,like=like,comment=comment,compic=compic,current_time=current_time,friends=friends,id=id,pics=pics,pic=pic,post_pic=post_pic,ids=ids,others_profile=others_profile)
    else:
        return redirect(url_for('login_form'))

    



@app.route('/textr/profile/new_post',methods=['GET','POST'])
def new_profile_post():
    if session.get('user') != None:
        if request.method == 'GET':
            return redirect(url_for('profile'))
        else:
            content = request.form.get('content')
            file=request.files['pix']
            filename= file.filename
            allowed = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG','.mp4','.MP4','.wmv','.WMV','.mkv','.MKV','.webm','.WEBM']
            if filename !='' and content !='':
                name,ext = os.path.splitext(filename)
                if ext in allowed:
                    id = session.get('user')
                    newname= generate_name()+ext
                    file.save('textr/static/post_media/'+newname)
                    p=Post(post_userid=id,post=content,post_media=newname)
                    db.session.add(p)
                    db.session.commit()
                    flash("Post Uploaded Successfully")
                    return redirect(url_for('home'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('profile'))
            elif filename !='':
                name,ext = os.path.splitext(filename)
                if ext in allowed:
                    id = session.get('user')
                    newname= generate_name()+ext
                    file.save('textr/static/post_media/'+newname)
                    p=Post(post_userid=id,post_media=newname)
                    db.session.add(p)
                    db.session.commit()
                    flash("Media Post Uploaded")
                    return redirect(url_for('home'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('profile'))
            elif content != '':
                id = session.get('user')
                p=Post(post_userid=id,post=content)
                db.session.add(p)
                db.session.commit()
                flash("Post Uploaded Successfully")
                return redirect(url_for('home'))
            else:
                flash("One or more fields not completed, Please complete your post")
                return redirect(url_for('profile'))
    else:
        return redirect(url_for('login_form'))

    



@app.route('/textr/new_post',methods=['GET','POST'])
def new_post():
    if session.get('user') != None:
        if request.method == 'GET':
            return redirect(url_for('post'))
        else:
            content = request.form.get('content')
            file=request.files['pix']
            filename= file.filename
            allowed = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG','.mp4','.MP4','.wmv','.WMV','.mkv','.MKV','.webm','.WEBM']
            if filename !='' and content !='':
                name,ext = os.path.splitext(filename)
                if ext in allowed:
                    id = session.get('user')
                    newname= generate_name()+ext
                    file.save('textr/static/post_media/'+newname)
                    p=Post(post_userid=id,post=content,post_media=newname)
                    db.session.add(p)
                    db.session.commit()
                    flash("Post Uploaded Successfully")
                    return redirect(url_for('home'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('home'))
            elif filename !='':
                name,ext = os.path.splitext(filename)
                if ext in allowed:
                    id = session.get('user')
                    newname= generate_name()+ext
                    file.save('textr/static/post_media/'+newname)
                    p=Post(post_userid=id,post_media=newname)
                    db.session.add(p)
                    db.session.commit()
                    flash("Media Post Uploaded")
                    return redirect(url_for('home'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('post'))
            elif content != '':
                id = session.get('user')
                p=Post(post_userid=id,post=content)
                db.session.add(p)
                db.session.commit()
                flash("Post Uploaded Successfully")
                return redirect(url_for('home'))
            else:
                flash("One or more fields not completed, Please complete your post")
                return redirect(url_for('home'))
    else:
        return redirect(url_for('login_form'))





@app.route('/textr/profile/cover_photo/',methods=["POST","GET"])
def cover_photo():
    if session.get('user') == None:
        return redirect(url_for('form'))
    else:
        if request.method == 'GET':
            return redirect(url_for('profile'))
        else:
            file=request.files['pix']
            filename= file.filename
            allowed = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG']
            if filename !='':
                name,ext = os.path.splitext(filename)
                if ext in allowed:
                    id=session.get('user')
                    newname= generate_name()+ext
                    file.save('textr/static/cover_photo/'+newname)
                    
                    # Crop the uploaded image
                    uploaded_image = Image.open(file)
                    left = 100
                    top = 100
                    right = 1200
                    bottom = 1200
                    cropped_image = uploaded_image.crop((left, top, right, bottom))
                    cropped_image.save('textr/static/cropped_cover/'+newname)
                    
                    c=CoverPhoto(cover_photo_userid=id,cover_photo=newname)
                    db.session.add(c)
                    db.session.commit()
                    flash("Cover Photo Updated Successfully")
                    return redirect(url_for('profile'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('profile'))
            else:
                flash("Please choose a file")
                return redirect(url_for('profile'))





@app.route('/textr/profile/picture/',methods=["POST","GET"])
def picture():
    if session.get('user') == None:
        return redirect(url_for('form'))
    else:
        if request.method == 'GET':
            return redirect(url_for('upload'))
        else:
            file=request.files['pix']
            filename= file.filename
            allowed = ['.png','.jpg','.jpeg','.JPG','.PNG','.JPEG']
            if filename !='':
                name,ext = os.path.splitext(filename)
                if ext in allowed:
                    id=session.get('user')
                    newname= generate_name()+ext
                    file.save('textr/static/uploads/'+newname)
                    
                    # Crop the uploaded image
                    uploaded_image = Image.open(file)
                    left = 100
                    top = 100
                    right = 400
                    bottom = 400
                    cropped_image = uploaded_image.crop((left, top, right, bottom))
                    cropped_image.save('textr/static/cropped_profile/'+newname)
                    
                    # Update the database with the new image name
                    p=ProfilePicture(profile_picture_userid=id,profile_picture=newname)
                    db.session.add(p)
                    db.session.commit()
                    
                    flash("Profile Picture Updated Successfully")
                    return redirect(url_for('profile'))
                else:
                    flash('File type not allowed')
                    return redirect(url_for('picture'))
            else:
                flash("Please choose a file")
                return redirect(url_for('picture'))







@app.route('/textr/show/profile_image/<id>')
def show_image(id):
    if session.get('user') != None:
        ids=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        profile_pic = ProfilePicture.query.get(id)
        return render_template('user/show_image.html',profile_pic=profile_pic,profile=profile)
    else:
        return redirect(url_for('login_form'))







@app.route('/textr/show/post_image/<id>')
def show_post(id):
    if session.get('user') != None:
        ids=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        post_media = Post.query.get(id)
        return render_template('user/show_post.html',post_media=post_media,profile=profile)
    else:
        return redirect(url_for('login_form'))







@app.route('/textr/show/cover_image/<id>')
def show_cover(id):
    if session.get('user') != None:
        ids=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==ids).first()
        ids=session.get('user')
        cover_photo = CoverPhoto.query.get(id)
        return render_template('user/show_cover.html',cover_photo=cover_photo,profile=profile)
    else:
        return redirect(url_for('login_form'))




@app.route('/textr/photos')
def photo_column():
    if session.get('user') != None:
        id=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        profile_pics = ProfilePicture.query.filter(ProfilePicture.profile_picture_userid==id).all()
        cover = CoverPhoto.query.filter(CoverPhoto.cover_photo_userid==id).all()
        post = Post.query.filter(Post.post_userid==id).all()
        return render_template('user/photo_column.html',profile=profile,cover=cover,post=post,profile_pics=profile_pics)
    else:
        return redirect(url_for('login_form'))





@app.route('/textr/profile_pics')
def profile_pics():
    if session.get('user') != None:
        id=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        pics = ProfilePicture.query.filter(ProfilePicture.profile_picture_userid==id).all()
        return render_template('user/profile_pics.html',profile=profile,pics=pics)
    else:
        return redirect(url_for('login_form'))





@app.route('/textr/cover_pics')
def cover_pics():
    if session.get('user') != None:
        id=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        cover = CoverPhoto.query.filter(CoverPhoto.cover_photo_userid==id).all()
        return render_template('user/cover_pics.html',cover=cover,profile=profile)
    else:
        return redirect(url_for('login_form'))




@app.route('/textr/post_media')
def post_media():
    if session.get('user') != None:
        id=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        media = Post.query.filter(Post.post_userid==id).all()
        return render_template('user/post_media.html',media=media,profile=profile)
    else:
        return redirect(url_for('login_form'))




@app.route('/textr/menu')
def menu():
    if session.get('user') != None:
        id=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        return render_template('user/menu.html',profile=profile)
    else:
        return redirect(url_for('login_form'))



@app.route('/textr/settings')
def settings():
    if session.get('user') != None:
        id=session.get('user')
        profile = ProfilePicture.query.order_by(desc(ProfilePicture.profile_picture_id)).filter(ProfilePicture.profile_picture_userid==id).first()
        return render_template('user/settings.html',profile=profile)
    else:
        return redirect(url_for('login_form'))




@app.route('/user/logout/')
def user_logout():
    if session.get('user')!=None:
        session.pop('user',None)
    return redirect(url_for("form"))