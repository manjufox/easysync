import asyncio
import sqlite3


class MyDB:
    # async with に入る直前に呼ばれます。
    async def __aenter__(self):
        self._connection 
        return self

    # async with ブロックを抜けた直後に呼ばれます。
    async def __aexit__(self, exc_type, exc, tb):
        self._connection.close()

    async def fetchall(self, query, args=[]):
        cursor = await self._connection.cursor()
        await cursor.execute(query, args)
        return await cursor.fetchall()