import requests
from PIL import Image

class QuantumMessagingAPI:
    def __init__(self, webhook_url, key, proxies=None):
        self.webhook_url = webhook_url
        self.proxies = proxies
        self.key = key

    def send_text_message(self, content):
        payload = {
            "type": "text",
            "textMsg": {
                "content": content
            }
        }
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                proxies=self.proxies if self.proxies else None,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def send_text_message_with_mention(self, content, mentioned_type=1, mentionlist=None):
        payload = {}
        if mentioned_type == 1:
            payload = {
                "type": "text",
                "textMsg": {
                    "content": content,
                    "isMentioned": "true",
                    "mentionType": mentioned_type,
                },
            }
        else:
            payload = {
                "type": "text",
                "textMsg": {
                    "content": content,
                    "isMentioned": "true",
                    "mentionType": mentioned_type,
                    "mentionedMobileList": [i for i in mentionlist],
                },
            }
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                proxies=self.proxies if self.proxies else None,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def send_image_message(self, file_path):
        upload_response = self.upload_file(file_path, 1, proxies=self.proxies)
        if "data" not in upload_response or not upload_response.get("data"):
            return {"error": "Failed to upload image. Server response: " + str(upload_response)}
        file_id = upload_response["data"]["id"]
        try:
            with Image.open(file_path) as img:
                width, height = img.size
        except Exception as e:
            return {"error": f"Failed to open image file: {str(e)}"}
        payload = {
            "type": "image",
            "imageMsg": {"fileId": file_id, "height": height, "width": width},
        }
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                proxies=self.proxies if self.proxies else None,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def send_file_message(self, file_path):
        try:
            response = self.upload_file(file_path, 2, proxies=self.proxies)
            fileId = response['content']['id']
            payload = {
                "type": "file",
                "fileMsg": {'fileId': fileId}
            }
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                proxies=self.proxies if self.proxies else None,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def send_news_message(self, title, description, url, pic_url):
        payload = {
            "type": "news",
            "news": {
                "info": {
                    "title": title,
                    "description": description,
                    "url": url,
                    "picUrl": pic_url,
                }
            },
        }
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                proxies=self.proxies if self.proxies else None,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def upload_file(self, file_path, file_type, proxies=None):
        url = f"https://imtwo.zdxlz.com/im-external/v1/webhook/upload-attachment?key={self.key}&type={file_type}"
        files = {"file": (file_path, open(file_path, "rb"), "*/*")}
        try:
            response = requests.post(
                url,
                files=files,
                proxies=proxies if proxies else None,
                verify=True,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
