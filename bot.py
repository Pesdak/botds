import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Webhook,  AsyncWebhookAdapter
import aiohttp
import asyncio
import os
import time
import vk_api

webhook_url = os.environ.get('WEBHOOK')
login = os.environ.get('LOGIN')
password = os.environ.get('PASSWORD')
token = os.environ.get('BOT_TOKEN')

vk = vk_api.VkApi(login = login, password = password)
vk.auth()

Bot = commands.Bot(command_prefix='/')
Bot.remove_command('help')

@Bot.event
async def on_ready():
	print('Бот в онлайне!')
	game = discord.Game(r"Insiders")    
	await Bot.change_presence(status=discord.Status.idle, activity=game)

	ag = 0
	while True:
		newsfeed = vk.method('newsfeed.get', {'count': 1,'source_ids': -153688326})
		if ag != newsfeed['items'][0]['post_id']:
			ag = newsfeed['items'][0]['post_id']
			text = newsfeed['items'][0]['text']
			try:
				url = newsfeed['items'][0]['attachments'][0]['photo']['sizes'][7]['url']
				async with aiohttp.ClientSession()  as session: 
					webhook =  Webhook.from_url(webhook_url,  adapter= AsyncWebhookAdapter(session))
					emb = discord.Embed(title='Инсайды', description=f'{text}', colour=0xc28411)
					emb.set_image(url=f'{url}')
					emb.set_footer(text=webhook.created_at.today().strftime("%d.%B.%Y %X"))
					await webhook.send(embed= emb,  username= 'Insiders')
			except KeyError:
				async with aiohttp.ClientSession()  as session: 
					webhook =  Webhook.from_url(webhook_url,  adapter= AsyncWebhookAdapter(session))
					emb = discord.Embed(title='Инсайды', description=f'{text}', colour=0xc28411)
					emb.set_footer(text=webhook.created_at.today().strftime("%d.%B.%Y %X"))
					await webhook.send(embed= emb,  username= 'Insiders')

Bot.run(str(token))
