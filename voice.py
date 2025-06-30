import asyncio
import os

import edge_tts
import playsound


def voices(voice='en-US-GuyNeural'):
    voices_list = [
        'en-US-GuyNeural',
        'uz-UZ-SardorNeural',
        'uz-UZ-MadinaNeural',
        'en-US-JennyNeural',
        'en-IN-NeerjaExpressiveNeural'
    ]
    if voice.isdigit():
        return voices_list[int(voice) - 1]
    return voice

async def tts(text,voice='en-US-GuyNeural'):
    communicate = edge_tts.Communicate(
        text,
        voices(voice)) # uz-UZ-SardorNeural|uz-UZ-MadinaNeural | en-US-JennyNeural | en-US-GuyNeural
    # indian => en-IN-NeerjaExpressiveNeural
    try:
        os.remove('voice.ogg')
    except:
        pass
    await communicate.save("voice.mp3")
    os.rename('voice.mp3', 'voice.ogg')
    return 'voice.ogg'


# import asyncio
# import edge_tts
#
# async def list_voices():
#     voices = await edge_tts.list_voices()
#     for voice in voices:
#         print(f"{voice['ShortName']} | {voice['Gender']} | {voice['Locale']} | {voice['FriendlyName']}")
#
# asyncio.run(list_voices())

if __name__ == '__main__':
    try:
        asyncio.run(tts('are you crazy  ?'))
    except KeyboardInterrupt:
        print("exit")
    except PermissionError:
        print("no permission")
