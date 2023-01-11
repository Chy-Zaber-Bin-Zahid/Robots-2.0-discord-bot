import discord
import os
from keep_alive import keep_alive

client = discord.Client()

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

#
def read():
  robot_file = open('Robot update.txt')
  read = robot_file.read()
  return read
  robot_file.close()

def updated_deadline(new):
  file  = open('Robot update.txt','w')
  file.write(new)
  file.close()

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
  robot_file2 = open('Live class link.txt')
  read2 = robot_file2.read()
  return read2
  robot_file2.close()

def updated_deadline2(new):
  file  = open('Live class link.txt','w')
  file.write(new)
  file.close()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if str(message.channel) not in ( "test-channel","announcement","asim","apu","shuvo","zaber","faisal","live-class-link","exam-dates"):
    return
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith("!update"):
    new = msg.split("!update ",1)[1]
    updated_deadline(new)
    embed.description = new
    await message.reply(f"{message.author.mention}Looks like it updated successfully but to make sure kindly type 😉'!deadlines' here!")

  if msg.startswith("!up exam"):
    new = msg.split("!up exam ",1)[1]
    updated_deadline3(new)
    await message.reply(f"{message.author.mention}Looks like it updated successfully but to make sure kindly type 😉'!exam' here!")

  if msg.startswith("!deadlines"):
    new = read()
    embed.description = new
    await message.reply(embed=embed)
    #await message.reply(new)

  if msg.startswith("!link"):
    new2 = read2()
    embed.description = new2
    await message.reply(embed=embed) #new2

  if msg.startswith("!helpme"):
    await message.reply(help1)
  
  if msg.startswith("!arrow"):
    await message.reply(line)

  if msg.startswith("!exam"):
    new3 = read3()
    embed.description = new3
    await message.reply(embed=embed)

keep_alive()
client.run(os.getenv('Robot'))
