from __future__ import annotations

from apify import Actor


async def main() -> None:
    async with Actor:

        payload = await Actor.get_input()
        print(payload)

        await Actor.set_status_message("Finished", is_terminal=True)
