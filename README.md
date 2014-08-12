python-box
=============

Python Client for box api (2014)


```
import requests as r
response = r.get('https://app.goclio.com/api/v2/activities', headers={'Authorization': 'Bearer :token'})


from box.box import Me
s=Me(token=':token')
# tell me about the current user
s.get()


from box.box import Folders
s=Folders(token=':token')
# get all the users folders
s.get()
# look specifically at folder id 2
# 0 is the default folder relative to the user 0,1,2...
# each user has these folders
s.get(id=2)


from box.box import Files
fl=Files(token=':token')
fl.get()
```


Refresh a token

```
social_auth = UserSocialAuth.objects.last()

updated_data = social_auth.get_backend_instance().refresh_token(token=':refresh_token_from_social_auth')

social_auth.extra_data.update(updated_data)
social_auth.save()
```
