import discord
import requests
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
ANTICHEAT_CHANNEL = int(os.getenv("ANTICHEAT_CHANNEL"))
STAFF_CHANNEL = int(os.getenv("STAFF_CHANNEL"))

last_staff_total = 0
last_watchdog_total = 0

async def check_punishment_stats():
    global last_staff_total, last_watchdog_total

    while True:
        try:
            response = requests.get('https://api.hypixel.net/punishmentstats', params={'key': API_KEY})
            data = response.json()

            if data['success']:
                staff_total = data['staff_total']
                watchdog_total = data['watchdog_total']

                if last_staff_total != 0 and staff_total > last_staff_total:
                    channel = client.get_channel(STAFF_CHANNEL)
                    if channel:
                        staff_banned = discord.Embed(
                            title=f"Staff ban #{staff_total}",
                            description="This was a staff ban. Be careful!",
                            color=0xff0000
                        )
                        await channel.send(embed=staff_banned)
                        print(f"Staff ban #{staff_total}. This was a staff ban. Be careful!")

                if last_watchdog_total != 0 and watchdog_total > last_watchdog_total:
                    channel = client.get_channel(ANTICHEAT_CHANNEL)
                    if channel:
                        watchdog_banned = discord.Embed(
                            title=f"Anticheat ban #{watchdog_total}",
                            description="Don't worry, this was an anticheat ban.",
                            color=0xff0000
                        )
                        await channel.send(embed=watchdog_banned)
                        print(f"Watchdog ban #{watchdog_total}. Don't worry, this was an anticheat ban.")

                last_staff_total = staff_total
                last_watchdog_total = watchdog_total

        except Exception as e:
            print(f'Error occurred while checking punishment stats: {e}')

        await asyncio.sleep(1)  # Check every second

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    banner = """
  _    _                _             _   ____                  _   _         _    _  __   _             
 | |  | |              (_)           | | |  _ \                | \ | |       | |  (_)/ _| (_)            
 | |__| | _   _  _ __   _ __  __ ___ | | | |_) |  __ _  _ __   |  \| |  ___  | |_  _ | |_  _   ___  _ __ 
 |  __  || | | || '_ \ | |\ \/ // _ \| | |  _ <  / _` || '_ \  | . ` | / _ \ | __|| ||  _|| | / _ \| '__|
 | |  | || |_| || |_) || | >  <|  __/| | | |_) || (_| || | | | | |\  || (_) || |_ | || |  | ||  __/| |   
 |_|  |_| \__, || .__/ |_|/_/\_\\___| |_| |____/  \__,_||_| |_| |_| \_| \___/  \__||_||_|  |_| \___||_|   
           __/ || |                                                                                      
          |___/ |_|  

by joshiy13
"""
    print(banner)
    await check_punishment_stats()

client.run(TOKEN)