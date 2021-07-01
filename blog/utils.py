import base64
import os
import secrets
import uuid

import ffmpeg
import pyrebase as pyrebase
from PIL import Image
import core.settings
from core.settings import BASE_DIR

current_path = os.path.dirname(__file__) + '/staticfiles/temp/'

FIREBASE_CONFIG = core.settings.FIREBASE_CONFIG


def auth_headers(token):
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }


def return_files_data_for_post(request):
    files_data = dict()
    image = request.FILES.get('image')
    video = request.FILES.get('video')
    if image:
        files_data.update({'image': image})
    if video:
        files_data.update({'video': video})
    return files_data


def return_form_data_for_post(request):
    form_data = {
        "title": request.data.get("title"),
        "category": request.data.get("category"),
        "content": request.data.get("content"),
    }

    return form_data


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.name)

    filename_hexed = random_hex + f_ext
    picture_path = os.path.join(current_path, filename_hexed)
    output_size = (540, 540)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    url_image = put_image(picture_path, filename_hexed)
    os.remove(picture_path)

    return url_image


def put_image(path_to_file, new_filename):
    firebase_storage = pyrebase.initialize_app(config=FIREBASE_CONFIG)

    storage = firebase_storage.storage()
    storage.child(new_filename).put(path_to_file)

    return get_url_of_image(new_filename)


def get_url_of_image(firebase_file_name):
    firebase_storage = pyrebase.initialize_app(FIREBASE_CONFIG)
    storage = firebase_storage.storage()

    email = 'commerce.tf@gmail.com'
    password = 'alex2811'
    auth = firebase_storage.auth()

    user = auth.sign_in_with_email_and_password(email, password)
    url = storage.child(firebase_file_name).get_url(user['idToken'])
    import re
    url = re.findall('(.+)&token', url)[0]
    return url


def delete_obj():
    pass


# def save_video(video_instance):
#     # get uniq name for TempVideo Model
#     uniq_name = str(uuid.uuid4())
#
#     # creating instance of TempVideo
#     instance = TempVideo(video_name=uniq_name, videofile=video_instance)
#     instance.save()
#
#     # setting var with path of video instance
#     video_path = instance.videofile.path
#
#     # get extension of video file
#     _, f_ext = os.path.splitext(video_path)
#     url = put_image(video_path, uniq_name)
#     os.remove(video_path)
#     instance.delete()
#     return url
