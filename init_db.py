from datetime import datetime

from forum.models import Forum, Post, Thread
from user.models import User

u = User.objects.create(username='User name', email='email@mail.com',
                        name='First name', about='about info')

f = Forum.objects.create(user=u, name='New forum', short_name='newforum')

t = Thread.objects.create(forum=f, user=u, title='New title', message='Test message',
                          slug='newthread', isClosed=False, date=datetime.now())

p = Post.objects.create(user=u, thread=t, message='Post mess', date=datetime.now())
