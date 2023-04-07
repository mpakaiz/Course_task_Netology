import requests
import time
import json
from ya_disk import YandexDisk
from gdriveclass import Gdrive
from os import path
from tqdm import tqdm


TOKEN = str(input('Введите токен с Полигона Яндекс.Диска: '))
# TOKEN = 'y0_AgAAAAACohocAADLWwAAAADezu9emLKFzwSpRx25Ah6D94krf7IB0kM'
ya = YandexDisk(token=TOKEN)
# 1089625

# 'y0_AgAAAAACohocAADLWwAAAADezu9emLKFzwSpRx25Ah6D94krf7IB0kM'


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_albums(self, user_id):
        albums = self.url + 'photos.getAlbums'

        albums_params = {
            'count': 200,
            'user_id': user_id,

        }

        req = requests.get(albums, params={**self.params, **albums_params}).json()
        albums_list = req['response']['items']
        albums_names = [str(album['title']) for album in albums_list]
        print('У пользователя есть следующие альбомы: ')
        for i, j in enumerate(albums_names, 1):
            print(f"{i}: {j}")
        select_album = int(input('Введите номера альбома из которого нужно сохранить фотографии: '))
        return albums_list[select_album - 1]['id']

    def get_photos(self, user_id):
        photos = self.url + 'photos.get'
        count = int(input('Сколько фото необходимо загрузить?: '))
        get_photos_params = {
            'count': count,
            'extended': 1,
            'user_id': user_id,
            'album_id': 'profile'
        }

        req = requests.get(photos, params={**self.params, **get_photos_params}).json()
        all_files = []
        folder = ya.create_folder()
        for i in tqdm(req['response']['items']):
            time.sleep(0.1)
            info = {}
            likes = set()
            for j in i.get('sizes'):
                if j.get('type') == 'z':
                    a = path.basename(j.get('url'))
                    b = path.splitext(a)[1].split('?')[0]
                    url = j.get('url').strip()
                    if i.get('likes').get('count') not in likes:
                        info['file_name'] = str(i.get('likes').get('count')) + b
                        info['size'] = j.get('type')
                        all_files.append(info)
                        likes.add(i.get('likes').get('count'))
                    else:
                        info['file_name'] = str(i.get('date')) + "_" + str(i.get('likes').get('count')) + b
                        info['size'] = j.get('type')
                        all_files.append(info)
                    with open('image.jpg', 'wb') as image:
                        response = requests.get(url)
                        image.write(response.content)
                    ya.upload_file_to_disk(f"{folder}/{info['file_name']}", 'image.jpg')
                    print(f"В папку {folder} загружена фотография {info['file_name']} в формате {j.get('type')}")
        with open('data.json', 'w') as f:
            json.dump(all_files, f, indent=2)

    def get_album_photos(self, user_id):
        album = self.get_albums(user_id)
        self.get_photos_from_albums(user_id, album)

    def get_photos_from_albums(self, user_id, album_id):

        photos = self.url + 'photos.get'
        count = int(input('Сколько фото необходимо загрузить?: '))
        get_photos_params = {
            'count': count,
            'extended': 1,
            'user_id': user_id,
            'album_id': album_id
        }

        req = requests.get(photos, params={**self.params, **get_photos_params}).json()
        all_files = []
        likes = set()
        folder = ya.create_folder()

        for i in tqdm(req['response']['items']):
            time.sleep(0.1)
            info = {}
            for j in reversed(i.get('sizes')):
                a = path.basename(j.get('url'))
                b = path.splitext(a)[1].split('?')[0]
                url = j.get('url').strip()
                if i.get('likes').get('count') not in likes:
                    info['file_name'] = str(i.get('likes').get('count')) + b
                    info['size'] = j.get('type')
                    all_files.append(info)
                    likes.add(i.get('likes').get('count'))
                else:
                    info['file_name'] = str(i.get('date')) + "_" + str(i.get('likes').get('count')) + b
                    info['size'] = j.get('type')
                    all_files.append(info)
                with open('image.jpg', 'wb') as image:
                    response = requests.get(url)
                    image.write(response.content)
                ya.upload_file_to_disk(f"{folder}/{info['file_name']}", 'image.jpg')
                print(f"В папку {folder} загружена фотография {info['file_name']} в формате {j.get('type')}")
                break
        with open('data.json', 'w') as f:
            json.dump(all_files, f, indent=2)

    def get_photos_to_gdrive(self, user_id):
        photos = self.url + 'photos.get'
        count = int(input('Сколько фото необходимо загрузить?: '))
        get_photos_params = {
            'count': count,
            'extended': 1,
            'user_id': user_id,
            'album_id': 'profile'
        }

        req = requests.get(photos, params={**self.params, **get_photos_params}).json()
        all_files = []
        for i in tqdm(req['response']['items']):
            time.sleep(0.1)
            info = {}
            likes = set()
            for j in i.get('sizes'):
                if j.get('type') == 'z':
                    a = path.basename(j.get('url'))
                    b = path.splitext(a)[1].split('?')[0]
                    url = j.get('url').strip()
                    if i.get('likes').get('count') not in likes:
                        info['file_name'] = str(i.get('likes').get('count')) + b
                        info['size'] = j.get('type')
                        all_files.append(info)
                        likes.add(i.get('likes').get('count'))
                    else:
                        info['file_name'] = str(i.get('date')) + "_" + str(i.get('likes').get('count')) + b
                        info['size'] = j.get('type')
                        all_files.append(info)
                    with open('image.jpg', 'wb') as image:
                        response = requests.get(url)
                        image.write(response.content)
                    Gdrive.upload_photo(f"{info['file_name']}", f"{info['file_name']}")
                    print(f"В папку загружена фотография {info['file_name']} в формате {j.get('type')}")
        with open('data.json', 'w') as f:
            json.dump(all_files, f, indent=2)

    def get_photos_from_albums_gdrive(self, user_id, album_id):

        photos = self.url + 'photos.get'
        count = int(input('Сколько фото необходимо загрузить?: '))
        get_photos_params = {
            'count': count,
            'extended': 1,
            'user_id': user_id,
            'album_id': album_id
        }

        req = requests.get(photos, params={**self.params, **get_photos_params}).json()
        all_files = []
        likes = set()

        for i in tqdm(req['response']['items']):
            time.sleep(0.1)
            info = {}
            for j in reversed(i.get('sizes')):
                a = path.basename(j.get('url'))
                b = path.splitext(a)[1].split('?')[0]
                url = j.get('url').strip()
                if i.get('likes').get('count') not in likes:
                    info['file_name'] = str(i.get('likes').get('count')) + b
                    info['size'] = j.get('type')
                    all_files.append(info)
                    likes.add(i.get('likes').get('count'))
                else:
                    info['file_name'] = str(i.get('date')) + "_" + str(i.get('likes').get('count')) + b
                    info['size'] = j.get('type')
                    all_files.append(info)
                with open('image.jpg', 'wb') as image:
                    response = requests.get(url)
                    image.write(response.content)
                Gdrive.upload_photo(f"{info['file_name']}", f"{info['file_name']}")
                print(f"В папку загружена фотография {info['file_name']} в формате {j.get('type')}")
                break
        with open('data.json', 'w') as f:
            json.dump(all_files, f, indent=2)
