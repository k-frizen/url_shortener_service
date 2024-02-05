import json
import random
import string

from models import *


class Shortener:
    """Class provides features to operate with URLs: generating, updating and extracting"""
    _instance = None

    __URLS_JSON = 'urls.json'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Shortener, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        create_table()

    def __set_mapping(self) -> None:
        """Launch set up mapping with shorten URLs"""
        # todo remove
        import os
        if os.path.exists(self.__URLS_JSON):
            with open(self.__URLS_JSON, 'r') as file:
                self.url_mapping = json.load(file)
        else:
            self.url_mapping = {}

    def update_urls_mapping_file(self) -> None:
        """Upload changed data into the storage file"""
        with open(self.__URLS_JSON, 'w') as file:
            json.dump(self.url_mapping, file)

    def create_short_url(self, original_url: str) -> str:
        """Generate unique short url and insert it into the urls storage.

        :param original_url: url must be converted
        :return: shorten unique URL"""
        short_code = self.generate_short_code()
        while short_code in self.url_mapping:
            short_code = self.generate_short_code()
        insert_short_url(short_code, original_url)
        return short_code

    def delete_short_url(self, short_code: str) -> None:
        """Remove short url from the storage

        :param short_code: code to identify url
        :raise ValueError: in case of given code doesn't exist"""
        # delete_url(short_code)
        # todo check if short_code doesn't exist in the db
        if short_code not in self.url_mapping:
            raise ValueError("Short URL not found")
        del self.url_mapping[short_code]
        self.update_urls_mapping_file()

    def get_redirect_info(self, short_code: str) -> str | None:
        """Extract redirect data

        :param short_code: code to identify url"""
        if short_code in self.url_mapping:
            return self.url_mapping[short_code]

    @staticmethod
    def generate_short_code(length: int = 6) -> str:
        """Create unique short code to identify URL

        :param length: amount of symbols in the result code"""
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
