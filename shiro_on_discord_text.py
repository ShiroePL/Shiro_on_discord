import discord
import open_ai_api
import connect_to_azuredb
import api_keys
import play_audio as play_audio
import request_voice_tts as request_voice
import api_play_animation as play_animation
import subprocess


class MyClient(discord.Client):

  def __init__(self):
    # adding intents module to prevent intents error in __init__ method in newer versions of Discord.py
    intents = discord.Intents.default(
    )  # Select all the intents in your bot settings as it's easier
    intents.message_content = True
    super().__init__(intents=intents)
    
  async def on_ready(self):
    # print out information when the bot wakes up
    print('Logged in as')
    print(self.user.name)
    print(self.user.id)
    print('------')
    # send a request to the model without caring about the response

  async def on_message(self, message):
  #async def test(ctx, arg):  
    #message = arg
    """
        this function is called whenever the bot sees a message in a channel
        """
    # ignore the message if it comes from the bot itself
    if message.author.id == self.user.id:
      return
    
    # form query payload with the content of the message
    payload = {'inputs': {'text': message.content}}

    #sending question to open ai
    question = "User: " + message.content + " ->"
    question_to_db = "User: " + message.content
    # while the bot is waiting on a response from openai
    # set the its status as typing for user-friendliness
    async with message.channel.typing():
      answer = open_ai_api.send_to_openai(question) #taking answer from openAIS
        #send to azure tts
      #request_voice.request_voice_fn(answer) #--------------audio related
        #play animation first cause this is like 2 seconds
      #play_animation.play_animation_fn() #--------------audio related
        #play audio as subprocess to continue with the code and write answer on discord
      # if message.content.startswith('$hello'):
      #   answer = "to napisałem: " + message.content

      
      #subprocess.Popen(["python", "./play_audio.py"])  #--------------audio related
    
    bot_response = answer

    # if error
    if not answer:
      if 'error' in answer:
        bot_response = '`Error: {}`'.format(answer['error'])
      else:
        bot_response = 'Hmm... something is not right.'

    # send the model's response to the Discord channel
    #connect_to_azuredb.connect_to_azuredb_fn(question_to_db, bot_response) #SENDING TO AZURE DB
    #send response to discord
    await message.channel.send(bot_response)

   
client = MyClient()
client.run(api_keys.token_key)



