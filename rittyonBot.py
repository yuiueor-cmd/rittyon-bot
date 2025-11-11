import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Flaskをバックグラウンドで起動
threading.Thread(target=run_flask).start()
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot has connected as {bot.user}")


@bot.event
async def on_member_join(member):
    guild = member.guild
    admin_role = discord.utils.get(guild.roles, name="管理者")
    bot_member = guild.me

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True),
        admin_role: discord.PermissionOverwrite(view_channel=True),
        bot_member: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    channel_name = f"welcome-{member.name}"
    channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

    await channel.send(
        f"""{member.mention} さん、参加ありがとうございます！🎉

以下の項目を教えてください：

・年齢  
・プラットフォーム  
・最高ランク帯（シーズンまで記載ください）  
・現在のランク帯  
・参加率  

まずはこちら教えてください！"""
    )

    print(f"📁 チャンネル作成: {channel_name}")

    general_channel = discord.utils.get(guild.text_channels, name="一般")
    if general_channel:
        await general_channel.send(
            f"{member.mention} さん、ようこそ！🎉\nこちらのチャンネルで自己紹介をお願いします：\n{channel.mention}"
        )
    else:
        await channel.send("⚠ 一般チャンネルが見つかりませんでした。管理者にご確認ください。")

bot.run(os.getenv("DISCORD_TOKEN"))