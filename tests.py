from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='ashwani')
        u.set_password('ashwani')
        self.assertFalse(u.check_password('awesome'))
        self.assertTrue(u.check_password('ashwani'))

    def test_avatar(self):
        u = User(username='user', email='user@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'b58996c504c5638798eb6b511e6f49af'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='susan', email='susan@example.com')
        u2 = User(username='robin', email='robin@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followers.all(), [])
        self.assertEqual(u1.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'robin')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'susan')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='virat', email='virat@example.com')
        u2 = User(username='kedar', email='kedar@example.com')
        u3 = User(username='pant', email='pant@example.com')
        u4 = User(username='rohit', email='rohit@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create posts
        now = datetime.utcnow()
        p1 = Post(body='C\'mon I got a 100 today', author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body='I am the next finisher', author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body='C\'mon lads! We have a special guest here today',
                  author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body='I have three 200s B:', author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        #setup the followers
        # virat follow rohit
        u1.follow(u4)
        # everyone follow virat
        u2.follow(u1)
        u3.follow(u1)
        u4.follow(u1)
        # pant follow all
        u3.follow(u2)
        u3.follow(u4)
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p4, p1])
        self.assertEqual(f2, [p2, p1])
        self.assertEqual(f3, [p2, p3, p4, p1])
        self.assertEqual(f4, [p4, p1])


if __name__ == '__main__':
    unittest.main(verbosity=2)