from CatassApi import CatassApi
from YandexDiskApi import YandexDiscApi

text = input("Input text for cats:")

filename = "./creds/ya_token"
try:
    cataasApi = CatassApi()
    image = cataasApi.load_with_text(text)

    yandexApi = YandexDiscApi(filename)
    yandexApi.upload(image)

    print(f"Cat image with text \"{text}\" successfully uploadede on yandex disk.")
    exit(1)
except FileNotFoundError:
    print(f"File {filename} does not find.")
    exit(0)
except RuntimeError as error:
    print(f"Error {error}.")
    exit(0)
