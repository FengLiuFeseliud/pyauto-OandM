import asyncio
import aiohttp
import copy


class Img:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }

    def __init__(self, dtime, cookie=""):
        self.__task = []
        self.__session = None
        self.__loop = None
        self.headers["cookie"] = cookie
        self.dtime = dtime

    async def session(self):
        if self.__session == None:
            self.__session = aiohttp.ClientSession(headers=self.headers)
        
        return self.__session
    
    def loop(self):
        if self.__loop == None:
            self.__loop = asyncio.get_event_loop()
        
        return self.__loop
    
    async def __get(self, mode, yi, limit, dtime):
        offset = limit * yi
        api = f"https://www.vilipix.com/api/illust?mode={mode}&limit={limit}&offset={offset}&date={dtime}"

        session = await self.session()
        async with session.get(api) as req:
            data = await req.json()

        return (mode, data["rows"], dtime)
        
    async def __add_task(self, mode, limit):
        for yi in range(0, 10):
            self.__task.append(asyncio.create_task(self.__get(mode, yi, limit, self.dtime)))
    
    def daily(self, limit=30):
        self.loop().run_until_complete(self.__add_task("daily", limit))
    
    def weekly(self, limit=30):
        self.loop().run_until_complete(self.__add_task("weekly", limit))
    
    def monthly(self, limit=30):
        self.loop().run_until_complete(self.__add_task("monthly", limit))
    
    async def __run_task(self):
        await asyncio.wait(self.__task)
    
    def run_task(self, func):
        self.loop().run_until_complete(self.__run_task())
        for task in self.__task:
            mode, data, dtime = task.result()
            func(mode, data, dtime)

        return data

