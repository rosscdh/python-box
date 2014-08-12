python-box
=============

Python Client for box api (2014)


```
import requests as r
response = r.get('https://app.goclio.com/api/v2/activities', headers={'Authorization': 'Bearer :token'})


from box.box import Me
s=Me(token=':token')
s.get()


from box.box import Folders
s=Folders(token=':token')
s.get()

```


Refresh a token

```
social_auth = UserSocialAuth.objects.last()

updated_data = social_auth.get_backend_instance().refresh_token(token=':refresh_token_from_social_auth')

social_auth.extra_data.update(updated_data)
social_auth.save()
```
