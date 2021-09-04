import asyncio
import discord
from google.cloud import secretmanager
from . import minecraft
import logging
import os


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


def get_discord_token() -> str:
    client = secretmanager.SecretManagerServiceClient()
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    except KeyError:
        name = "projects/chibawest-gamecenter/secrets/discord-bot-api-token-dev/versions/latest"
    else:
        name = "projects/chibawest-gamecenter/secrets/discord-bot-api-token/versions/latest"
    request = secretmanager.AccessSecretVersionRequest(name=name)
    response = client.access_secret_version(request=request)
    return response.payload.data.decode("utf-8")


class ChibawestGamecenterBot(discord.Client):
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content == "!commands":
            await message.channel.send(
                "\n".join(
                    [
                        "!commands ... botが利用可能なコマンドを表示する",
                        "!repos ... アプリケーションのGitHubリポジトリを表示する",
                        "!status ... マイクラサーバーを起動する",
                        "!hey xxx ... xxxサーバーを起動",
                        "!bye xxx ... xxxサーバーを停止",
                        "!how xxx ... xxxサーバーへのログイン方法を表示",
                    ]
                )
            )
        if message.content == "!repos":
            await message.channel.send(
                "https://github.com/mytk0u0/chibawest-gamecenter-bot"
            )

        if message.content == "!status":
            status = await minecraft.get_server_status()
            await message.channel.send(f"minecraft server status: {status}")

            status = await minecraft.get_server_status()
            await message.channel.send(f"valheim server status: {status}")

        # minecraft commands
        if message.content == "!hey minecraft":
            await message.channel.send("minecraftを始めます")
            await minecraft.start_server()
        if message.content == "!bye minecraft":
            await message.channel.send("minecraftを終わります")
            await minecraft.stop_server()
        if message.content == "!how minecraft":
            ip = await minecraft.get_server_ip()
            await message.channel.send(f"アドレス{ip}にポート19132で接続してください。")

        # valheim commands
        if message.content == "!hey valheim":
            await message.channel.send("valheimを始めます")
            await minecraft.start_server()
        if message.content == "!bye valheim":
            await message.channel.send("valheimを終わります")
            await minecraft.stop_server()
        if message.content == "!how valheim":
            ip = await minecraft.get_server_ip()
            await message.channel.send(f"{ip}:2456でサーバーに接続してください。「chibawest」で入れます")


def run():
    logger = get_logger()

    logger.info("Downloading discord token...")
    discord_token = get_discord_token()  # アクセス件が無い場合は利用可能な適当なtokenで代用してください
    logger.info("Discord token was downloaded.")

    logger.info("Starting bot application...")
    client = ChibawestGamecenterBot()
    client.run(discord_token)
    logger.info("Bot application is running.")
