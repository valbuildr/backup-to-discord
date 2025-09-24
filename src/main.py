import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from logging import getLogger
import shutil
from datetime import datetime
import hashlib

load_dotenv()

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

log = getLogger("discord.fansbot")

if not os.path.exists("src/backups"):
    os.makedirs("src/backups")


def hash_file(filepath):
    sha256_hash = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None


@tasks.loop(hours=24)
async def backup_world():
    log.info("Backing up...")

    if not os.path.exists(os.getenv("BACKUP_DIR")):
        raise Exception("The specified path does not exist.")

    name = f"src/backups/backup@{int(datetime.now().timestamp())}"

    if os.getenv("CLEAR_BACKUP_DIR").lower() == "true":
        for item in os.listdir("src/backups"):
            item_path = os.path.join("src/backups", item)
            try:
                os.remove(item_path)
            except OSError as e:
                pass

    shutil.make_archive(name, "zip", os.getenv("BACKUP_DIR"))
    h = hash_file(name + ".zip")

    channel = await bot.fetch_channel(os.getenv("CHANNEL_ID"))

    if channel:
        messages = [message async for message in channel.history(limit=1)]
        last_message = messages[0] if messages else None

        prev_h = None

        if (
            last_message
            and last_message.author.id == bot.user.id
            and last_message.content.startswith("SHA256 Hash: `")
        ):
            prev_h = last_message.content.replace("`", "").replace("SHA256 Hash: ", "")
            print(prev_h)

        if h != prev_h:
            async with channel.typing():
                await channel.send(
                    content=f"SHA256 Hash: `{h}`", file=discord.File(name + ".zip")
                )
    else:
        raise Exception("The specified channel ID does not exist.")

    log.info("Successfully backed up!")


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user.name}")

    backup_world.start()


bot.run(os.getenv("DISCORD_TOKEN"))
