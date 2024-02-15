import requests
import discord
import time
from discord import Embed, File
from discord.ext import commands
from utils.secret import botsecret
from utils.twitch import obter_slug, encodar_string

# Configurações básicas
prefix = "!" # prefixo usado para utilizar os comandos do bot
intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True
client = commands.Bot(command_prefix=prefix,  case_insensitive=True, intents=intents)
client.remove_command('ajuda')

# Start notifying in the console.
@client.event
async def on_ready():
	print(f"O bot Tarkov Brasil Cuts está online e funcionando! - {client.user.name}")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="@TarkovBrasilCuts"))

@client.command()
@commands.check(lambda ctx: ctx.channel.id == 1106998521648914432)
async def ajuda(ctx):
	# Comandos disponíveis no bot
    embed = Embed(title="Tarkov Brasil Cuts: envie seus clips pelo Discord!")
    embed.add_field(name="!ajuda", value="Exibe os comandos disponíveis.", inline=False)
    embed.add_field(name="!enviarclip", value="Envia clip para a base de dados.", inline=False)
    # embed.add_field(name='+plataformas', value='Exibe as plataformas que são aceitas pelo projeto Tarkov Brasil Cuts.', inline=False)    
    await ctx.reply(embed=embed, mention_author=True)
    # await ctx.message.delete()

@client.command()
@commands.check(lambda ctx: ctx.channel.id == 1106998521648914432) # id do canal do DS 1106998521648914432 > server de tests 1106411371010211981
async def enviarclip(ctx, *, arg='0'):
	if arg != '0':
		msginput = str(arg)
		if ' ' in msginput:
			clip_link, classificacao = msginput.split(sep=' ', maxsplit=1) # Divide a string no primeiro espaço, separando em link do clip e classificação em tags
			classificacao_encodado = encodar_string(classificacao)
			if obter_slug(clip_link):
				# Prepara o a URL para fazer o POST
				url_envio = f"""https://docs.google.com/forms/u/1/d/e/1FAIpQLSe1nQhJwJUPWteD6KO7DMdpWUa3ZHKQF22Vnh2yKqo1IuOjgA/formResponse?entry.349130113={clip_link}&entry.727576029.other_option_response={classificacao_encodado}&entry.727576029=__other_option__"""
				print(url_envio)
				# Envia dados para o formulário, inserindo o link do clip e as tags
				try:
					requests.post(url_envio)
				except Exception as erro:
					print(erro)			
				
				logs = f"**Clip: ** {clip_link}\n**Tags: ** {classificacao}\n**Enviado por: ** {ctx.author.mention}"
				success = Embed(title=":white_check_mark:   O o seu clip foi enviado com sucesso!", description=logs, color=4564285)
				success.set_footer(text="💜   Obrigado por contribuir com o Tarkov Brasil Cuts!")
				await ctx.reply(embed=success, mention_author=True)
			else:
				print('link inválido')
				logs = f"**Clip: ** {clip_link}\n{ctx.author.mention}, revise o link do clip e utilize o comando novamente!"
				fail = Embed(title=":x:   O envio do clip falhou!", description=logs, color=15548997)
				fail.set_footer(text='⛔️   O link é inválido.')
				await ctx.reply(embed=fail, mention_author=True)
		else:
			if obter_slug(msginput):
				# Prepara o a URL para fazer o POST
				url_envio = f"""https://docs.google.com/forms/u/1/d/e/1FAIpQLSe1nQhJwJUPWteD6KO7DMdpWUa3ZHKQF22Vnh2yKqo1IuOjgA/formResponse?entry.349130113={msginput}"""
				
				# Envia dados para o formulário apenas com o link do clip
				try:
					requests.post(url_envio)
				except Exception as erro:
					print(erro)			
				print('link válido')
				logs = f"**Clip: ** {msginput}\n**Enviado por: ** {ctx.author.mention}"
				success = Embed(title=":white_check_mark:   O o seu clip foi enviado com sucesso!", description=logs, color=4564285)
				success.set_footer(text="💜   Obrigado por contribuir com o Tarkov Brasil Cuts!")
				await ctx.reply(embed=success, mention_author=True)
			else:
				print('link inválido')
				logs = f"**LINK INVÁLIDO**!\n**Clip: ** {msginput}\n{ctx.author.mention}, revise o link do clip e utilize o comando novamente!"
				fail = Embed(title=":x:   O envio do clip falhou!", description=logs, color=15548997)
				fail.set_footer(text='⛔️   O link é inválido.')
				await ctx.reply(embed=fail, mention_author=True)
	else:
		await ctx.reply(f"🚫   {ctx.author.mention}, você precisa enviar um link de clip para que eu possa enviar para a base de dados!", mention_author=True)
	
client.run(botsecret)
