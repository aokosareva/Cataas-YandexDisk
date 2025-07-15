class Image:

    def __init__(self, content, name: str, size: int, mime_type: str):
        self.__content = content
        self.__name = name
        self.__size = size
        self.__ext = mime_type.replace("image/", "")

    def image_filename(self):
        return f"{self.__name}.{self.__ext}"

    def metadata_filename(self):
        return f"{self.__name}.json"

    def size(self):
        return self.__size

    def content(self):
        return self.__content