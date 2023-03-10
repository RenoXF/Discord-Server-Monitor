import discord
from discord.ext import commands,tasks
from datetime import datetime
import os
import psutil
import netifaces as ni

#discord requires this to run
intents = discord.Intents.all()
intents.members = True

#insert bot token 
TOKEN = 'Your Token here'
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']  ##select network interface
current_dateTime = datetime.now()

#command prefix is what you use to run the command
#ex:?hello
bot = commands.Bot(command_prefix='?', intents=intents) 

@tasks.loop(minutes=1)
async def autoping():
    modmail_channel = await bot.fetch_channel('Channel ID Here')                         ##change xxx below with your bot client id
    embed = discord.Embed(title=f"{bot.user}",url="https://discord.com/api/oauth2/authorize?client_id=xxxxxxxxx&permissions=8&scope=bot%20applications.commands", description="Discord Server Monitor", color=0x00aaff)
    embed.add_field(name="Latency",value=f"{round(bot.latency * 1000)}ms")
    embed.add_field(name="CPU",value=f"{psutil.cpu_percent()}%")
    embed.add_field(name="RAM",value=f"{psutil.virtual_memory().percent}%")
    embed.add_field(name="Disk",value=f"{psutil.disk_usage('/').percent}%")
    embed.add_field(name="IP Address",value=f"{ip}")
    embed.set_footer(text=f'Time : {current_dateTime.hour}:{current_dateTime.minute} -- {current_dateTime.day}/{current_dateTime.month}/{current_dateTime.year}')
    await modmail_channel.send(embed=embed)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')
    autoping.start()

bot.run(TOKEN)
