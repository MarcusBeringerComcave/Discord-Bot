# #####################################################################################
#   bot.py
# #####################################################################################
#  imports
# ##################
import os                                           #  import operating system
import random                                       #  import random function

import discord                                      #  import discord api
import googletrans                                  #  import googletrans api
import asyncio                                      #  import asyncrone function for async/await syntax

from dotenv import load_dotenv                      #  import load_dotenv function from dotenv api
from discord.ext import commands                    #  import commands function from dotenv api
from googletrans import Translator                  #  import load_dotenv function from dotenv api

load_dotenv()                                       #  start load_dotenv function
TOKEN = os.getenv('DISCORD_TOKEN')                  #  get bot token with getenv
GUILD = os.getenv('DISCORD_GUILD')                  #  get guild name with getenv

description = '''Comcave Collage Lernpfad'''        #  set description for bot

intents = discord.Intents.default()                 #  set intents from discrod api th handle permissions
intents.members = True                              #  "
intents.message_content = True                      #  "

client = discord.Client(command_prefix = ['!', '?'], description = description, intents = intents)  #  set the bot as var client
client = commands.Bot(command_prefix = ['!', '?'], description = description, intents = intents)    #  set the bot commands as var client
client.remove_command('help')                                                                       #  remove default help message function

translator = Translator()                           #  import the translator function into var
# #####################################################################################
#  ready
# #####################################################################################
@client.event                                                                                   #  declare an event
async def on_ready():                                                                           #  set the on ready event for the bot (if bot is ready)
    print('{} ({}) is ready'.format(client.user.name, client.user.id))                          #  set the printout, when bot is connected
    await client.change_presence(activity = discord.Game(name = 'an sich rum', type = 1))       #  set status of the bot
# #####################################################################################
#  member join
# #####################################################################################
@client.event                                                                                   #  declare an event
async def on_member_join(user):                                                                 #  set the on member join event for the bot (if a new member is joining first time)
    print(user)                                                                                 #  set the printout, when user is connected
    await user.create_dm()                                                                      #  create a direct message event and send a message as pm to user when login the first time
    await user.dm_channel.send(f'{user.mention}\n```Willkommen bei den Comcavlern\n\nAls erstes schau Dir die Hilfe an, damit Du wießt, was Du hier alles machen kannst.\nDie Hilfe kannst Du Dir jederzeit mit "!hilfe" anzeigen lassen\n\nDu kannst Dich in Deine Gruppen eintragen mit den Befehlen:\n\n　　　　!standort DEIN STANDORT\n　　　　　　　　Um Deine Gruppe deines Standortes zu betreten\n　　　　　　　　Bsp.: !standort Karlsruhe\n\n　　　　!fach DEIN FACHGEBIET\n　　　　　　　　Um Deine Gruppe deines Fachgebiets zu betreten\n　　　　　　　　Bsp.: !fach Anwendungsentwicklung\n```')
# #####################################################################################
#  messages event
# #####################################################################################
@client.event                                                                                   #  declare an event
async def on_message(message):                                                                  #  set the on message event for the bot (if a member writes an message on the server)
    # getting messages from bot pm
    user = message.author                                                                       #  get the user who wrote the message
    if user == client.user:                                                                     #  if the wirte is the bot itself, then exit this function
        return                                                                                  #  the exit point
    if isinstance(message.channel, discord.DMChannel):                                          #  get just meessages when a user answer a bots private message
        if not message.content.startswith('!'):                                                 #  just get messages without a command prfix
            admin = await client.fetch_user(762078856659730482)                                 #  set a specified user as admin for respond
            await admin.create_dm()                                                             #  create a direct message event and send message as pm to the admin
            await admin.dm_channel.send(f'{user.mention} hat folgendes auf den Bot geantwortet:\n```{message.content}```')
        if message.content.startswith('!'):                                                     #  just get messages with a command prfix
            await user.create_dm()                                                              #  create a direct message event and send message as pm to the user that commands only work at the server
            await user.dm_channel.send(f'{user.mention}:\n```Diese Befehle gehen natürlich nur auf dem Server,\negal in welchem Channel, aber NUR auf dem Server,\nnicht als Privat Nachricht beim Bot```')
    await client.process_commands(message)                                                      #  free the message event var, otherwise the bot commands ar not working
# #####################################################################################
#  client commands
# #####################################################################################
#  warn unregistered users with a pm
@client.command(pass_context = True, aliases = ['warn'])                        #  create a command with alias (useage: !warn)
@commands.has_role('Administrator')                                             #  check role of the user, command only allowed for specified role, in this case Administrator
async def warnunregistered(ctx):                                                #  defining function
    guild = ctx.guild                                                           #  get the guild from where the user is wrinting for content using
    for user in guild.members:                                                  #  for every user in this guild
        if len(user.roles) == 1:                                                #  check if user just have the everyone role
            await user.create_dm()                                              #  create a direct message event and send message as pm to the user to set groups and roles to himself
            await user.dm_channel.send(f'{user.mention}\n```Ich hoffe Du kannst einen positiven Nutzen aus unserem Server ziehen.\n\nLeider hast Du Dich bis lang noch nicht zu einer Gruppe geaddet,\ndamit man sehen kann was Du machst und wo Du lernst.\nEs hilft allen, wenn Du das bitte machen würdest.\n\nDu kannst Dich auf unserem Server in Deine Gruppen eintragen mit den Befehlen:\n\n　　　　!standort DEIN STANDORT\n　　　　　　　　Um Deine Gruppe deines Standortes zu betreten\n　　　　　　　　Bsp.: !standort Karlsruhe\n\n　　　　!fach DEIN FACHGEBIET\n　　　　　　　　Um Deine Gruppe deines Fachgebiets zu betreten\n　　　　　　　　Bsp.: !fach Anwendungsentwicklung\n\nSchau Dir die gern auch die Hilfe an, damit Du wießt, was Du hier alles machen kannst.\nDie Hilfe kannst Du Dir jederzeit mit "!hilfe" anzeigen lassen\n```')
#  list unregistered users
@client.command(pass_context = True, aliases = ['list'])                        #  create a command with alias (useage: !list)
@commands.has_role('Administrator')                                             #  check role of the user, command only allowed for specified role, in this case Administrator
async def listunregistered(ctx):                                                #  defining function
    guild = ctx.guild                                                           #  get the guild from where the user is wrinting for content using
    await ctx.send(f'Nutzer ohne Rollen:')                                      #  headline for the channel message
    for user in guild.members:                                                  #  for every user in this guild
        if len(user.roles) == 1:                                                #  check if user just have the everyone role
            await ctx.send(f'{user.name}#{user.discriminator}\n')               #  write down all users with only the everyone role
#  ask user for issues
@client.command(pass_context = True, aliases = ['ask'])                         #  create a command with alias (useage: !ask)
@commands.has_role('Administrator')                                             #  check role of the user, command only allowed for specified role, in this case Administrator
async def askissues(ctx):                                                      #  defining function
    guild = ctx.guild                                                           #  get the guild from where the user is wrinting for content using
    user = ctx.author                                                           #  get the user who wrote the message
    if user == client.user:                                                     #  if the wirte is the bot itself, then exit this function
        return                                                                  #  the exit point
    for member in guild.members:                                                #  for every user in this guild
        #  check if member is an instance of guild members and if message is not sent to specifies users
        if isinstance(member, discord.Member) and member.name != 'Sandro Simperl' and member.name != 'ComCave' and member.name != 'Bot':
            #  set message
            message = f'{member.mention}\n```Ich hoffe Du kannst einen positiven Nutzen aus unserem Server ziehen.\n\nIch möchte hiermit die Gelegenheit nutzen,\nDich zu fragen ob bis jetzt alles in Ordnung ist.\n\nEs würde mich freuen, wenn Du mir mitteilst, was ich ändern oder anpassen soll.\nIch bin für jede Kritik oder jedes Feedback, dankbar.\n\nDu kannst:\n　　　　direkt antworten\n　　　　dem User "Sandro Simperl#5764" (Tag unten) eine Nachricht senden\n　　　　per Email an "sandrosimperl.cc@outlook.de" eine Nachricht senden\n　　　　oder auf dem Server per Feedback Befehl:\n　　　　　　　　!feedback DEINE MEINUNG\n\nIch danke Dir bereit jetzt für das teilnehmen und Deinen Mühen.\n```\n<@{762078856659730482}>\n'
            try:                                                                #  try sending message
                await member.send(message)
            except discord.Forbidden:                                           #  if not sendable, then send admin a message
                admin = await ctx.bot.fetch_user(762078856659730482)            #  define admin user and sent the message
                await admin.send(f'Fehler: Nachricht konnte nicht an {member.name} gesendet werden.')

#  get a feedback
@client.command(pass_context = True, aliases = ['feedback'])
async def fdbk(ctx, *, message):
    if ctx.author.bot:
        return
    user = ctx.message.author
    userid = ctx.message.author.id
    guild = ctx.guild
    for member in guild.members:
        if member.name == 'Sandro Simperl':
            await member.create_dm()
            await member.dm_channel.send(f'{user.mention} ({userid})hat folgendes Feedback gesendet:\n```{message}```')
# ##################
#  member list
# ##################
@client.command(pass_context = True, aliases = ['m', 'member', 'members'])
async def mem(ctx, role: discord.Role = None):
    for guild in client.guilds:
        if role is None:
            await ctx.send(f'```　　Mitglieder --> ```')
            for member in guild.members:
                if not member.bot:
                    await ctx.send(f'　　　{member.mention}')
        else:
            await ctx.send(f'```　　{role.name} --> ```')
            for member in role.members:
                if not member.bot:
                    await ctx.send(f'　　　{member.mention}')
# ##################
#  clear channels
# ##################
@client.command(pass_context = True, aliases = ['p', 'purge', 'clear'])
@commands.has_role('Administrator')
async def prg(ctx, menge: int = None):
    if menge is None:
        await ctx.channel.purge(limit = 9000000)
    else:
        await ctx.channel.purge(limit = menge)
# ##################
#  show help
# ##################
#  show help
@client.command(pass_context = True, aliases = ['h', 'help', 'hilfe', 'bot'])
async def hlp(ctx):
    embed = discord.Embed(title = 'Server', description = 'Bot prefix ist ? oder !\nAlle Befehle auch in Englisch funktional\n', color = 0xcc4636)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Hilfe', value = f'\n!hilfe\n　　Zeigt diese Hilfe an\n\n!hilfmir\n　　Schickt diese Hilfe als PM an Dich', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Aktionen', value = f'\n!standort ***dein Standort***\n　　Fügt Dich zur Gruppe Deines Standortes hinzu\n　　　　Bsp.: !standort Karlsruhe\n　　　　Bsp.: !standort München\n\n!fach ***dein Fach***\n　　Fügt Dich zur Gruppe Deines Ausbildungsfaches hinzu\n　　　　Bsp.: !fach Anwendungsentwicklung\n　　　　Bsp.: !fach Systemintegration', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Informationen', value = f'\n!members\n　　Zeigt eine Liste aller Member an\n\n!members ***dein Standort***\n　　Zeigt eine Liste der Member von deinem Standpunkt\n　　　　Bsp.: !members Karlsruhe\n　　　　Bsp.: !members München\n\n!members ***Gruppe***\n　　Zeigt eine Liste der Member die zu der Gruppe gehören\n　　　　Bsp.: !members Administrator\n　　　　Bsp.: !members Anwendungsentwicklung', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Übersetzungen', value = f'\n!**lang** ***text***\n　　Übersetzt den eingegebene ***text*** in "**lang**" stehenden Sprache\n　　Nutzbare Sprachen:\n　　　　!de　--> übersetzt nach deutsch\n　　　　!en　--> übersetzt nach englisch\n　　　　!fr　--> übersetzt nach französisch\n　　　　!es　--> übersetzt nach spanisch\n　　　　!ru　--> übersetzt nach russisch\n　　　　!de　--> übersetzt nach Deutsch\n　　　　wenn mehr erwünscht, bitte melden\n　　Beispiele:\n　　　　Bsp.: !de This is a test　　--> Das ist ein Test\n　　　　Bsp.: !en Das ist ein Test　--> This is a test\n　　　　Bsp.: !ru This is a test　　--> Это проверка', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Feedback', value = f'\n!feedback ***nachricht***\n　　Hier kannst Du alles melden, was:\n　　　　nicht funktioniert\n　　　　Dir nicht passt\n　　　　geändert werden sollt\n　　　　Dir am Herzen liegt', inline = False)
    embed.add_field(name = ' ', value = f' ', inline = False)
    embed.set_footer(text = '\nsandrosimperl.cc@outlook.de')
    await ctx.send(embed = embed)
#  send help as pm
@client.command(pass_context = True, aliases = ['hm', 'helpme', 'hilfmir'])
async def hlpme(ctx):
    user = ctx.message.author
    embed = discord.Embed(title = "Server", description = 'Bot prefix ist ? oder !\nAlle Befehle auch in Englisch funktional\n', color = 0xcc4636)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Hilfe', value = f'\n!hilfe\n　　Zeigt diese Hilfe an\n\n!hilfmir\n　　Schickt diese Hilfe als PM an Dich', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Aktionen', value = f'\n!standort ***dein Standort***\n　　Fügt Dich zur Gruppe Deines Standortes hinzu\n　　　　Bsp.: !standort Karlsruhe\n　　　　Bsp.: !standort München\n\n!fach ***dein Fach***\n　　Fügt Dich zur Gruppe Deines Ausbildungsfaches hinzu\n　　　　Bsp.: !fach Anwendungsentwicklung\n　　　　Bsp.: !fach Systemintegration', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Informationen', value = f'\n!members\n　　Zeigt eine Liste aller Member an\n\n!members ***dein Standort***\n　　Zeigt eine Liste der Member von deinem Standpunkt\n　　　　Bsp.: !members Karlsruhe\n　　　　Bsp.: !members München\n\n!members ***Gruppe***\n　　Zeigt eine Liste der Member die zu der Gruppe gehören\n　　　　Bsp.: !members Administrator\n　　　　Bsp.: !members Anwendungsentwicklung', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Übersetzungen', value = f'\n!**lang** ***text***\n　　Übersetzt den eingegebene ***text*** in "**lang**" stehenden Sprache\n　　Nutzbare Sprachen:\n　　　　!de　--> übersetzt nach deutsch\n　　　　!en　--> übersetzt nach englisch\n　　　　!fr　--> übersetzt nach französisch\n　　　　!es　--> übersetzt nach spanisch\n　　　　!ru　--> übersetzt nach russisch\n　　　　!de　--> übersetzt nach Deutsch\n　　　　wenn mehr erwünscht, bitte melden\n　　Beispiele:\n　　　　Bsp.: !de This is a test　　--> Das ist ein Test\n　　　　Bsp.: !en Das ist ein Test　--> This is a test\n　　　　Bsp.: !ru This is a test　　--> Это проверка', inline = False)
    embed.add_field(name = '----------------------------', value = f'', inline = False)
    embed.add_field(name = 'Feedback', value = f'\n!feedback ***nachricht***\n　　Hier kannst Du alles melden, was:\n　　　　nicht funktioniert\n　　　　Dir nicht passt\n　　　　geändert werden sollt\n　　　　Dir am Herzen liegt', inline = False)
    embed.add_field(name = ' ', value = f' ', inline = False)
    embed.set_footer(text = '\nsandrosimperl.cc@outlook.de')
    await user.create_dm()
    await user.dm_channel.send(embed = embed)
# ##################
#  add roles
# ##################
#  add location
@client.command(pass_context = True, aliases = ['standort', 's', 'location', 'loc'])
async def ort(ctx, role: str = None):
    user = ctx.message.author
    if role is None:
        await ctx.send(f'{user.mention}```Du musst schon einen Standort eingeben\nBsp.: !standort Karlsruhe\n```')
    else:
        if role != 'Administrator' and 'Dozent' and 'CC - Bot' and 'Bot':
            role = discord.utils.get(ctx.guild.roles, name = role)
            if role is None:
                await ctx.guild.create_role(name = role)
            if role not in user.roles:
                await discord.Member.add_roles(user, role)
                await ctx.send(f'{user.mention}```Dein Standort wurde für Dich eingetragen```')
            else:
                await ctx.send('Du bist schon in dieser Gruppe drin')
#  add subject
@client.command(pass_context = True, aliases = ['fach', 'f', 'subject', 'sub'])
async def ausbildung(ctx, role: str = None):
    user = ctx.message.author
    if role is None:
        await ctx.send(f'{user.mention}```Du musst schon eine Fachrichtung eingeben\nBsp.: !fach Anwendungsentwicklung\n```')
    else:
        if role != 'Administrator' and 'Dozent' and 'CC - Bot' and 'Bot':
            role = discord.utils.get(ctx.guild.roles, name = role)
            if role is None:
                await ctx.guild.create_role(name = role)
            if role not in user.roles:
                await discord.Member.add_roles(user, role)
                await ctx.send(f'{user.mention}```Dein Fach wurde für Dich eingetragen```')
            else:
                await ctx.send('Du bist schon in dieser Gruppe drin')
# ##################
#  translator
# ##################
#  translator
async def translation(ctx, translate_to, translate_to_flag, message):
    if ctx.author.bot:
        return
    translate_from = translator.detect(message).lang.lower()
    if translate_from == translate_to:
        await ctx.send("Die gleichen Sprache, muss nicht übersetzt werden")
        return
    if translate_from == 'en':
        translate_from_flag = 'us'
    else:
        translate_from_flag = translate_from
    result = translator.translate(message, dest = translate_to)
    translate_message = result.text
    await ctx.send(f':flag_' + translate_from_flag + ': --> :flag_' + translate_to_flag + ': \n' + translate_message)
    
# languages
aliases_dict = {
    'de': 'de',
    'en': 'us',
    'fr': 'fr',
    'es': 'es',
    'ru': 'ru'
}
#  translation
@client.command(pass_context=True, aliases=list(aliases_dict.keys()))
async def translate(ctx, *, message):
    alias = ctx.invoked_with.lower()
    if alias in aliases_dict:
        await translation(ctx, alias, aliases_dict[alias], message)
    else:
        await ctx.send("Ungültiger Alias. Verfügbare Aliase: " + ", ".join(aliases_dict.keys()))

client.run(TOKEN)