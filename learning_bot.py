# the Discord Python API
import discord
import connect_to_azuredb
import pyodbc
import api_keys
import play_audio as play_audio
from discord.ext import commands
import bot_askshiro_voice
import bot_askshiro_text
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
    bot.loop.create_task(bot_askshiro_text.handle_openai_response_text(interaction, question))

@bot.tree.command(name="askshiro_with_voice")
async def askshiro_with_voice(interaction: discord.Interaction, question: str):
     # Schedule a coroutine to handle the OpenAI response
    bot.loop.create_task(bot_askshiro_voice.handle_openai_response_voice(interaction, question))

# Login to Discord with the bot's token.
bot.run(api_keys.token_key)

# Close the database connection when the bot shuts down
@bot.event
async def on_shutdown():
    print("---GOING TO SLEEP, BYE!---")
    global conn
    if conn is not None:
        conn.close()
