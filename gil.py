import discord
import config
import datetime
from vk_client import VKClient
from embed_preparer import prepare_embed_from_vk, prepare_embed_from_discord
from storage import Storage
import asyncio
from tprint import log


class GillyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vk_to_discord_channel = None
        self.discord_to_discord_channel = None
        self.vk = self.loop.create_task(self.vk_task())

    @staticmethod
    async def set_thumbs(message):
        for reaction in ['👍', '👎']:
            await asyncio.sleep(0.1)
            await message.add_reaction(reaction)

    async def send_embed_from_vk(self, post, group_profile):
        embed = prepare_embed_from_vk(post, group_profile)
        sent = await self.vk_to_discord_channel.send(embed=embed)
        await self.set_thumbs(sent)

    @staticmethod
    async def get_vk_data(send_method):
        with Storage(config.vk_group_ids) as s:
            for _ in config.vk_group_ids:
                oldest_group, after = s.get_next()
                v_cli = VKClient(config.vk_access_token)
                post = v_cli.get_mostly_liked_post(oldest_group, after=after)
                if post:
                    group_profile = v_cli.get_group_profile(oldest_group)
                    await send_method(post, group_profile)
                    s.set_after(oldest_group, post['date'])
                    return
                else:
                    s.set_after(oldest_group, datetime.datetime.now().timestamp())
                    log('Отсутствуют новые подходящие посты:', oldest_group)

    async def send_embed_from_discord(self, message):
        embed = prepare_embed_from_discord(message)
        await self.discord_to_discord_channel.send(embed=embed)

    async def set_game(self):
        activity = discord.Activity(name=config.game_name, type=discord.ActivityType.listening)
        await self.change_presence(activity=activity, status=discord.Status.online)

    async def on_ready(self):
        log('Вошёл под', self.user)
        self.vk_to_discord_channel = self.get_channel(config.vk_to_discord_channel_id)
        self.discord_to_discord_channel = self.get_channel(config.discord_to_discord_channel_id)
        await self.set_game()

    async def vk_task(self):
        await self.wait_until_ready()
        await asyncio.sleep(5)
        while not self.is_closed():
            try:
                await self.get_vk_data(self.send_embed_from_vk)
            except Exception as e:
                log(e)
            await asyncio.sleep(config.vk_to_discord_timeout)

    async def on_message(self, message):
        await self.wait_until_ready()
        if message.channel.id not in config.discord_channel_ids:
            return
        if self.user == message.author:
            return
        await self.send_embed_from_discord(message)


client = GillyClient()
client.run(config.discord_token)
