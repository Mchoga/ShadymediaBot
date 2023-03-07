import time
import asyncio

async def test(num):
    await asyncio.sleep(2)
    print(num)



async def testa(num):
    print(num)

async def main():
    task1 = asyncio.create_task(test(0))
    task2 = asyncio.create_task(testa(1))
    await task1

    # await task2


asyncio.run(main())


