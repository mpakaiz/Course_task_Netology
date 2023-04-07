with open('text.txt', 'r') as file_object:
    token = file_object.read().strip()

from vkclass import VkUser
vk_client = VkUser(token, '5.131')


def vk_photo_profile_ya(vk_id):
    return vk_client.get_photos(vk_id)


def vk_photo_albums_ya(vk_id):
    return vk_client.get_album_photos(vk_id)


def vk_photo_profile_gd(vk_id):
    return vk_client.get_photos_to_gdrive(vk_id)


def vk_photo_albums_gd(vk_id):
    return vk_client.get_photos_from_albums_gdrive(vk_id)


def copy_photo():
    print("""С помощью этой функции можно сохранять фотографии из Вконтакте на Яндекс.Диск или Google.Drive по выбору.
    Существуют следующие опции:
    1. Скачать фото Профиля ВК на Яндекс.Диск;
    2. Скачать фото из альбомов ВК на Яндекс.Диск;
    3. Скачать фото Профиля ВК на Google.Drive;
    4. Скачать фото из альбомов на Google.Drive.
    5. Выйти
    """)
    vk_id = int(input('Введите id профиля ВК для скачивания фото: '))
    while True:
        comand = input("Выберите опцию: ")
        if comand == '1':
            vk_photo_profile_ya(vk_id)
        elif comand == '2':
            vk_photo_albums_ya(vk_id)
        elif comand == '3':
            vk_photo_profile_gd(vk_id)
        elif comand == '4':
            vk_photo_albums_gd(vk_id)
        elif comand == '5':
            print("Выход")
            return


if __name__ == "__main__":
    copy_photo()


# vk_id = str(input('Введите vk_id для сохранения фотографий: '))
# vk_client = VkUser(token, '5.131')
# pprint(vk_client.get_photos('1089625'))
# vk_client.get_photos('1089625')
# vk_client.get_albums('1089625')
# vk_client.get_photos_from_albums("1089625")
# vk_client.get_album_photos('1089625')
# vk_client.get_photos_to_gdrive('1089625')

# 1089625
