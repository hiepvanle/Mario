from src.storages.abstract import AbstractStorage
from src.utils import load_image


class ImagesStorage(AbstractStorage):
    defaults = {
        'wall': load_image('box.png', prefix=r"..\..\data"),
        'empty': load_image('grass.png', prefix=r"..\..\data"),
        'player': load_image('mario.png', prefix=r"..\..\data"),
    }

    @classmethod
    def create_singleton(cls):
        return ImagesStorage()