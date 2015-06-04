import requests
import json

def download_m3u8(vod_id):
    # Requests auth_token
    url = """https://api.twitch.tv/api/vods/{id}/access_token""".format(id=vod_id)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("API returned {0}".format(r.status_code))
    try:
        j = r.json()
        print(j)
        print(j['sig'])
        print(j['token'])
    except ValueError as e:
        print("API did not return valid JSON: {}".format(e))
        print("{}".format(r.text))
        quit()

    # Request to get m3u8 file
    url = """https://usher.justin.tv/vod/{id}?nauth={token}&nauthsig={sig}""".format(id=vod_id, sig=j['sig'], token=j['token'])
    m3u8_file = requests.get(url)
    if r.status_code != 200:
        raise Exception("API returned {0}".format(r.status_code))
    
    return m3u8_file
