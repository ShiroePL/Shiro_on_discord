# the Discord Python API
import discord
import open_ai_api
import chatgpt_api
import connect_to_azuredb
import api_keys
import play_audio as play_audio
import request_voice_tts as request_voice
#import api_play_animation as play_animation
import subprocess
from discord.ext import commands
from discord import app_commands
from better_profanity import profanity
import asyncio
import os
import bot_askshiro_voice
import bot_askshiro_text
from embeds.introduce_embed import introduce_embed_fn
# This example requires the 'message_content' intent.

# intents = discord.Intents.default()
# intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


# Creating a commands.Bot() instance, and assigning it to "bot"
#bot = commands.Bot()

# When the bot is ready, run this code.
@bot.event
async def on_ready():
    print("The bot is Up and ready!")
    try:
        synced = await bot.tree.sync()
        print("synced")

        
    except Exception as e:
        print(e)


@bot.tree.command(name="introduce") #introduce embed
async def introduce(interaction: discord.Interaction):
    await interaction.response.send_message("Eghem, *deep breath*.", embed=introduce_embed_fn()) # Send the embed with some text



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

    #question_to_db = "User: " + question  #for Azure DB 
    # question = "User: " + question + " ->" #changing to format for open AI
    # async with interaction.channel.typing():
    
        #play animation first cause this is like 2 seconds
      #play_animation.play_animation_fn() #--------------audio related
        #play audio as subprocess to continue with the code and write answer on discord
        #answer = "to napisałem: " + question

    

    #subprocess.Popen(["python", "./play_audio.py"])  #--------------audio related

    

    #await interaction.response.send_message(answer)



# Login to Discord with the bot's token.
bot.run(api_keys.token_key)
































# @bot.event
# async def on_ready():
#     print(f'{bot.user} succesfully logged in!')

# @bot.event
# async def on_message(message):
#     # Make sure the Bot doesn't respond to it's own messages
#     if message.author == bot.user: 
#         return
    
#     if message.content == 'hello':
#         await message.channel.send(f'Hi {message.author}')
#     if message.content == 'bye':
#         await message.channel.send(f'Goodbye {message.author}')

#     await bot.process_commands(message)


# @bot.command()
# async def test(ctx, *, arg):
#     await ctx.send(arg)


# bot.run(api_keys.token_key)




# client = MyClient(intents=intents)
# client.run(api_keys.token_key)
