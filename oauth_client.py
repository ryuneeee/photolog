import oauth2 as oauth
import configparser
from urllib.parse import parse_qsl


class OAuthClient:
    def __init__(self):
        super().__init__()
        self.consumer = None
        self.callback_url = None
        self.oauth_token = None
        self.oauth_token_secret = None
        self.user_nsid = None
        self.read_config()

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read('photolog.cfg')
            self.user_nsid = config['Flickr_token']['user_nsid']
            self.oauth_token = config['Flickr_token']['oauth_token']
            self.oauth_token_secret = config['Flickr_token']['oauth_token_secret']
            self.init_consumer(config['Flickr_token']['oauth_consumer_token'],
                               config['Flickr_token']['oauth_consumer_token_secret'])

        except:
            pass

    def request_token(self):
        request_token_url = 'https://www.flickr.com/services/oauth/request_token?oauth_callback=' + self.callback_url
        client = oauth.Client(self.consumer)
        resp, content = client.request(request_token_url, "GET")
        path = content.decode().split('&')
        oauth_token = path[1][12:]
        self.oauth_token_secret = path[2][19:]

        return oauth_token

    def callback(self, oauth_token, verifier):
        token = oauth.Token(oauth_token, self.oauth_token_secret)
        token.set_verifier(verifier)
        client = oauth.Client(self.consumer, token)
        resp, content = client.request('https://www.flickr.com/services/oauth/access_token')
        access_token = dict(parse_qsl(content.decode()))

        self.oauth_token = access_token['oauth_token']
        self.oauth_token_secret = access_token['oauth_token_secret']

        write_config(self.consumer, access_token)
        return access_token

    def init_consumer(self, key, secret):
        self.consumer = oauth.Consumer(key=key, secret=secret)

    def get_authorize_url(self, token):
        return 'https://www.flickr.com/services/oauth/authorize?oauth_token=' + token

    def request(self):
        token = oauth.Token(self.oauth_token, self.oauth_token_secret)
        client = oauth.Client(self.consumer, token)
        resp, content = client.request('https://api.flickr.com/services/rest?method=flickr.people.getPhotos&'
                                       'user_id={user_nsid}&format=json&nojsoncallback=1&extras=original_format,description'
                                       .format(user_nsid=self.user_nsid))
        return content.decode()


def write_config(consumer, access_token):
    config = configparser.ConfigParser()
    config['Flickr_token'] = {'oauth_consumer_token': consumer.key,
                              'oauth_consumer_token_secret': consumer.secret,
                              'oauth_token': access_token['oauth_token'],
                              'oauth_token_secret': access_token['oauth_token_secret'],
                              'user_nsid': access_token['user_nsid'],
                              'username': access_token['username']}

    with open('photolog.cfg', 'w') as configfile:
        config.write(configfile)
