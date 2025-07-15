from CatassApi import CatassApi
from YandexDiskApi import YandexDiscApi

text = input("Input text for cats:")

filename = "./creds/ya_token"
try:
    cataas = CatassApi()
    image = cataas.load_with_text(text)

    yandexApi = YandexDiscApi(filename)
    yandexApi.upload(image)

    exit(1)
except FileNotFoundError:
    print(f"File {filename} does not find.")
    exit(0)
except RuntimeError as error:
    print(f"Error {error}.")
    exit(0)
