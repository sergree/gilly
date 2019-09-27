import pickle
from collections import OrderedDict


class Data:

    def __init__(self):
        self.group_ids = OrderedDict()
        self.cursor = 0

    def prepare(self, vk_group_ids):
        for group_id in vk_group_ids:
            if group_id not in self.group_ids:
                self.group_ids[group_id] = 0
        for group_id in list(self.group_ids.keys()):
            if group_id not in vk_group_ids:
                del self.group_ids[group_id]
        self.cursor = self.cursor % len(self.group_ids)


class Storage:

    def __init__(self, vk_group_ids):
        self.__data = None
        self.__vk_group_ids = vk_group_ids

    def __enter__(self):
        self.__load()
        self.__data.prepare(self.__vk_group_ids)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save()

    def __load(self):
        try:
            with open('data.pickle', 'rb') as f:
                self.__data = pickle.load(f)
        except FileNotFoundError:
            self.__data = Data()

    def __save(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.__data, f)

    def get_next(self):
        data = tuple(self.__data.group_ids.items())[self.__data.cursor]
        self.__data.cursor = (self.__data.cursor + 1) % len(self.__data.group_ids)
        return data[0], data[1]

    def set_after(self, group_id, value):
        self.__data.group_ids[group_id] = value
