from models import User, Post, db, connect_db, Tag, PostTag
from app import app
connect_db(app)
db.drop_all()
db.create_all()

user1 = User(first_name="mayuri",last_name="shah",img_url="")
user2 = User(first_name="mehul",last_name="shah",img_url="")
user3 = User(first_name="mayuri",last_name="shah",img_url="")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()

post1 = Post(title="t1",content = "abcd",user_id=1)
post2 = Post(title="t2",content = "abcd",user_id=2)
post3 = Post(title="t3",content = "abcd",user_id=1)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()


tag1=Tag(name='tag1')
tag2=Tag(name='tag2')
tag3 =Tag(name='tag3')

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()

posttag1 = PostTag(post_id = 1 ,tag_id = 1)
posttag2 = PostTag(post_id = 1,tag_id = 2)
posttag3 = PostTag(post_id = 1 ,tag_id = 3)
posttag4 = PostTag(post_id = 2,tag_id = 1)
posttag5 = PostTag(post_id = 2 ,tag_id = 2)

db.session.add(posttag1)
db.session.add(posttag2)
db.session.add(posttag3)
db.session.add(posttag4)
db.session.add(posttag5)

db.session.commit()


