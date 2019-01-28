import requests
from requests import ConnectionError
from urllib3.exceptions import ResponseError
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from os import getenv
from random import randint
from xkcd_methods import get_comics
from xkcd_methods import get_comics_count
from xkcd_methods import XkcdAPIUnavailable
from vk_methods import upload_photo_to_vk
from vk_methods import post_photo_to_vk_wall
from vk_methods import save_img_to_vk
from vk_methods import get_vk_upload_adress
from vk_methods import VkAPIUnavailable


class OSException(Exception):
    pass


def delete_img_file(img_file_path):
    try:
        os.remove(img_file_path)
        return
    except (OSError, PermissionError, FileNotFoundError):
        raise OSException("Failed to remove {} !\nPossible reasons:\n"
                          "-Permission error\n"
                          "-File doesn't exist\n"
                          "-File descriptor is open".format(img_file_path))


def download_image(img_url=None, img_path=None):
    try:
        response = requests.get(img_url)
    except (ConnectionError, ResponseError):
        raise XkcdAPIUnavailable("{} is not available!".format(img_url))
    try:
        with open(img_path, "wb") as file:
            file.write(response.content)
            return img_path
    except (OSError, PermissionError):
        return


def extract_filename_from_url(url):
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return file_name


def open_img_to_upload(path_to_img):
    try:
        image_file_descriptor = open(path_to_img, 'rb')
    except (OSError, PermissionError, FileNotFoundError):
        raise OSException("Failed to open image file - {} !\n"
                          "Possible reasons:\n"
                          "-Permission error\n"
                          "-File doesn't exist\n"
                          "-File descriptor is open".format(path_to_img))
    img_file = {'photo': image_file_descriptor}
    return img_file


if __name__ == '__main__':
    load_dotenv()
    app_id = getenv("client_id")
    access_token = getenv("access_token")
    vk_group_id = getenv("vk_group_id")
    try:
        comics_count = get_comics_count()
        message, img_comics_url, title, url_comics = get_comics(randint(
            1,
            comics_count
        ))
        filename = extract_filename_from_url(img_comics_url)
        downloaded_img_path = download_image(img_comics_url, filename)
        if not downloaded_img_path:
            exit("No comics downloaded from Xkcd API!\nNothing to post!")
    except XkcdAPIUnavailable as error:
        exit(error)
    img_to_upload = open_img_to_upload(downloaded_img_path)
    try:
        upload_url = get_vk_upload_adress(
            vk_group_id,
            access_token
        )

        uploaded_photo, server, img_hash = upload_photo_to_vk(
            upload_url,
            img_to_upload
        )
        media_id, owner_id = save_img_to_vk(
            access_token,
            uploaded_photo,
            vk_group_id,
            server,
            img_hash
        )
        post_id = post_photo_to_vk_wall(
            vk_group_id,
            owner_id,
            media_id,
            message,
            access_token
        )
        print("You have successfully posted comics = {} to vk_group_id = {}\n"
              "Post_id = {}".format(url_comics, vk_group_id, post_id))
    except VkAPIUnavailable as error:
        exit(error)
    finally:
        img_to_upload['photo'].close()
        delete_img_file(downloaded_img_path)






