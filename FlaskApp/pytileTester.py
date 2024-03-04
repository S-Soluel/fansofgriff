import asyncio
from aiohttp import ClientSession
from pytile import async_login

email    = 'Brickyoyo10@gmail.com'
password = 'UE9Sl-0yn5@$F-h'
#Rucksack uuid = xxx
async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login(email, password, session)
        tiles = await api.async_get_tiles()
        for tile_uuid, tile in tiles.items():
            print(f"{tile.latitude} {tile.longitude}")
            if tile.kind == "TILE":
                return tile.latitude, tile.longitude
            if tile.uuid == "xxx":
                break

asyncio.run(main())