import requests
from requests import ConnectionError
from urllib3.exceptions import ResponseError

V = 5.92


class VkAPIUnavailable(Exception):
    pass


def upload_photo_to_vk(url, files):
    try:
        response = requests.post(url, files=files)
        if not response.ok:
            raise ResponseError
    except (ConnectionError, ResponseError):
        raise VkAPIUnavailable("{} is not available!".format(url))
    content = response.json()
    try:
        photo = content['photo']
        server = content['server']
        hash = content['hash']
        if not all([photo, server, hash]):
            raise KeyError
        return photo, server, hash
    except KeyError:
        raise VkAPIUnavailable("Something went wrong"
                               " during uploading photo to vk!\n"
                               "API-method - {}".format(url))


def post_photo_to_vk_wall(
        group_id,
        owner_id,
        media_id,
        message,
        access_token
):
    payload = {
        "owner_id": "-{}".format(group_id),
        "message": message,
        "attachments": "photo{}_{}".format(owner_id, media_id),
        "from_group": 1,
        "v": V,
        "access_token": access_token

    }
    url = "https://api.vk.com/method/wall.post"
    try:
        response = requests.post(url, params=payload)
        if not response.ok:
            raise ResponseError
    except (ConnectionError, ResponseError):
        raise VkAPIUnavailable("{} is not available!".format(url))
    content = response.json()
    try:
        post_id = content["response"]["post_id"]
    except KeyError:
        error_code = content['error']['error_code']
        error_msg = content['error']['error_msg']
        raise VkAPIUnavailable("Something went wrong"
                               " during posting to vk-wall!\n"
                               "API-method - {}\n"
                               "error_code - {}\n"
                               "error_msg - {}".format(url,
                                                       error_code,
                                                       error_msg
                                                       ))
    return post_id


def save_img_to_vk(access_token, photo, group_id, server, img_hash):
    payload = {
        "access_token": access_token,
        "group_id": group_id,
        "photo": photo,
        "server": server,
        "hash": img_hash,
        "v": V
    }
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    try:
        response = requests.post(url, params=payload)
        if not response.ok:
            raise ResponseError
    except (ConnectionError, ResponseError):
        raise VkAPIUnavailable("{} is not available!".format(url))
    try:
        content = response.json()['response'][0]
        media_id = content['id']
        owner_id = content['owner_id']
        return media_id, owner_id
    except KeyError:
        error_code = content['error']['error_code']
        error_msg = content['error']['error_msg']
        raise VkAPIUnavailable("Something went wrong"
                               " during saving photo to vk!\n"
                               "API-method - {}\n"
                               "error_code - {}\n"
                               "error_msg - {}".format(url,
                                                       error_code,
                                                       error_msg
                                                       ))


def get_vk_upload_adress(vk_group_id, access_token):
    payload = {
        "access_token": access_token,
        "scope": "photos",
        "group_id": vk_group_id,
        "v": V
    }
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    try:
        response = requests.get(url, params=payload)
        if not response.ok:
            raise ResponseError
    except (ConnectionError, ResponseError):
        raise VkAPIUnavailable("{} is not available!".format(url))
    content = response.json()
    try:
        upload_url = content['response']['upload_url']
    except KeyError:
        error_code = content['error']['error_code']
        error_msg = content['error']['error_msg']
        raise VkAPIUnavailable("Something went wrong"
                               " during getting vk-upload_url !\n"
                               "API-method - {}\n"
                               "error_code - {}\n"
                               "error_msg - {}".format(url,
                                                       error_code,
                                                       error_msg
                                                       ))
    return upload_url


if __name__ == '__main__':
    pass