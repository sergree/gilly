import discord
import config


def __construct_embed(title, description, url=None, set_footer=True):
    embed = discord.Embed(
            title=title,
            color=config.embed_color,
            description=description,
            url=url
        )
    if set_footer:
        embed.set_footer(text=config.vk_embed_footer)
    return embed


# Убираем лишний текст из различных постов
def __vk_text_fix(post):
    text = post['text']
    if post['owner_id'] in config.vk_bad_words:  # Нерабочие ссылки Пикабу
        for bad in config.vk_bad_words[post['owner_id']]:
            if bad in text:
                return text.split(bad)[0]
    return text


# Убираем @here @everyone
def __discord_text_fix(text):
    for bad_word in config.discord_bad_words:
        text = text.replace(bad_word, '')
    return text.strip()


def prepare_embed_from_vk(post, group_profile):

    text = __vk_text_fix(post)

    link = None
    photo = None

    if 'attachments' in post:
        for attachment in post['attachments']:
            if attachment['type'] == 'link':
                link = attachment['link']
            if attachment['type'] == 'photo':
                photo = attachment['photo']
                sizes = len(photo['sizes'])
                photo = photo['sizes'][sizes - 1]['url']

    if link:
        embed = __construct_embed(
            link['title'],
            text if text else link['description'],
            link['url']
        )
    else:
        embed = __construct_embed(
            group_profile['name'],
            text
        )

    embed.set_thumbnail(url=group_profile['photo_200'])
    embed.set_author(
        name=group_profile['name'],
        icon_url=group_profile['photo_200'],
        url='https://vk.com/' + group_profile['screen_name']
    )

    if photo:
        embed.set_image(url=photo)

    return embed


def prepare_embed_from_discord(message):

    text = __discord_text_fix(message.content)

    embed = __construct_embed(
        message.guild.name,
        text,
        config.discord_urls.get(message.guild.id),
        set_footer=False
    )

    embed.set_thumbnail(url=str(message.guild.icon_url))
    embed.set_author(
        name=message.author.display_name,
        icon_url=str(message.author.avatar_url)
    )

    return embed
