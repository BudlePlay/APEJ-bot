import discord
from discord.ext import commands, tasks
from discord.utils import get
import string
import re
import json
from datetime import datetime, timedelta
import os
import random
import asyncio
import emoji
from dateutil import tz
import dataget


rootname = "data/server"
intents = discord.Intents.all()
tokenfile = open("token.json", "r", encoding="UTF-8")

bot = commands.Bot(command_prefix=["cc!", "CC!"], intents=intents)


@bot.event
async def on_ready():
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("메세지 관리"),
    )
    bot.loop.create_task(job())


async def job():
    while True:

        sendch=bot.get_channel(importdata["channel"])

        sendmsg=dataget.get_chat_data()

        sendmsg=dataget.CheckMessage(sendmsg)


        await sendch.send(sendmsg)

        await asyncio.sleep(5)

testinfo = {}


@bot.event
async def on_member_join(member):

    global testinfo
    testrole = discord.utils.get(member.guild.roles, name="입장테스트")
    await member.add_roles(testrole)

    channel = await member.guild.create_text_channel("입장채널")
    selfbot = discord.utils.get(member.guild.members, id=bot.user.id)
    await channel.set_permissions(member, read_messages=True)
    await channel.set_permissions(selfbot, read_messages=True)
    await channel.set_permissions(member.guild.default_role, read_messages=False)

    testcode = random.sample(string.ascii_lowercase, 10)

    testinfo[str(channel.id)] = {"userid": member.id, "testcode": testcode}

    print(testinfo)

    await channel.send(f"{testinfo[str(channel.id)]['testcode']} 순서대로 채팅")



@bot.event
async def on_message(tempmessage):

    if re.match("[a-z]{1}", tempmessage.content) and len(tempmessage.content) == 1:

        channelid = tempmessage.channel.id
        if str(channelid) in testinfo.keys():
            
            if testinfo[str(channelid)]["testcode"][0] == tempmessage.content and testinfo[str(channelid)]["userid"]==tempmessage.author.id:
                del testinfo[str(channelid)]["testcode"][0]
                print(testinfo[str(channelid)])

                if len(testinfo[str(channelid)]["testcode"]) == 0:
                    testrole = discord.utils.get(tempmessage.guild.roles, name="입장테스트")
                    await tempmessage.author.remove_roles(testrole)
                    del testinfo[str(channelid)]
                    await bot.get_channel(channelid).delete()

    else:
        

        await bot.process_commands(tempmessage)



testcheck = input("test모드 > 'test'입력")

token = ""
importdata=json.load(tokenfile)
if testcheck == "test":
    token = importdata["testtoken"]
else:
    token = importdata["token"]

bot.run(token)
