# /// script
# dependencies = ["pygame-ce"]
# ///

import sys
import asyncio

if sys.platform == "emscripten":
    sys.path.insert(0, "/data/data/mma/assets")
else:
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def main() -> None:
    import flags
    from game import Game

    flags.parse()

    game = Game()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
