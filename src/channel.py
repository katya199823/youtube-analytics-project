import os
import json
from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь json в нормальном формате"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        Модифицировали конструктор "Channel"
        """
        self.__channel_id = channel_id
        youtube = self.get_service()
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']


    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        printj(channel)


    def to_json(self, file_name):
        """
        Метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.__dict__, file, indent=4, ensure_ascii=False)


    @classmethod
    def get_service(cls):
        """
        Класс-метод `get_service()`, возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        return youtube

