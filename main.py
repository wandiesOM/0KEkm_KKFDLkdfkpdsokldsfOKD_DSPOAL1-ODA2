import discord
from discord.ext import commands, tasks
import asyncio
import random
import g4f
import os

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

CHAT_CHANNEL_ID = 1471445681846878365
WELCOME_CHANNEL_ID = 1471445681846878365
BAD_WORDS = ['пидр', 'негр', 'пидорас', 'гандон' , 'пидорас' , 'нигга' , 'негрище' , 'nigga' , 'negr' , 'pidoras' , 'pidor']

LIGHT_BLUE = 0x3D839C
DOCS_URL = "https://i.pinimg.com/originals/2c/92/4f/2c924f5738ab7e80986cc8ff0290714a.gif"

@tasks.loop(hours=2, minutes=1)
async def bump_reminder():
    channel = bot.get_channel(CHAT_CHANNEL_ID)
    if channel:
        role_mention = "<@&1473629581222219839>" 
        
        embed = discord.Embed(
            title="🚀 время поднять сервер :3!",
            url=DOCS_URL,
            description="Напишите **/bump**, пожалуйста чтобы поднять сервер в топ Dishboard :3",
            color=0xFFAC33
        )
        await channel.send(content=role_mention, embed=embed)

@bot.event
async def on_ready():
    if not bump_reminder.is_running():
        bump_reminder.start()
    
    channel = bot.get_channel(CHAT_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="✨ System Status: Online", url=DOCS_URL, description="**бот начал работу :D**", color=LIGHT_BLUE)
        embed.set_image(url="https://i.pinimg.com/originals/2c/92/4f/2c924f5738ab7e80986cc8ff0290714a.gif")
        await channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="👋 Приветствуем!", url=DOCS_URL, description=f"{member.mention}, добро пожаловать на сервер!", color=LIGHT_BLUE)
        embed.set_image(url="https://i.pinimg.com/originals/2c/92/4f/2c924f5738ab7e80986cc8ff0290714a.gif")
        await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot or message.guild is None:
        return

    content = message.content.lower()
    if any(word in content for word in BAD_WORDS):
        await message.delete()
        embed = discord.Embed(description=f"{message.author.mention}, вы написали запретное слово! пожалуйста больше так не делайте :3", color=LIGHT_BLUE)
        embed.set_image(url="https://cdn-icons-gif.flaticon.com/12132/12132907.gif")
        await message.channel.send(embed=embed, delete_after=100000)
        return

    await bot.process_commands(message)

@bot.command()
async def ai(ctx, *, question):
    async with ctx.typing():
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[{"role": "user", "content": question}],
            )
            
            if response:
                if len(response) > 2000:
                    response = response[:1997] + "..."
                embed = discord.Embed(title="🤖 Ответ ИИ", url=DOCS_URL, description=response, color=LIGHT_BLUE)
                await ctx.reply(embed=embed)
            else:
                await ctx.send("бля чёт херня какая то зови @ferfi я пофикшу")
        except Exception:
            await ctx.send("бля чёт херня какая то зови @ferfi я пофикшу")

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="📜 Список доступных команд", url=DOCS_URL, color=LIGHT_BLUE)
    embed.add_field(name="Общее", value="`/info`, `/avatar`, `/commands`", inline=False)
    embed.add_field(name="Фан", value="`/roll`, `/coin`, `/ball`, `/hug`", inline=False)
    embed.add_field(name="нееронка", value="`/ai <вопрос>`", inline=False)
    await ctx.send(embed=embed, delete_after=40)

@bot.command()
async def ball(ctx, *, question):
    responses = ["Беc порно :C", "ты умрёшь и т.д", "хз", "да", "неа"]
    embed = discord.Embed(title="🔮 Магический шар", url=DOCS_URL, description=f"**Вопрос:** {question}\n**Ответ:** {random.choice(responses)}", color=LIGHT_BLUE)
    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(description=f"{ctx.author.mention} обнял {member.mention}! 🤗", color=LIGHT_BLUE)
    embed.set_image(url="https://i.pinimg.com/originals/b9/c7/11/b9c711e03a47d4744226b372b3140016.gif")
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, limit: int = 100):
    embed = discord.Embed(description=f"🎲 Выпало число: **{random.randint(1, limit)}**", color=LIGHT_BLUE)
    await ctx.send(embed=embed)

@bot.command()
async def coin(ctx):
    res = random.choice(["Орёл", "Решка"])
    embed = discord.Embed(description=f"🪙 Монетка показала: **{res}**", color=LIGHT_BLUE)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ Аватар {member.name}", url=DOCS_URL, color=LIGHT_BLUE)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="ℹ️ Информация", url=DOCS_URL, description="этот бот был создан @randomguyl3 для его собственного наикрутейщего сервера , наслаждайтесь", color=LIGHT_BLUE))

import os
token = os.getenv('BOT_TOKEN')
bot.run(token)
