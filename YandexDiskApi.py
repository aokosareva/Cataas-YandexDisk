import json
import requests

from Image import Image


class YandexDiscApi:
    base_url = 'https://cloud-api.yandex.net/v1/disk'
    base_dir = 'SPD-126'

    def __init__(self, token_filename: str):
        self.__load_token(token_filename)

    def __load_token(self, token_filename: str):
        file = open(token_filename)
        token = file.readline()
        file.close()

        self.__token = token

    def __make_dir_url(self) -> str:
        return f"{self.base_url}/resources"

    def __uploading_url(self) -> str:
        return f"{self.base_url}/resources/upload"

    def __headers(self, headers=None) -> dict:
        if headers is None:
            headers = {}

        headers['Authorization'] = f"OAuth {self.__token}"

        return headers

    def __make_dir(self, dirname: str):
        headers = self.__headers({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        parameters = {
            "path": dirname,
        }

        response = requests.put(
            self.__make_dir_url(),
            headers=headers,
            params=parameters)

        if (response.status_code not in [201, 409]):
            raise RuntimeError(
                f"Error while creating dir {dirname}."
                f"StatusCode: {response.status_code}, Error:{response.text}")

        return True

    def __link_for_upload(self, filename: str):
        self.__make_dir(self.base_dir)

        parameters = {
            "path": f"{self.base_dir}/{filename}",
        }

        response = requests.get(
            self.__uploading_url(),
            headers=self.__headers(),
            params=parameters)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error while getting link for upload {filename}."
                f"StatusCode: {response.status_code}, Error:{response.text}")

        return response.json()["href"]

    def __uploadImage(self, image: Image):
        upload_url = self.__link_for_upload(image.image_filename())

        response = requests.put(upload_url, files={"file": image.content()})
        if response.status_code != 201:
            raise RuntimeError(
                f"Error while uploading {image.image_filename()}."
                f"StatusCode: {response.status_code}, Error:{response.text}")

    def __uploadMetadata(self, image: Image):
        upload_url = self.__link_for_upload(image.metadata_filename())
        payload = {
            "size": image.size()
        }
        headers = self.__headers({
            "Content-Type": "application/json",
        })

        response = requests.put(upload_url, headers=headers, data=json.dumps(payload))

        if response.status_code != 201:
            raise RuntimeError(
                f"Error while uploading {image.metadata_filename()}."
                f"StatusCode: {response.status_code}, Error:{response.text}")

    def upload(self, image: Image):
        self.__uploadImage(image)
        self.__uploadMetadata(image)
