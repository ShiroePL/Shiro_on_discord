#For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 

import os
import azure.cognitiveservices.speech as speechsdk

def request_voice_fn(text):

# Creates an instance of a speech config with specified subscription key and service region.
    speech_key = "undefined"
    service_region = "undefined"
        #speech config
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    #speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    
    #audio config
    #audio_config = speechsdk.audio.AudioOutputConfig(filename="response.wav", use_default_speaker=True)


    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    speech_synthesis_voice_name='en-US-AshleyNeural'

    ssml = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="en-US-AshleyNeural"><prosody rate="3%" pitch="21%">""" + text + """</prosody></voice></speak>"""
   
    result = synthesizer.speak_ssml_async(ssml).get()

    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file("response.wav")
    
   

    # instantiate SpeechSynthesizer by passing your speech_config object and the audio_config object as parameters
    # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # speech_synthesizer.speak_text_async(text).get()


#text = "What is this **** and how can this be so ******?"
#request_voice_fn(text)
# def sprawdzam(tekst):
#     return "to jest to co jest w zmiennej tekst: " + tekst