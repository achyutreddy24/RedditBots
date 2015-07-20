import requests
import json
from random import random
from livestreamer.compat import urlparse
from livestreamer.exceptions import NoStreamsError, PluginError, StreamError
from livestreamer.plugin import Plugin, PluginOptions
from livestreamer.plugin.api import http, validate
from livestreamer.plugin.api.utils import parse_json, parse_query
from livestreamer.stream import (
    HTTPStream, HLSStream, FLVPlaylist, extract_flv_header_tags
)

from livestreamer.plugin.api import http_session
http = http_session.HTTPSession()



_access_token_schema = validate.Schema(
    {
        "token": validate.text,
        "sig": validate.text
    },
    validate.union((
        validate.get("sig"),
        validate.get("token")
    ))
)


class UsherService(object):
    def _create_url(self, endpoint, **extra_params):
        url = "http://usher.twitch.tv{0}".format(endpoint)
        params = {
            "player": "twitchweb",
            "p": int(random() * 999999),
            "type": "any",
            "allow_source": "true",
            "allow_audio_only": "true",
        }
        params.update(extra_params)

        req = requests.Request("GET", url, params=params)
        # prepare_request is only available in requests 2.0+
        if hasattr(http, "prepare_request"):
            req = http.prepare_request(req)
        else:
            req = req.prepare()

        return req.url

    def channel(self, channel, **extra_params):
        return self._create_url("/api/channel/hls/{0}.m3u8".format(channel),
                                **extra_params)

    def video(self, video_id, **extra_params):
        return self._create_url("/vod/{0}".format(video_id), **extra_params)

class TwitchAPI(object):
    def __init__(self, beta=False):
        self.oauth_token = None
        self.subdomain = beta and "betaapi" or "api"

    def add_cookies(self, cookies):
        http.parse_cookies(cookies, domain="twitch.tv")

    def call(self, path, format="json", schema=None, **extra_params):
        params = dict(as3="t", **extra_params)

        if self.oauth_token:
            params["oauth_token"] = self.oauth_token

        url = "https://{0}.twitch.tv{1}.{2}".format(self.subdomain, path, format)

        # The certificate used by Twitch cannot be verified on some OpenSSL versions.
        res = http.get(url, params=params, verify=False)

        if format == "json":
            return http.json(res, schema=schema)
        else:
            return res

    def access_token(self, endpoint, asset, **params):
        return self.call("/api/{0}/{1}/access_token".format(endpoint, asset), **params)

    def channel_info(self, channel, **params):
        return self.call("/api/channels/{0}".format(channel), **params)

    def channel_subscription(self, channel, **params):
        return self.call("/api/channels/{0}/subscription".format(channel), **params)

    def channel_viewer_info(self, channel, **params):
        return self.call("/api/channels/{0}/viewer".format(channel), **params)

    def token(self, **params):
        return self.call("/api/viewer/token", **params)

    def user(self, **params):
        return self.call("/kraken/user", **params)

    def videos(self, video_id, **params):
        return self.call("/api/videos/{0}".format(video_id), **params)

    def viewer_info(self, **params):
        return self.call("/api/viewer/info", **params)


def download_m3u8(vod_id):
    usher = UsherService()
    api = TwitchAPI()

    sig, token = api.access_token("vods", vod_id, schema=_access_token_schema)
    #json = api.access_token("vods", vod_id, schema=_access_token_schema)

    print('sig is '+str(sig))
    print('token is '+str(token))

    url = usher.video(vod_id, nauthsig=sig, nauth=token)

    return url
    # Requests auth_token
   # url = """https://api.twitch.tv/api/vods/{id}/access_token""".format(id=vod_id)
   # r = requests.get(url)
   # if r.status_code != 200:
   #     raise Exception("API returned {0}".format(r.status_code))
   # try:
   #     j = r.json()
   ##     print(j)
   #     print(j['sig'])
   #     print(j['token'])
   # except ValueError as e:
   #     print("API did not return valid JSON: {}".format(e))
   #     print("{}".format(r.text))
   #     quit()

    
    #return m3u8_file
