import asyncio
from enum import Enum
from googleapiclient.discovery import build

query = {
    "project": "chibawest-gamecenter",
    "zone": "asia-northeast1-a",
    "instance": "valheim-instance",
}


async def get_server_status() -> str:
    return build("compute", "v1").instances().get(**query).execute()["status"]


async def get_server_ip() -> str:
    return (
        build("compute", "v1")
        .instances()
        .get(**query)
        .execute()["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
    )


async def start_server() -> None:
    status = await get_server_status()
    if status in {"STAGING", "STOPPING", "RUNNING"}:
        return
    build("compute", "v1").instances().start(**query).execute()


async def stop_server() -> None:
    status = await get_server_status()
    if status in {"STAGING", "STOPPING", "TERMINATED"}:
        return
    build("compute", "v1").instances().stop(**query).execute()
