from playsound import playsound


def play_audio_fn():
    try:
        playsound('response.wav')
        print("Playing voice")
    except:
        print("Error or ended reading audio.")


import pygame

# def play_audio_fn():
#     pygame.mixer.init()
#     pygame.mixer.music.load("./azure_tts/response.wav")
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy() == True:
#         continue

# from pydub import AudioSegment
# from pydub.playback import play

# def play_audio_fn():
#     sound = AudioSegment.from_wav("./azure_tts/response.wav")
#     play(sound)

play_audio_fn()
#play_audio_fn()
