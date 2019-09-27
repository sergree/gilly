# Токены ВК и Discord

vk_access_token = 'ВСТАВЬТЕ_VK_ТОКЕН_СЮДА'
discord_token = 'ВСТАВЬТЕ_DISCORD_ТОКЕН_СЮДА'

game_name = 'github.com/sergree'

# Настройки VK -> Discord

vk_to_discord_timeout = 300  # Новый пост из ВК каждые 5 минут (300 секунд)

vk_group_ids = [
    30602036,   # IGM
    31480508,   # Pikabu
    57846937,   # MDK
]

vk_bad_words = {
    -31480508: ['Длиннопост от ', 'Комментарии: ', 'Длиннопост: '],  # Удаляем лишний текст из постов Пикабу
}

vk_to_discord_channel_id = 600000000000000000

vk_embed_footer = 'Gilly by Sergree: https://github.com/sergree/gilly'

# Настройки Discord -> Discord

discord_channel_ids = [
    500000000000000000,
]

discord_bad_words = [
    '@here',
    '@everyone'
]

discord_urls = {
    267624335836053506: 'https://discord.gg/python',
}

discord_to_discord_channel_id = 600000000000000001

# Настройки Embed

embed_color = 0x002568

