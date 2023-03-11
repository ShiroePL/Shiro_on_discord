import discord
import chatgpt_api
import connect_to_azuredb
import play_audio as play_audio
import request_voice_tts as request_voice
from better_profanity import profanity
import asyncio


async def handle_openai_response_voice(interaction):
    
    async with interaction.channel.typing():
            # Defer the response to let Discord know that the bot is still working
        await interaction.response.defer()
        try:
            if profanity.contains_profanity(question) == False: # if false in question then generate answer
                question_to_db = "Viewer: " + question  #for Azure DB   
                question = "Viewer: " + question #changing to format for open AI
                    # send to open ai for answer
                answer, prompt_tokens, completion_tokens, total_tokens = chatgpt_api.send_to_openai(question)

                if profanity.contains_profanity(answer) == False: # if false in answer then  
                        #send to azure db
                    connect_to_azuredb.connect_to_azuredb_fn(question_to_db, answer)
                    connect_to_azuredb.send_chatgpt_usage_to_database(prompt_tokens, completion_tokens, total_tokens)   
                        #tts request
                    request_voice.request_voice_fn(answer)
                        # Get the user who issued the command.
                    user = interaction.user
                        # Check if the user is in a voice channel.
                    if user.voice is None:
                        await interaction.followup.send("You are not in a voice channel! but here is answer: \n" + answer)
                        return
                        # Connect to the user's voice channel.
                    voice_client = await user.voice.channel.connect()
                        # Load the audio file and apply volume transformation.
                    audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='response.wav'), volume=0.5)
                        # Play the audio.
                    voice_client.play(audio_source)
                        # Send the response to the user.
                    await interaction.followup.send(answer)
                        # Wait until the audio finishes playing.
                    while voice_client.is_playing():
                        await asyncio.sleep(1)
                        # Disconnect from the voice channel.
                    await voice_client.disconnect()
                    #connect_to_azuredb.connect_to_azuredb_fn(question_to_db, answer)
                else:       # if answer contains some censored words
                    censored = profanity.censor(answer)
                        #send to azure db   
                    connect_to_azuredb.connect_to_azuredb_fn(question_to_db, censored)
                    connect_to_azuredb.send_chatgpt_usage_to_database(prompt_tokens, completion_tokens, total_tokens)
                    await interaction.followup.send("Hmm, my answer contains some censored words so I will not say it aloud. *writing on paper*: \n" + censored)
            else:
                await interaction.followup.send("Please don't use bad words in questions! I can't answer to that.", file=discord.File('pictures/shock_2.gif'))
        except Exception as e: 
            print(e)
            await interaction.followup.send("Oh, something crushed. Need to look at my logs *looking*", file=discord.File('pictures/shock_2.gif'))