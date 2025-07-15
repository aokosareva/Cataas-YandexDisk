import requests

from Image import Image


class CatassApi:
    base_url = 'https://cataas.com'

    def load_with_text(self, text: str) -> Image:
        url = f"{self.base_url}/cat/says/{text}"

        response = requests.get(url)

        content_type = response.headers.get('Content-Type')
        if not content_type.startswith("image/"):
            raise RuntimeError(f"Unexpected response content-type."
                  f" image/* expected."
                  f" {content_type} given")

        image = Image(
            response.content,
            text,
            int(response.headers.get('Content-Length')),
            response.headers.get('Content-Type')
        )

        return image
