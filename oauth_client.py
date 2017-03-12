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
        resp, content = client.request('https://www.flickr.com/services/oauth/access_token', "POST")
        access_token = dict(parse_qsl(content.decode()))

        write_config(access_token)
        return access_token

    def init_consumer(self, key, secret):
        self.consumer = oauth.Consumer(key=key, secret=secret)

    def get_authorize_url(self, token):
        return 'https://www.flickr.com/services/oauth/authorize?oauth_token=' + token


def write_config(access_token):
    config = configparser.ConfigParser()
    config['Flickr_token'] = {'oauth_token': access_token['oauth_token'],
                              'oauth_token_secret': access_token['oauth_token_secret'],
                              'user_nsid': access_token['user_nsid'],
                              'username': access_token['username']}

    with open('photolog.cfg', 'w') as configfile:
        config.write(configfile)
