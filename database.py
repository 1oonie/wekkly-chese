import asqlite


class Database:
    connection: asqlite.Connection

    def __init__(self, path: str):
        self.path = path

    async def connect(self):
        self.connection = await asqlite.connect(self.path)

    async def disconnect(self):
        await self.connection.close()
