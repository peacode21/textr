from datetime import datetime

from textr import db

class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    user_fname = db.Column(db.String(45),nullable=False)
    user_mname = db.Column(db.String(45),nullable=True)
    user_lname = db.Column(db.String(45),nullable=False)
    user_pwd=db.Column(db.String(180),nullable=False) 
    user_username = db.Column(db.String(45),nullable=False)
    user_email = db.Column(db.String(65),nullable=False) 
    user_phone=db.Column(db.String(20),nullable=False) 
    user_gender =db.Column(db.String(20),nullable=False) 
    user_address = db.Column(db.String(155),nullable=True) 
    user_bio = db.Column(db.String(255),nullable=True) 
    user_registerat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    user_lastlogin=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    
    #Foreign keys
    user_stateid = db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)

    #setup
    userstate = db.relationship('State',back_populates='stateuser')
    userpicture = db.relationship('ProfilePicture',back_populates='pictureuser')
    userpost = db.relationship('Post',back_populates='postuser')
    usergrouppost = db.relationship('GroupPost',back_populates='grouppostuser')
    usergroupmessage = db.relationship('GroupMessage',back_populates='groupmessageuser')
    usergroupmembers = db.relationship('GroupMembers',back_populates='groupmembersuser')
    usergroupadmin = db.relationship('GroupAdmin',back_populates='groupadminuser')
    usercoverpix = db.relationship('CoverPhoto',back_populates='coverpixuser')
    userlike = db.relationship('Like',back_populates='likeuser')
    commentpostuser = db.relationship('GroupPostComments',back_populates='postusercomment')
    usergrouppostlike = db.relationship('GroupPostLike',back_populates='likegrouppostuser')
    usercomment = db.relationship('Comment',back_populates='commentuser')


class State(db.Model):
    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    state = db.Column(db.String(155),nullable=False)

    #Foreign keys
    state_countryid = db.Column(db.Integer, db.ForeignKey('country.country_id'),nullable=False)

    #setup
    statecountry = db.relationship('Country',back_populates='countrystate')
    stateuser = db.relationship('User',back_populates='userstate')


class ProfilePicture(db.Model):
    profile_picture_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    profile_picture = db.Column(db.Text(),nullable=False)

    #Foreign keys
    profile_picture_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    pictureuser = db.relationship('User',back_populates='userpicture')


class Post(db.Model):
    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post = db.Column(db.Text(),nullable=True)
    post_media = db.Column(db.Text(),nullable=True)
    post_created_at=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    post_updated_at=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    
    #Foreign keys
    post_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    postuser = db.relationship('User',back_populates='userpost')
    likepost = db.relationship('Like',back_populates='postlike')
    postcomment = db.relationship('Comment',back_populates='commentpost')


class Message(db.Model):
    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    message = db.Column(db.Text(),nullable=False)
    message_created_at=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    message_updated_at=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)

    #Foreign keys
    message_sourceid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    message_targetid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    source_user = db.relationship('User', foreign_keys=[message_sourceid], backref='sourcemessage')
    target_user = db.relationship('User', foreign_keys=[message_targetid], backref='targetmessage')




class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)

    #Foreign keys
    like_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    like_post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))

    #setup
    likeuser = db.relationship('User',back_populates='userlike')
    postlike = db.relationship('Post',back_populates='likepost')



class GroupProfilePicture(db.Model):
    group_profile_picture_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_profile_picture = db.Column(db.Text(),nullable=False)
    
    #Foreign keys
    group_profile_picture_groupid = db.Column(db.Integer, db.ForeignKey('group.group_id'),nullable=False)

    #setup
    grouppix = db.relationship('Group',back_populates='pixgroup')


class GroupPostLike(db.Model):
    group_post_like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    #Foreign keys
    group_post_like_group_post_id = db.Column(db.Integer, db.ForeignKey('group_post.group_post_id'),nullable=False)
    group_post_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    likegrouppost = db.relationship('GroupPost',back_populates='grouppostlike')
    likegrouppostuser = db.relationship('User',back_populates='usergrouppostlike')


class GroupPost(db.Model):
    group_post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_post = db.Column(db.Text(),nullable=False)
    group_post_createdat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    group_post_updatedat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    group_post_media = db.Column(db.Text(),nullable=True)
    
    #Foreign keys
    group_post_groupid = db.Column(db.Integer, db.ForeignKey('group.group_id'),nullable=False)
    group_post_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    postgroup = db.relationship('Group',back_populates='grouppost')
    grouppostuser = db.relationship('User',back_populates='usergrouppost')
    grouppostlike = db.relationship('GroupPostLike',back_populates='likegrouppost')
    postcommentgroup = db.relationship('GroupPostComments',back_populates='groupcommentpost')


class GroupPostComments(db.Model):
    group_post_comments_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_post_comments = db.Column(db.Text(),nullable=False)
    group_post_createdat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    group_post_updatedat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    
    #Foreign keys
    group_post_comments_group_postid = db.Column(db.Integer, db.ForeignKey('group_post.group_post_id'),nullable=False)
    group_post_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    groupcommentpost = db.relationship('GroupPost',back_populates='postcommentgroup')
    postusercomment = db.relationship('User',back_populates='commentpostuser')


class GroupMessage(db.Model):
    group_message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_message = db.Column(db.Text(),nullable=False)
    group_message_createdat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    group_message_updatedat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    group_message_media = db.Column(db.Text(),nullable=True)
    
    #Foreign keys
    group_message_groupid = db.Column(db.Integer, db.ForeignKey('group.group_id'),nullable=False)
    group_message_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    messagegroup = db.relationship('Group',back_populates='groupmessage')
    groupmessageuser = db.relationship('User',back_populates='usergroupmessage')


class GroupMembers(db.Model):
    group_members_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_members_joinedat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)
    
    #Foreign keys
    group_members_groupid = db.Column(db.Integer, db.ForeignKey('group.group_id'),nullable=False)
    group_members_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    membersgroup = db.relationship('Group',back_populates='groupmembers')
    groupmembersuser = db.relationship('User',back_populates='usergroupmembers')


class GroupCoverPhoto(db.Model):
    group_cover_photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_cover_photo = db.Column(db.Text(),nullable=False)
    
    #Foreign keys
    group_cover_photo_groupid = db.Column(db.Integer, db.ForeignKey('group.group_id'),nullable=False)

    #setup
    groupcoverphoto = db.relationship('Group',back_populates='coverphotogroup')


class GroupAdmin(db.Model):
    group_admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    
    #Foreign keys
    group_admin_groupid = db.Column(db.Integer, db.ForeignKey('group.group_id'),nullable=False)
    group_admin_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    admin_group = db.relationship('Group', foreign_keys=[group_admin_groupid], backref='admingroup')
    groupadminuser = db.relationship('User',back_populates='usergroupadmin')


class Group(db.Model):
    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_name = db.Column(db.String(75),nullable=False)
    group_summary = db.Column(db.Text(),nullable=True)
    group_status = db.Column(db.String(15),nullable=False,server_default=('Active'))
    group_createdat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    group_updatedat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    
    #Foreign keys
    group_createdby_group_adminid = db.Column(db.Integer, db.ForeignKey('group_admin.group_admin_id'),nullable=False)
    group_updatedby_group_adminid = db.Column(db.Integer, db.ForeignKey('group_admin.group_admin_id'),nullable=True)
    
    #setup
    group_createdby = db.relationship('GroupAdmin', foreign_keys=[group_createdby_group_adminid], backref='groupcreatedby')
    group_updatedby = db.relationship('GroupAdmin', foreign_keys=[group_updatedby_group_adminid], backref='groupupdatedby')
    coverphotogroup = db.relationship('GroupCoverPhoto',back_populates='groupcoverphoto')
    groupmembers = db.relationship('GroupMembers',back_populates='membersgroup')
    groupmessage = db.relationship('GroupMessage',back_populates='messagegroup')
    grouppost = db.relationship('GroupPost',back_populates='postgroup')
    pixgroup = db.relationship('GroupProfilePicture',back_populates='grouppix')


class FriendRequest(db.Model):
    friend_request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    friend_request_createdat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)
    
    #Foreign keys
    friend_request_sourceid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    friend_request_targetid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    
    #setup
    source_friend_request = db.relationship('User', foreign_keys=[friend_request_sourceid], backref='sourcefriendrequest')
    target_friend_request = db.relationship('User', foreign_keys=[friend_request_targetid], backref='targetfriendrequest')


class Friends(db.Model):
    friends_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    friends_status = db.Column(db.String(45),nullable=False,server_default=('Friends'))
    friends_created_at=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False)  
    friends_updated_at=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True)
    
    #Foreign keys
    friends_sourceid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    friends_targetid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    
    #setup
    source_friends = db.relationship('User', foreign_keys=[friends_sourceid], backref='sourcefriends')
    target_friends = db.relationship('User', foreign_keys=[friends_targetid], backref='targetfriends')


class CoverPhoto(db.Model):
    cover_photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cover_photo = db.Column(db.Text(),nullable=False)
    
    #Foreign keys
    cover_photo_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)

    #setup
    coverpixuser = db.relationship('User',back_populates='usercoverpix')


class Country(db.Model):
    country_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    country = db.Column(db.String(75),nullable=False)

    #setup
    countrystate = db.relationship('State',back_populates='statecountry')


class Comment(db.Model):
    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.Text(),nullable=False)
    comment_createdat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=False) 
    comment_updatedat=db.Column(db.DateTime(), default=datetime.utcnow,nullable=True) 
    
    #Foreign keys
    comment_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    comment_postid = db.Column(db.Integer, db.ForeignKey('post.post_id'),nullable=False)

    #setup
    commentuser = db.relationship('User',back_populates='usercomment')
    commentpost = db.relationship('Post',back_populates='postcomment')



