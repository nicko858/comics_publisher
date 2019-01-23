import requests
from requests import ConnectionError
from urllib3.exceptions import ResponseError


class XkcdAPIUnavailable(Exception):
    pass


def get_comics_count():
    url_comics = "https://xkcd.com/info.0.json"
    try:
        response = requests.get(url_comics)
        if not response.ok:
            raise ResponseError
    except (ConnectionError, ResponseError):
        raise XkcdAPIUnavailable("{} is not available!".format(url_comics))
    content = response.json()
    return content['num']


def get_comics(comics_number=None):
    if not comics_number:
        url_comics = "https://xkcd.com/info.0.json"
    else:
        url_comics = "https://xkcd.com/{}/info.0.json".format(comics_number)
    try:
        response = requests.get(url_comics)
        if not response.ok:
            raise ResponseError
    except (ConnectionError, ResponseError):
        raise XkcdAPIUnavailable("{} is not available!".format(url_comics))
    content = response.json()
    comment = content['alt']
    img_comics_url = content['img']
    title = content['title']
    return [comment, img_comics_url, title, url_comics]


if __name__ == '__main__':
    pass