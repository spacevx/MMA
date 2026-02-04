import asyncio
import flags
from game import Game


async def main() -> None:
    flags.parse()

    game = Game()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
