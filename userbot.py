from pyrogram import Client
import aiohttp
from datetime import datetime

import asyncio

api_id = '22361461'
api_hash = 'b4da203deab5553a109bdce28421e6d3'

server_url = "http://localhost:5000/"
channel_id = -1002213479744

app = Client("viewer", api_id=api_id, api_hash=api_hash)

@app.on_message()
async def handle_messages(client, message):
    
    
    if message.chat.id == channel_id:
        print(message)

        try:
            
            if message.text or message.caption:
            
                if message.text:
                    args = {
                        "chat_id": message.chat.id,
                        "message_id": message.id,
                        "text": message.text,
                        "media": "None",
                        "views": message.views,
                        "forwards": message.forwards,
                        "date": message.date
                    }
                    
                elif message.caption:
                    args = {
                        "chat_id": message.chat.id,
                        "message_id": message.id,
                        "text": message.caption,
                        "media": message.photo.file_id,
                        "views": message.views,
                        "forwards": message.forwards,
                        "date": message.date
                    }
                else:
                    pass
                    
            else:
                pass

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    server_url + "post/add" + 
                    f"?id={args["message_id"]}&description={args["text"]}&media=None&pub_date={args["date"]}&forwards={args["forwards"]}&views={args["views"]}"
                , ssl = False) as response:
                    json = await response.json()
                    print(json)
                
        except Exception as E:
            print(E)

async def main():
    await app.start()

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()