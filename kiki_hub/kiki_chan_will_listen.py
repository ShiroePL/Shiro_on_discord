import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient  # important! #works becaouse this is in VIRTUAL ENVIROMENT
import sys
sys.path.insert(0, '../')
import api_keys
intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')
stored_ctx = None

@client.event
async def on_ready():
    try:
        print("------")
        print("Kiki-Chan is Up and ready to listen!")
        print("------")
    except Exception as e:
        print(e)

@client.command()
async def converse(ctx):
    global stored_ctx
    stored_ctx = ctx
    #await ctx.send('NOW I HAVE CTX')
    await stored_ctx.send('Needed to take your personal informations :O Now I know everything i need ^_^')
    


@client.event
async def on_voice_state_update(member, before, after):
    global stored_ctx
    if member == client.user:
        # ignore events triggered by the bot itself
        return
        # check if the member is joining or leaving a channel
    if before.channel != after.channel:
        print(f"{member.display_name} has joined/ left the voice channel {after.channel.name}.")
        # print the before and after voice states
    print(f"Before: {before.self_mute}")
    print(f"After: {after.self_mute}")
        # check if the member is currently muted
    if before.self_mute == True and after.self_mute == False: #from mute to unmute START RECORDING      
        print(f"{member.display_name} UNMUTED, RECORD HIM!.") 
        await stored_ctx.invoke(client.get_command('rec'))
        await stored_ctx.send('to jest odpalone przez unmute AUTOMATICO')
        # Get the guild and voice client objects      
    elif before.self_mute == False and after.self_mute == True: #from unmute to mute STOP RECORDING
        print(f"{member.display_name} MUTED, STOOOOP RECORDING.")
        await stored_ctx.invoke(client.get_command('stop'))
        


@client.command()
async def help(ctx):
    embedVar = discord.Embed(title="here are my commands!",
                             description="nuser **!join** to start the recording\nuser **!stop** to stop the recording", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def join(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)   
    await channel.connect(cls=NativeVoiceClient)   
    await stored_ctx.send('joined the channel')


@client.command()
async def rec(ctx):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)  
    await channel.connect(cls=NativeVoiceClient)
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')
    wav_bytes = await ctx.voice_client.stop_record()
    with open('recording.wav', 'wb') as f:
        f.write(wav_bytes)
    await ctx.voice_client.disconnect()

@rec.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=NativeVoiceClient)
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

client.run(api_keys.kiki_token)