import os
import discord
import random
import asyncio
# import youtube_dl
import yt_dlp as youtube_dl
import nacl
import urllib.parse
import re
import requests
import aiohttp
import json
import datetime
import pytz

# from youtube_search import YoutubeSearch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from discord import Permissions
# import nacl.secret
# from dotenv import load_dotenv
from keep_alive import keep_alive

# load_dotenv()
# my_secret = os.environ['Robot']

intents = discord.Intents.all()

client = discord.Client(intents=intents)

week_options = {
    '1️⃣': 'Saturday',
    '2️⃣': 'Sunday',
    '3️⃣': 'Monday',
    '4️⃣': 'Tuesday',
    '5️⃣': 'Wednesday',
    '6️⃣': 'Thursday'
}

time_options = {
    '1️⃣': '08:00 AM-09:20 AM',
    '2️⃣': '09:30 AM-10:50 AM',
    '3️⃣': '11:00 AM-12:20 PM',
    '4️⃣': '12:30 PM-01:50 PM',
    '5️⃣': '02:00 PM-03:20 PM',
    '6️⃣': '03:30 PM-04:50 PM',
    '7️⃣': '05:00 PM-06:20 PM'
}

selected_week = None
selected_time = None

voice_client = None
is_playing = False
# previous_song = None
inactive_time = 5  # In seconds

songs_folder = "songs"

# Path to your songs folder
songs_folder = "songs"

# Function to delete all files and subdirectories
def delete_contents(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

c = 0
dic = {}

team = ["Brazil", "Croatia"]
team1 = ["Netherlands", "Argentina"]

#Embeded message
embed = discord.Embed()
embed.description = '''Nothing for now!'''

#!arrow
line = "↓↓↓↓↓↓↓↓\n↓↓↓↓↓↓↓↓\n↓↓↓↓↓↓↓↓\n↓↓↓↓↓↓↓↓\n↓↓↓↓↓↓↓↓\n"*4

#!help
help1 = '''Instruction:
All commands :

1.(!deadlines) : Use this command to know about your upcoming course assignment, quiz, exam, etc.

2.(!update) : Use this to update deadlines. Note: while using !update first give a space after !update (example : "!update  HelLo" not "!updateHello") and then write your updated deadlines.

3.!helpme

All these commands only works in "announcement" channel.'''

#Youtube code


#
def read():
  robot_file = open('Robot update.txt')
  read = robot_file.read()
  return read
  robot_file.close()

def updated_deadline(new):
  file = open('Robot update.txt','w')
  file.write(new)
  file.close()

def remove_line(new):
  file = open('Robot update.txt')
  store = file.readlines()
  removed = ""
  for i, j in enumerate(store):
    if new in j:
      removed = store[i]
      store.pop(i)
  if removed == "":
    return "Nothing"
  new1 = ""
  for k in store:
    new1+=k
  file1 = open('Robot update.txt','w')
  file1.write(new1)
  return removed
  file.close()
  file1.close()


def read3():
  robot_file3 = open('exam.txt')
  read3 = robot_file3.read()
  return read3
  robot_file3.close()

def updated_deadline3(new3):
  file  = open('exam.txt','w')
  file.write(new3)
  file.close()

def read2():
  robot_file2 = open('Recordings.txt')
  read2 = robot_file2.read()
  return read2
  robot_file2.close()

def updated_recordings(new):
  file  = open('Recordings.txt','w')
  file.write(new)
  file.close()

def go_away():
  file  = open('go away.txt','r')
  return file.read()
  file.close()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
    global voice_client, is_playing

    if voice_client is not None and voice_client.channel is not None:
        members_in_channel = len(voice_client.channel.members) - 1  # Exclude bot itself

        if members_in_channel == 0:
            await asyncio.sleep(inactive_time)
            members_in_channel = len(voice_client.channel.members) - 1  # Check again after waiting

            if members_in_channel == 0:
                await voice_client.disconnect()
                voice_client = None
                is_playing = False

    

@client.event
async def on_message(message):
  global voice_client, is_playing
  
  if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
    store = go_away()
    embed.description = store
    await message.channel.send(file = discord.File('middle.gif'),embed=embed)
    
  if str(message.channel) not in ( "test-channel","announcement","asim","apu","shuvo","zaber","faisal","walid","recordings-playlists","exam-dates","adda","listen-musics","github-status","available-room-bracu"):
    return
  if message.author == client.user:
    return
  msg = message.content
  print(msg)

  if msg.startswith("!update"):
    new = msg.split("!update ",1)[1]
    updated_deadline(new)
    embed.description = new
    await message.reply(f"{message.author.mention}Looks like it updated successfully but to make sure kindly type 😉'!deadlines' here!")

  if msg.startswith("!remove"):
    new = msg.split("!remove ",1)[1]
    removed = remove_line(new)
    if removed != "Nothing":
      await message.reply(f"{message.author.mention}This Line '{removed}' has been removed from the deadline succesfully but to make sure kindly type 😉'!deadlines' here!")
    else:
      await message.reply(f"{message.author.mention}There is no such Line written as '{new}' Bitch!")
      

  if msg.startswith("!up exam"):
    new = msg.split("!up exam ",1)[1]
    updated_deadline3(new)
    await message.reply(f"{message.author.mention}Looks like it updated successfully but to make sure kindly type 😉'!exam' here!")


  if msg.startswith("!deadlines"):
    global c
    global dic
    if len(dic) > 1:
      dic = {}
      c = 0
    user_id = message.author.id
    if user_id not in dic:
      c+=1
      dic[user_id] = c
      new = read()
      embed.description = new
      await message.reply(embed=embed)
    else:
      c+=1
      dic[user_id] = c
      if dic[user_id] > 3:
        c = 0
        del dic[user_id]
        await message.author.send(file = discord.File('lojja.gif'))
      else:
        new = read()
        embed.description = new
        await message.reply(embed=embed)
    
    #await message.reply(new)

  if msg.startswith("!recordings"):
    new2 = read2()
    embed.description = new2
    await message.reply(embed=embed) #new2

  if msg.startswith("!up recording"):
    new = msg.split("!up recording ",1)[1]
    updated_recordings(new)
    embed.description = new
    await message.reply(f"{message.author.mention}Looks like it updated successfully but to make sure kindly type 😉'!recordings' here!")

  if msg.startswith("!helpme"):
    await message.reply(help1)
  
  if msg.startswith("!arrow"):
    await message.reply(line)

  if msg.startswith("!exam"):
    if len(dic) > 1:
      dic = {}
      c = 0
    user_id = message.author.id
    if user_id not in dic:
      c+=1
      dic[user_id] = c
      new3 = read3()
      embed.description = new3
      await message.reply(embed=embed)
    else:
      c+=1
      dic[user_id] = c
      if dic[user_id] > 3:
        c = 0
        del dic[user_id]
        await message.author.send(file = discord.File('lojja.gif'))
      else:
        new3 = read3()
        embed.description = new3
        await message.reply(embed=embed)
  
  if msg.startswith('!apu'):
    await message.reply("Apu the আপু!",file = discord.File('apu.jpg'))
    
  if msg.startswith('!faisal'):
    await message.reply("Faisal the MNS faculty!",file = discord.File('faisal.jpg'))
    
  if msg.startswith('!zaber'):
    await message.reply("Zaber the Sofa pro!",file = discord.File('zaber.jpg'))

  if msg.startswith('!asim'):
    await message.reply("Asim the Code Boss!",file = discord.File('asim.jpg'))

  if msg.startswith('!shuvo'):
    await message.reply("Shuvo the চা পাগলা!",file = discord.File('shuvo.jpg'))

  if msg.startswith('!walid'):
    await message.reply("Walid the Diamond Noob!",file = discord.File('walid.jpg'))

  if msg.startswith('!Brazil or Croatia who wins?'):
    await message.reply(random.choice(team))

  if msg.startswith('!Argentina or Netherlands who wins?'):
    await message.reply(random.choice(team1))


  #youtube
  if msg.startswith('!play'):
        search_query = msg[6:].strip()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './songs/%(title)s.%(ext)s',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if 'entries' in search_results:
                video_info = search_results['entries'][0]
            else:
                video_info = search_results

            ydl.download([video_info['webpage_url']])

        song_filename = f"./songs/{video_info['title']}.{video_info['ext']}"

        voice_channel = message.author.voice.channel
        if voice_channel is None:
            await message.channel.send("You are not connected to a voice channel.")
            return

        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)

        if voice_client.is_playing() or is_playing:
            voice_client.stop()

        voice_client.play(discord.FFmpegPCMAudio(song_filename))

        is_playing = True
        await message.channel.send(f"Now playing: {video_info['title']}")

  elif msg == '!pause':
        if voice_client is not None and voice_client.is_playing():
            voice_client.pause()
            await message.channel.send("Playback paused.")
        else:
            await message.channel.send("I'm not currently playing any song.")

  elif msg == '!resume':
        if voice_client is not None and voice_client.is_paused():
            voice_client.resume()
            await message.channel.send("Playback resumed.")
        else:
            await message.channel.send("I'm not currently paused.")

  elif msg == '!leave':
        if voice_client is not None:
            await voice_client.disconnect()
            voice_client = None
            is_playing = False
          # Call the function to delete contents of the songs folder
            delete_contents(songs_folder)
            await message.channel.send("I left the voice channel.")
        else:
            await message.channel.send("I'm not in a voice channel.")



  
  # if str(message.channel) in ("listen-musics"):
  #   print("hello")
  #   if msg.startswith('!play'):
  #         search_query = msg[6:].strip()
  
  #         ydl_opts = {
  #             'format': 'bestaudio/best',
  #             'outtmpl': './songs/%(title)s.%(ext)s',
  #         }
  
  #         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
  #             search_results = ydl.extract_info(f"ytsearch:{search_query}", download=False)
  #             if 'entries' in search_results:
  #                 video_info = search_results['entries'][0]
  #             else:
  #                 video_info = search_results
  
  #             ydl.download([video_info['webpage_url']])
  
  #         song_filename = f"./songs/{video_info['title']}.{video_info['ext']}"
  
  #         voice_channel = message.author.voice.channel
  #         if voice_channel is None:
  #             await message.channel.send("You are not connected to a voice channel.")
  #             return
  
  #         if voice_client is None:
  #             voice_client = await voice_channel.connect()
  #         elif voice_client.channel != voice_channel:
  #             await voice_client.move_to(voice_channel)
  
  #         if voice_client.is_playing() or is_playing:
  #             voice_client.stop()
  
  #         voice_client.play(discord.FFmpegPCMAudio(song_filename))
  
  #         is_playing = True
  #         await message.channel.send(f"Now playing: {video_info['title']}")
  
  #   elif msg == '!pause':
  #         if voice_client is not None and voice_client.is_playing():
  #             voice_client.pause()
  #             await message.channel.send("Playback paused.")
  #         else:
  #             await message.channel.send("I'm not currently playing any song.")
  
  #   elif msg == '!resume':
  #         if voice_client is not None and voice_client.is_paused():
  #             voice_client.resume()
  #             await message.channel.send("Playback resumed.")
  #         else:
  #             await message.channel.send("I'm not currently paused.")
  
  #   elif msg == '!leave':
  #         if voice_client is not None:
  #             await voice_client.disconnect()
  #             voice_client = None
  #             is_playing = False
  #           # Call the function to delete contents of the songs folder
  #             delete_contents(songs_folder)
  #             await message.channel.send("I left the voice channel.")
  #         else:
  #             await message.channel.send("I'm not in a voice channel.")

  #github
  if str(message.channel) in ("github-status"):
    if message.content.startswith('!github'):
          username = message.content.split(' ')[1]
  
          # Send a GET request to the GitHub API
          response = requests.get(f'https://api.github.com/users/{username}')
  
          if response.status_code == 200:
              data = response.json()
  
              embed = discord.Embed(title=f'GitHub Information for {data["login"]}', color=0x00ff00)
              embed.add_field(name='Name', value=data.get('name', 'Not provided'), inline=False)
              embed.add_field(name='Bio', value=data.get('bio', 'Not provided'), inline=False)
              embed.add_field(name='Followers', value=data.get('followers', 0), inline=True)
              embed.add_field(name='Following', value=data.get('following', 0), inline=True)
              embed.add_field(name='Public Repositories', value=data.get('public_repos', 0), inline=True)
              embed.add_field(name='Location', value=data.get('location', 'Not provided'), inline=False)
              embed.add_field(name='Email', value=data.get('email', 'Not provided'), inline=False)
              
              embed.add_field(name='Profile Link', value=f'https://github.com/{data["login"]}', inline=False)
              embed.set_thumbnail(url=data.get('avatar_url'))
  
              await message.channel.send(embed=embed)
          else:
              await message.channel.send('GitHub account not found.')


  #Empty classroom and Labroom
  global selected_week
  global selected_time
  if str(message.channel) in ("available-room-bracu"):
    if message.content == '!freeroom':
        week_message = await message.channel.send("Select a day for a free room:")

        options_text = '\n'.join([f"{emoji} {i}. {day}" for i, (emoji, day) in enumerate(week_options.items(), start=1)])
        await week_message.edit(content=f"{week_message.content}\n{options_text}")

        for emoji in week_options.keys():
            await week_message.add_reaction(emoji)

        def check_week(reaction, user):
            return not user.bot and reaction.message.id == week_message.id and reaction.emoji in week_options.keys()

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check_week)
            selected_week = week_options[reaction.emoji]
        except asyncio.TimeoutError:
            await message.channel.send("Time limit exceeded. Please try again.")
            return

        await week_message.delete()

        time_message = await message.channel.send("Select a time range for a free room:")

        options_text = '\n'.join([f"{emoji} {i}. {time}" for i, (emoji, time) in enumerate(time_options.items(), start=1)])
        await time_message.edit(content=f"{time_message.content}\n{options_text}")

        for emoji in time_options.keys():
            await time_message.add_reaction(emoji)

        def check_time(reaction, user):
            return not user.bot and reaction.message.id == time_message.id and reaction.emoji in time_options.keys()

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check_time)
            selected_time = time_options[reaction.emoji]
        except asyncio.TimeoutError:
            await message.channel.send("Time limit exceeded. Please try again.")
            return

        await time_message.delete()

        with open('data.json', 'r') as file:
          data = json.load(file)
          store = data['availableRooms'][selected_week][selected_time]
          lab = data["labRooms"]

          embed = discord.Embed(title=f'Available Rooms {selected_week} {selected_time}', color=0x3fe0d0)

          column_limit = 15
          current_column = 0
          column_count = 1
          column_data = ""

          for room in store:
              room_name = room
              
              if room_name not in lab:
                  column_data += f"{room_name}\n"
              else:
                  column_data += f"**Lab room:** {room_name}\n"
              
              current_column += 1
              
              if current_column == column_limit:
                  embed.add_field(name=f'Column {column_count}', value=column_data, inline=True)
                  column_data = ""
                  current_column = 0
                  column_count += 1
          
          # Add any remaining rooms
          if column_data != "":
              embed.add_field(name=f'Column {column_count}', value=column_data, inline=True)

          await message.channel.send(embed=embed)
          










        # time_zone = pytz.timezone('Asia/Dhaka')
        # current_time = datetime.datetime.now(time_zone)
        # current_day = datetime.datetime.now(time_zone).strftime("%A")

        # print(data["availableRooms"])
        












        # # Check if it's Friday and the current time is not within any time range in the JSON file
        # if current_day == "Friday":
        #     time_ranges = ["08:00 AM-09:20 AM", "09:30 AM-10:50 AM", "11:00 AM-12:20 PM", "12:30 PM-01:50 PM",
        #                    "02:00 PM-03:20 PM", "03:30 PM-04:50 PM", "05:00 PM-06:20 PM"]
        #     is_time_range_valid = any(time_range for time_range in time_ranges if current_time.strftime("%I:%M %p") in time_range)

        #     if not is_time_range_valid:
        #         embed = discord.Embed(title="Unavailable on Friday", color=discord.Color.red())
        #         embed.add_field(name="No Available Rooms",
        #                         value="There are no rooms available on Friday at the current time range.",
        #                         inline=False)
        #         await message.channel.send(embed=embed)
        #         return

        # store = []
        # for entry in sheet1:
        #     day = entry["Day"]
        #     start_time = datetime.datetime.strptime(entry["Start time"], "%I:%M %p")
        #     end_time = datetime.datetime.strptime(entry["End time"], "%I:%M %p")
        #     room = entry["Room"]

        #     if day == current_day and start_time <= current_time.time() <= end_time.time():
        #         continue

        #     store.append(room)

        # unique_store = list(set(store))

        # # Check if there are available rooms and the current day is not Friday
        # if unique_store and current_day != "Friday":
        #     embed = discord.Embed(title=f"Available Free Rooms on {current_day} {current_time.strftime('%I:%M %p')}", color=discord.Color.yellow())

        #     columns = {}
        #     for room in unique_store:
        #         third_char = room[2]
        #         if third_char not in columns:
        #             columns[third_char] = []
        #         columns[third_char].append(room)

        #     for third_char, column_rooms in columns.items():
        #         column_text = "\n".join(column_rooms)
        #         field_name = f"Column {third_char}"
        #         embed.add_field(name=field_name, value=column_text, inline=True)

        #     await message.channel.send(embed=embed)
        # else:
        #     embed = discord.Embed(title="No Available Rooms", color=discord.Color.red())
        #     embed.add_field(name="No Available Rooms",
        #                     value="There are no rooms available at the current time.",
        #                     inline=False)
        #     await message.channel.send(embed=embed)



        
  

keep_alive()

client.run(os.getenv('Robot'))
# client.login(process.env.Robot)