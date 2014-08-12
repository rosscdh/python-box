import re
import json
import requests
import urlparse


class BaseApi(object):
    base_url = {
        'base': 'https://api.box.com/2.0/',
        'upload': 'https://upload.box.com/api/2.0/'
    }

    r = requests

    def __init__(self, token, **kwargs):
        self.token = token
        self.response = self.response_json = {}
        self.params = kwargs

    @property
    def auth(self):
        return {'Authorization': 'Bearer %s' % self.token}

    @property
    def status_code(self):
        return getattr(self.response, 'status_code', None)

    @property
    def ok(self):
        return getattr(self.response, 'ok', None)

    @property
    def parse_uri(self):
        uri = self.uri

        for k, v in self.params.iteritems():
            key = ':{key}'.format(key=k)
            uri = uri.replace(key, str(v))
        # removed extranuous /:keys from the urls
        return re.sub(r'\/\:(\w)+', '', uri)

    def headers(self, **kwargs):
        headers = {'Content-Type': 'application/json'}
        headers.update(kwargs)
        headers.update(self.auth)
        return headers

    def wrap_namespace(self, **kwargs):
        return json.dumps(kwargs)

    def endpoint(self, *args, **kwargs):
        return urlparse.urljoin(self.base_url.get(kwargs.get('api', 'base')), self.parse_uri, *args, **kwargs)

    def process(self, response):
        self.response = response
        if response.ok is True:
            self.response_json = self.response.json()
            return self.response_json
        #
        # Handle the bad BOX api implementation of 404 returning HTML and not
        # a valid REST reponse
        #
        return {'message': response.reason, 'ok': response.ok, 'status_code': response.status_code, 'url': response.url}

    def get(self, **kwargs):
        return self.process(response=self.r.get(self.endpoint(), headers=self.headers(), params=kwargs))

    def post(self, **kwargs):
        return self.process(response=self.r.post(self.endpoint(), headers=self.headers(), data=self.wrap_namespace(**kwargs)))

    def put(self, **kwargs):
        return self.process(response=self.r.put(self.endpoint(), headers=self.headers(), data=self.wrap_namespace(**kwargs)))

    def patch(self, **kwargs):
        return self.process(response=self.r.patch(self.endpoint(), headers=self.headers(), data=self.wrap_namespace(**kwargs)))

    def delete(self, **kwargs):
        return self.process(response=self.r.delete(self.endpoint(), headers=self.headers(), params=kwargs))


class Me(BaseApi):
    uri = 'users/me'


class Folders(BaseApi):
    uri = 'folders/:id'

    def __init__(self, **kwargs):
        #
        # By default the base box folder is id: 0
        #
        if 'id' not in kwargs:
            kwargs.update({'id': 0})
        super(Folders, self).__init__(**kwargs)

class Files(BaseApi):
    uri = 'files/:id'

