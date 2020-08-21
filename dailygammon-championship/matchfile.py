import requests
import sys

def matchfile(mid, cookies):
    URL = "http://dailygammon.com/bg/export/" + mid

    try:
        r = requests.get(URL, cookies=cookies)
        r.raise_for_status()
        return {
            "mid": mid,
            "res": r
        }

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
