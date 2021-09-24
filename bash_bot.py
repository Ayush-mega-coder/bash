# creating a bot
import discord
from discord.ext import commands
from discord import colour

import youtube_dl
import os

# creating a command
client = commands.Bot(command_prefix='-')

@client.command(name='version')
async def version(context):

    myEmbed = discord.Embed(
        title="Current version", description="The bot is version 1.0", color=0xfb00)
    myEmbed.add_field(name="Version code: ", value="v1.0.0", inline=False)
    myEmbed.add_field(name="Date Released ",
                      value="July 18th, 2021", inline=False)
    myEmbed.set_footer(text="Developed by Spunkey")
    myEmbed.set_author(name="Bash")

    await context.message.channel.send(embed=myEmbed)


@client.event
async def on_ready():

    general_channel = client.get_channel(849549651400065074)
    await general_channel.send('Hello, world! This is bash!')
            
#passing arguments and returning a string
@client.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


@client.event

# on_message func takes a parameter message and this function runs when somebody sends a message
async def on_message(message):
    general_channel = client.get_channel(849549651400065074)
    if message.content == 'what is the version':
    
        myEmbed = discord.Embed(
            title="Current version", description="The bot is version 1.0", color=0xff00)
        myEmbed.add_field(name="Version code: ", value="v1.0.0", inline=False)
        myEmbed.add_field(name="Date Released ",
                          value="July 18th, 2021", inline=False)
        myEmbed.set_footer(text="Developed by Spunkey")
        myEmbed.set_author(name="Bash")

        await general_channel.send(embed=myEmbed)
    # we have to specify this bc we are using this content for commands too
    await client.process_commands(message)
 
    if message.content == 'who':
        general_channel = client.get_channel(849549651400065074)
        await general_channel.send('I am bash')
        
    if message.content == 'what do you do':
        general_channel = client.get_channel(849549651400065074)
        await general_channel.send('i\'m a bot')
        
        
# Music

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()    

client.run('ODQ5NTQyNDIwMzc1MTQyNDEw.YLcsCA.HQ-BydQTK8YmptUaSlJmMEGdvmQ')
