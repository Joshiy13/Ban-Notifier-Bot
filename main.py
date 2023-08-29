import discord
import requests
import asyncio
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
ANTICHEAT_CHANNEL = int(os.getenv("ANTICHEAT_CHANNEL"))
STAFF_CHANNEL = int(os.getenv("STAFF_CHANNEL"))

last_staff_total = 0
last_watchdog_total = 0

async def send_increase_messages(channel, title, total, increase, description):
    current_unix_timestamp = int(datetime.now().timestamp())
    for _ in range(increase):
        embed = discord.Embed(
            title=f"{title}",
            description=f"Ban Time: <t:{current_unix_timestamp}:R>\n{description}",
            color=0xff0000 if "Staff" in title else 0x5b4295
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1004630104019837008/1146043716558131310/image0.webp" if "Staff" in title else "https://cdn.discordapp.com/attachments/1004630104019837008/1146043388559364206/image0.jpg")
        embed.set_footer(text="schummelware.com", icon_url="https://cdn.discordapp.com/icons/1133857876209836063/201545faaa922146e6489583ae735b70.webp?size=160")
        await channel.send(embed=embed)
        print(f"{title} #{total}")  # Print the increase to the console
        total -= 1  # Decrement total for the next message

async def check_punishment_stats():
    global last_staff_total, last_watchdog_total

    while True:
        try:
            response = requests.get('https://api.hypixel.net/punishmentstats', params={'key': API_KEY})
            data = response.json()

            if data['success']:
                staff_total = data['staff_total']
                watchdog_total = data['watchdog_total']
                staff_increase = staff_total - last_staff_total
                watchdog_increase = watchdog_total - last_watchdog_total

                if last_staff_total != 0 and staff_total > last_staff_total:
                    channel = client.get_channel(STAFF_CHANNEL)
                    if channel:
                        await send_increase_messages(channel, "Staff ban", staff_total, staff_increase, "They on your ass bruh")

                if last_watchdog_total != 0 and watchdog_total > last_watchdog_total:
                    channel = client.get_channel(ANTICHEAT_CHANNEL)
                    if channel:
                        await send_increase_messages(channel, "Watchdog ban", watchdog_total, watchdog_increase, "Nice config idiot")

                last_staff_total = staff_total
                last_watchdog_total = watchdog_total

        except Exception as e:
            print(f'Error occurred while checking punishment stats: {e}')

        await asyncio.sleep(1)

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