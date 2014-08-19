import re
import json
import requests
import urlparse


class BaseApi(object):
    base_url = {
        'base': 'https://api.box.com/2.0/',
        'upload': 'https://upload.box.com/api/2.0/',
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

    def endpoint(self, action='get', *args, **kwargs):
        return urlparse.urljoin(self.base_url.get('base'), self.parse_uri, *args, **kwargs)

    def process(self, response):
        self.response = response

        if response.ok is True:
            try:

                self.response_json = self.response.json()
                return self.response_json

            except Exception as e:
                self.response_json = None

        #
        # Handle the bad BOX api implementation of 404 returning HTML and not
        # a valid REST reponse
        #
        return {'message': response.reason, 'ok': response.ok, 'status_code': response.status_code, 'url': response.url}

    def get(self, **kwargs):
        return self.process(response=self.r.get(self.endpoint(), headers=self.headers(), params=kwargs))

    def post(self, files=None, **kwargs):
        return self.process(response=self.r.post(self.endpoint(action='post'), headers=self.headers(), files=files, data=self.wrap_namespace(**kwargs)))

    def put(self, files=None, **kwargs):
        return self.process(response=self.r.put(self.endpoint(action='put'), headers=self.headers(), files=files, data=self.wrap_namespace(**kwargs)))

    def options(self, **kwargs):
        return self.process(response=self.r.options(self.endpoint(action='list')))

    def delete(self, **kwargs):
        return self.process(response=self.r.delete(self.endpoint(action='delete'), headers=self.headers(), params=kwargs))


class Me(BaseApi):
    uri = 'users/me'


class Folders(BaseApi):
    uri = 'folders/:id'


class Files(BaseApi):
    uri = 'files/:id'

    def tasks(self, **kwargs):
        if self.params.get('id', None) is None:
            raise Exception('Must have task id params')
        t = self.Tasks(token=self.token, id=self.params.get('id'), action_type='list')
        return t.get(**kwargs)

    def create_task(self, **kwargs):
        if self.params.get('id', None) is None:
            raise Exception('Must have task id params')
        t = self.Tasks(token=self.token, action_type='crud')
        return t.post(item={'type': 'file', 'id': self.params.get('id')}, action=kwargs.pop('action', 'review'), **kwargs)

    class Tasks(BaseApi):
        uri = None
        uris = {
            'list': 'files/:id/tasks',
            'crud': 'tasks/:id',
        }

        def __init__(self, action_type='list', *args, **kwargs):
            self.uri = self.uris.get(action_type, 'list')  # select appropriate uri
            super(Files.Tasks, self).__init__(*args, **kwargs)



class UploadFiles(BaseApi):
    """
    https://developers.box.com/docs/#files-upload-a-file
    curl https://upload.box.com/api/2.0/files/content \
    -H "Authorization: Bearer ACCESS_TOKEN" \
    -F filename=@FILE_NAME \
    -F parent_id=PARENT_FOLDER_ID
    """
    uri = 'files/:id/content'

    def headers(self, **kwargs):
        headers = super(UploadFiles, self).headers(**kwargs)

        if headers.get('Content-Type', None) == 'application/json':
            # remove the JSOn content type as this is multipart
            headers.pop('Content-Type', None)

        if self.params.get('sha1', None) is not None:
            headers.update({
                'Content-MD5': self.params.get('sha1'),
            })
        return headers

    def wrap_namespace(self, **kwargs):
        """
        Dont convert to json as this is a file upload
        """
        return kwargs

    def endpoint(self, action, *args, **kwargs):
        uri = self.base_url.get('upload')
        return urlparse.urljoin(uri, self.parse_uri, *args, **kwargs)


class Events(BaseApi):
    uri = 'events/:id'

