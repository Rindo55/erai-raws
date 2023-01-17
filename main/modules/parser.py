import asyncio
from main.modules.schedule import update_schedule
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1

def trim_title(title: str):
    title = title.replace("[Erai-raws]","")
    return title

def parse():
    a = feedparser.parse("https://www.erai-raws.info/episodes/feed/?res=SD&type=magnet&subs%5B0%5D=us&0879fd62733b8db8535eb1be24e23f6d")
    b = a["entries"]
    data = []    

    for i in b:
        item = {}
        item['title'] = i['title']
        item['size'] = i['nyaa_size']
        item['link'] = i['link']
        data.append(item)
    data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        try:
            await status.edit(await status_text("Idle..."),reply_markup=button1)
            await update_schedule()
        except:
            pass

        await asyncio.sleep(30)
