import vk
import random
import config


class VKClient:

    def __init__(self, access_token):
        self.api = vk.API(
            access_token=access_token,
            v='5.101',
            lang='ru',
            timeout=10
        )

    def __get_wall(self, owner_id):
        try:
            data = self.api.wall.get(
                owner_id=-abs(owner_id),
                count=100,
                filter='owner'
            )
        except vk.exceptions.VkAPIError:
            return
        return data['items']

    def get_group_profile(self, group_id):
        try:
            data = self.api.groups.getById(
                group_id=abs(group_id),
            )
        except vk.exceptions.VkAPIError:
            return
        return data[0]

    def __get_good_posts(self, owner_id, after=None):
        posts = self.__get_wall(owner_id)
        good_posts = []

        for post in posts:

            # Подходящая дата
            if after and after >= post['date']:
                continue

            # Обычный пост
            if post['post_type'] != 'post':
                continue

            # Точно не репост
            if 'copy_history' in post:
                continue

            # Не реклама
            if post['marked_as_ads'] != 0:
                continue

            # Длина текста менее 2000 символов (чтобы влезло в Discord)
            if len(post['text']) >= 2000:
                continue

            # Если есть вложения
            if 'attachments' in post:

                # Не более двух вложений
                if len(post['attachments']) > 2:
                    continue

                # Если 2 вложения, то только картинка со ссылкой:
                elif len(post['attachments']) == 2:
                    if {post['attachments'][0]['type'], post['attachments'][1]['type']} != {'photo', 'link'}:
                        continue

                # Если 1 вложение, то только картинка или ссылка
                elif len(post['attachments']) == 1:
                    if post['attachments'][0]['type'] not in {'photo', 'link'}:
                        continue

            good_posts.append(post)
        return good_posts

    def get_mostly_liked_post(self, owner_id, after=None):
        good_posts = self.__get_good_posts(owner_id, after=after)
        if good_posts:
            return max(good_posts, key=lambda p: p['likes']['count'])

    def get_random_post(self, owner_id, after=None):
        good_posts = self.__get_good_posts(owner_id, after=after)
        if good_posts:
            return random.choice(good_posts)
