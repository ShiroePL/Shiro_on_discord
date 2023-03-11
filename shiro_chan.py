# the Discord Python API
import discord
import connect_to_azuredb
import pyodbc
import api_keys
import play_audio as play_audio
from discord.ext import commands
import askshiro_voice
import askshiro_text
from embeds.introduce_embed import introduce_embed_fn
from db_config import conn


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    # Create a global connection object
conn = None

# When the bot is ready, run this code.
@bot.event
async def on_ready():
    print("------")
    print("connected to Azure DB")
    print("ShiroAi-chan is Up and ready!")
    try:
        synced = await bot.tree.sync()
        print("synced")
        print("------")
    except Exception as e:
        print(e)

@bot.event
async def on_voice_state_update(member, before, after): #FOR VOICE CONVERSATION
    if member == bot.user:
        # ignore events triggered by the bot itself
        return

    # check if the member is joining or leaving a channel
    if before.channel != after.channel:
        print(f"{member.display_name} has joined/ left the voice channel {after.channel.name}.")

    

    print(f"Before: {before.self_mute}")
    print(f"After: {after.self_mute}")
        # check if the member is currently muted
    if before.self_mute == True and after.self_mute == False: #from mute to unmute START RECORDING      
        print(f"{member.display_name} UNMUTED, RECORD HIM kiki!.") 
        
        # Get the guild and voice client objects      
    elif before.self_mute == False and after.self_mute == True: #from unmute to mute STOP RECORDING
        print(f"{member.display_name} MUTED, KIKI, save audio and I'll begin my work :).")
        askshiro_voice.handle_openai_response_voice




@bot.tree.command(name="introduce") #introduce embed
async def introduce(interaction: discord.Interaction):
    """Displays an introduction embed."""
    await interaction.response.send_message("Eghem, *deep breath*.", embed=introduce_embed_fn()) # Send the embed with some text

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    """Displays a list of available commands."""
    commands = []
    for command in bot.commands:
        commands.append(command.name)
    await interaction.response.send_message(f"Available commands: {', '.join(commands)}")

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello " + interaction.user.name + " !",file=discord.File('pictures/smile.gif'))
    
@bot.tree.command(name="reset_database")
async def reset_database(interaction: discord.Interaction):
    bot.loop.create_task(connect_to_azuredb.reset_chat_history_for_user(interaction))

@bot.tree.command(name="shock_1")
async def shock_1(interaction: discord.Interaction):
    await interaction.response.send_message("OMG!",file=discord.File('pictures/shock_1.gif'))

@bot.tree.command(name="shock_2")
async def shock_2(interaction: discord.Interaction):
    await interaction.response.send_message("WHAT!",file=discord.File('pictures/shock_2.gif'))    

@bot.tree.command(name="askshiro")
async def askshiro(interaction: discord.Interaction, question: str):
     # Schedule a coroutine to handle the OpenAI response
    bot.loop.create_task(askshiro_text.handle_openai_response_text(interaction, question))

@bot.tree.command(name="askshiro_with_voice")
async def askshiro_with_voice(interaction: discord.Interaction, question: str):
     # Schedule a coroutine to handle the OpenAI response
    bot.loop.create_task(askshiro_voice.handle_openai_response_voice(interaction, question))

@bot.tree.command(name="join_voice")
async def join_voice(interaction: discord.Interaction):
     # Schedule a coroutine to handle the OpenAI response
    user = interaction.user
    await user.voice.channel.connect()

    
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    """Shuts down the bot."""
    await ctx.send("Shutting down...")
    await bot.close()



# Login to Discord with the bot's token.
bot.run(api_keys.token_key)

# Close the database connection when the bot shuts down
@bot.event
async def on_shutdown():
    print("---GOING TO SLEEP, BYE!---")
    global conn
    if conn is not None:
        conn.close()

@bot.event
async def on_message(message):
    # check if the message is from the first bot
    first_bot_id = "1063830555403223100"
    if message.author.id == first_bot_id:
        # get the command to run
        command = message.content

        # run the command and get the output
        ctx = await bot.get_context(message)
        output = await bot.invoke(ctx)

        # send the output to the designated channel
        designated_channel_id = "1076207973904433216"
        designated_channel = bot.get_channel(designated_channel_id)
        await designated_channel.send(output)