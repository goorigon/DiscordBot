import discord
from datetime import datetime
from DBClass import DBClass
from parser import Parser
from logs import Logs

#Yes, in plain text :(
client = discord.Client()
dbclass = DBClass()
parser = Parser()
logs = Logs()
messages = dbclass.messagesFromDB()

#This is just a function called when the bot is powered up-
#prints a message in the console.
@client.event
async def on_ready():
    messages = dbclass.messagesFromDB()
    print(messages['OnReady1'])
    print(messages['OnReady2'])
    print(messages['OnReady3'])

#This is the 'main' part of the bot e.a. events triggered by specified messages
#sent by users.
@client.event
async def on_message(message):
    #A dictionary of commands from the DB, currently updated on every message
    #for the developement purposes - you might want to FIXME in the future!
    commands = dbclass.commandFromDBParser()
    if(message.author == client.user):
        return
    #If the message matches one of the keys in the commands dictionary e.a. is
    #a valiable command it get parsed through the parser method to replace tags
    if(message.content.lower() in commands):
        key = message.content.lower()
        try:
            messageToParse = commands.get(key)
            #This is a possible FIXME I don't like that you have to provide the
            #parser with a user or otherwise you run into a danger of triggering
            #TypeError when user related tags appear, but it's not really urgent
            await client.send_message(message.channel,
            parser.parser(messageToParse, message.author))
        except Exception as e:
            print('This should not have happened, but if it did:'
                  'the following key was provided {}'.format(key))
            print(e)
    elif("!banuj" in message.content.lower()):
        if(message.author.server_permissions.ban_members):
            messageList = message.content.split()
            userToBan = discord.utils.find(lambda m: m.name == messageList[1], message.server.members)
            banDescription = message.content.replace(messageList[0], '')
            banDescription = banDescription.replace(messageList[1], '')
            banDescription = "{0} {1}".format(
                        parser.parser(messages['AdminBanDescription'], userToBan),
                        banDescription)
            embed = logs.embedMessage(discord, message.author, message,
                                 parser.parser(messages['AdminBanTitle'], userToBan),
                                 banDescription,
                                 discord.Colour(0xEC1F5E),
                                 datetime.now(),
                                 target = userToBan)
            await client.ban(userToBan, 0)
            await client.send_message(message.channel,
            parser.parser(messages['BanDescription'], userToBan))
            await client.send_message(discord.Object(id=messages['AdminChannelId']), embed=embed)
        else:
            await client.send_message(message.channel,
            parser.parser(messages['NoPermission'], message.author))

#A function which triggers when someone joins the Discord server
#It prints a welcome message.
@client.event
async def on_member_join(member):
    #Define bot and messages dict
    messages = dbclass.messagesFromDB()
    bot = discord.utils.get(member.server.members, id=messages['BotId'])
    #Define embed message to be displa
    embed = logs.embedMessage(discord, bot, member,
                         parser.parser(messages['AdminNewUserMessageTitle'], member),
                         parser.parser(messages['AdminNewUserMessage'], member),
                         discord.Colour(0x53d868),
                         datetime.now(),
                         target = member)

    await client.send_message(discord.Object(id=messages['WelcomeChannelId']),
        parser.parser(messages['WelcomeMessage'], member = member))
    await client.send_message(discord.Object(id=messages['AdminChannelId']), embed=embed)

    print("{0} | A new member has joined the server - {1}".format(datetime.now(), member.name))

#Runs the bot
client.run(messages['Token'])
