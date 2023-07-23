from src.storages.images import ImagesStorage
from src.storages.setting import SettingsStorage
from src.storages.world import WorldStorage

images_storage = ImagesStorage.singleton()
settings_storage = SettingsStorage.singleton()
world_storage = WorldStorage.singleton()

storages = [images_storage, settings_storage, world_storage]

for storage in storages:
    for key in storage.defaults:
        globals()[key] = storage.defaults[key]