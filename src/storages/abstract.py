from src.test.test import TestResult, Test
from abc import ABCMeta, abstractmethod


class AbstractStorage(metaclass=ABCMeta):
    _instance = None

    defaults = dict()

    @classmethod
    def singleton(cls):
        if cls._instance is None:
            cls._instance = cls.create_singleton()
            cls._instance.init_default()
        return cls._instance

    @classmethod
    @abstractmethod
    def create_singleton(cls):
        pass

    def init_default(self):
        for key, value in getattr(self, "defaults", dict()).items():
            self.set_value(key, value)

    def set_value(self, key, value):
        setattr(self, key, value)

    def value(self, key):
        return getattr(self, key)


if __name__ == "__main__":
    def test_persistance():
        class UniversalStorage(AbstractStorage):
            @classmethod
            def create_singleton(cls):
                return UniversalStorage()

        UniversalStorage.singleton().set_value("key", 80)
        return TestResult(UniversalStorage.singleton().value("key") == 80)


    def test_custom_storage():
        class TestStorage(AbstractStorage):
            defaults = {
                "item": 50
            }

            @classmethod
            def create_singleton(cls):
                return TestStorage()

        return TestResult(TestStorage.singleton().value("item") == 50)


    test = Test()
    test.add_test(test_persistance)
    test.add_test(test_custom_storage)
    test.run()
