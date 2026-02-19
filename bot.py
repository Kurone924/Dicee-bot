import re
import random
import discord
from discord.ext import commands
import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

DICE_RE = re.compile(r"^\s*(\d+)\s*[dD]\s*(\d+)\s*$")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content
    if content.startswith("$"):
        expr = content[1:]
        m = DICE_RE.match(expr)

        if m:
            x = int(m.group(1))
            y = int(m.group(2))

            rolls = [random.randint(1, y) for _ in range(x)]
            total = sum(rolls)

            await message.channel.send(
f"""{message.author.mention}
{x}d{y}：{rolls}
SUM={total}"""
            )
            return  # ← 有成功擲骰就不要再往下跑

    await bot.process_commands(message)  # ⭐超重要（未來指令會用到）

bot.run(TOKEN)
