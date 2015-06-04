import requests
import json

def download_m3u8(vod_id):

    pattern = """https://api.twitch.tv/api/vods/{id}""".format(id=vod_id)
        url = pattern.format(base=BASE_URL, id_=id_)
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("API returned {0}".format(r.status_code))

        try:
            j = r.json()
        except ValueError as e:
            print("API did not return valid JSON: {}".format(e))
            print("{}".format(r.text))
            quit()

