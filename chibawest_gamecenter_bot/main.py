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
        if message.content == "!cmd":
            await message.channel.send(
                "\n".join(
                    [
                        "!cmd ... botが利用可能なコマンドを表示する",
                        "!repos ... アプリケーションのGitHubリポジトリを表示する",
                        "!mc_start ... マイクラサーバーを起動する",
                        "!mc_stop ... マイクラサーバーを停止する",
                        "!mc_get ... マイクラサーバーの状態を取得する",
                        "!mc_ip ... マイクラサーバーのIPアドレスを取得する",
                    ]
                )
            )
        if message.content == "!repos":
            await message.channel.send(
                "https://github.com/mytk0u0/chibawest-gamecenter-apps"
            )
        if message.content == "!mc_start":
            await message.channel.send("マイクラサーバーを起動します。")
            await minecraft.start_server()
        if message.content == "!mc_stop":
            await message.channel.send("マイクラサーバーを停止します。")
            await minecraft.stop_server()
        if message.content == "!mc_get":
            status = await minecraft.get_server_status()
            await message.channel.send(f"マイクラサーバーの状態: {status}")
        if message.content == "!mc_ip":
            ip = await minecraft.get_server_ip()
            await message.channel.send(f"アドレス: {ip}\nポート: 19132")


def run():
    logger = get_logger()

    logger.info("Downloading discord token...")
    discord_token = get_discord_token()  # アクセス件が無い場合は利用可能な適当なtokenで代用してください
    logger.info("Discord token was downloaded.")

    logger.info("Starting bot application...")
    client = ChibawestGamecenterBot()
    client.run(discord_token)
    logger.info("Bot application is running.")
