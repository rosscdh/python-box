python-box
=============

Python Client for box api (2014)


```
from box.box import Me
s=Me(token=':token')
# tell me about the current user
s.get()

> {u'status': u'active', u'max_upload_size': 2147483648, u'name': u"Me McLastName", u'language': u'en', u'created_at': u'2014-05-16T00:13:13-07:00', u'address': u'', u'modified_at': u'2014-08-12T08:37:19-07:00', u'phone': u'+49555555555', u'avatar_url': u'https://app.box.com/api/avatar/large/216350218', u'space_used': 112950, u'space_amount': 10737418240, u'timezone': u'Europe/London', u'login': u'me@example.com', u'type': u'user', u'id': u'216350219', u'job_title': u'CTO'}

from box.box import Folders
s=Folders(token=':token')
# get all the users folders
s.get(id=0)
# look specifically at folder id 2
# 0 is the default folder relative to the user 0,1,2...
# each user has these folders
s.get(id=2)


from box.box import Files
fl=Files(token=':token')
fl.get()

#
# Get a files Tasks
#
from box.box import Files
fl=Files(token='hyTK09yBfIBo8JYfHpo5jxk0rDfjCHKL', id=19919416715)  # provide the file :id
fl.tasks()  # list tasks
#fl.create_task()  # not ready need integration with contacts
```


Refresh a token - Django using python-social-auth

```
social_auth = UserSocialAuth.objects.filter(provider='box').last()
refresh_token = social_auth.extra_data.get('refresh_token')
updated_data = social_auth.get_backend_instance().refresh_token(token=refresh_token)

social_auth.extra_data.update(updated_data)
social_auth.save()
```
