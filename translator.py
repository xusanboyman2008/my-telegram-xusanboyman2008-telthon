# from googletrans import Translator
# import datetime
# def translate(text, target_lang='uz'):
#     translator = Translator()
#     result = translator.translate(text, dest=target_lang)
#     return result.text
#
# if __name__ == "__main__":
#     translated = translate('hi there', "uz")
#     print("Translated:", translated,'\ntime:', end-stt)
# # # #
import aiohttp
import asyncio
import urllib.parse

from langdetect import detect


async def translate(text, target_lang="uz"):
    source_lang = detect(text)
    encoded_text = urllib.parse.quote(text)
    url = f"https://lingva.ml/api/v1/{source_lang}/{target_lang}/{encoded_text}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            return result["translation"]

# Test
if __name__ == "__main__":
        translated = asyncio.run(translate("/truz guy's you are luck each season you go somewhere with your all co-workers i think it should be amazing. how can give you a such vacation to you", "uz"))
        print("Translated:", translated)
