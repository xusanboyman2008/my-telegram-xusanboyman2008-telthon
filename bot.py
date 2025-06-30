# from telethon.sync import TelegramClient
# from telethon.sessions import StringSession
#
# # Replace these with your own values
# api_id = 23564987
# api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
#
# phone_number = input().strip()
#
# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     client.start(phone=phone_number)
#     session_string = client.session.save()
#     print(session_string)
#
import asyncio
import random
from datetime import datetime

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from translator import translate
from voice import tts

# from database import add_bad_word, delete_bad_word, add_message, ready_messages, banned_words

api_id = 23564987
api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
string_session = os.getenv('TOKEN')
# string_session = '1ApWapzMBu1ZOtkPhhMz-yhOMhyOBuqasPrIa7CD1fmwYNRNKUDrISbhX3LyKp9MLHEubcLWtEUT_TSKPrYX7SfohSctemVx0gTZJNdi1T66D00m_Gi7W09hSfN84r3POKBfrM95m5ng8Hj9auRBFbZh1jBXjJtR37nQHpbfjMizDwwTNzices6d6OTCA8pb87TTn8LmNSYdOYqzYX3wvvJu5eF1ED3_uzg-iH-nxpUcmOOtoTAvgslVwqT8QAOYRdzvgsA4NmURmarTTXi9K2rEAUq-DAD6Fwi5hOUNIVi2mwMCyrCzj-1N0bST04ZgessUfGxyYgA8ZKSkMD9c9_bNryafiDB0='

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Dictionary to keep track of greeted users and their last greeting date
greeted_users = {}


def add_bad_word(new_word):
    with open('bad_words.txt', 'a', encoding='utf-8') as w:
        w.write(f'\n{new_word}')
        return True


def delete_bad_word(word_to_remove):
    with open('bad_words.txt', 'r+', encoding='utf-8') as d:
        lines = d.readlines()
        d.seek(0)
        d.truncate(0)
        d.writelines(line for line in lines if line.strip() != word_to_remove)


def banned_words():
    with open('bad_words.txt', 'r', encoding='utf-8') as f:
        return f.read().splitlines()


def ready_messages():
    with open('messages.txt', 'r', encoding='utf-8') as a:
        return a.read().splitlines()


def add_message(message, response):
    with open('messages.txt', 'a', encoding='utf-8') as w:
        w.write(f'\n{message} = {response}')


def remove_message(word_to_remove):
    with open('messages.txt', 'a', encoding='utf-8') as d:
        lines = d.readlines()
        d.seek(0)
        d.truncate(0)
        d.writelines(line for line in lines if line.split(' = ')[0].strip() != word_to_remove)


async def auto_delete_after_read(event, msg, user_id, timeout=300):
    try:
        for _ in range(timeout // 2):  # e.g., 300 seconds total
            dialogs = await client.get_dialogs()

            for d in dialogs:
                if hasattr(d.entity, 'id') and d.entity.id == user_id:
                    # ✅ Use d.dialog.read_outbox_max_id (raw dialog object)
                    if d.dialog.read_outbox_max_id >= msg.id:
                        await asyncio.sleep(2)
                        await event.delete()
                        return

            await asyncio.sleep(2)
    except Exception as e:
        pass


@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.out:
        if '/tr' == event.text[:3]:
            text = event.text[3:]
            target = text[:2]
            translation = await translate(text[2:], target)
            await event.edit(translation)
            return
        if '/voice' in event.text[:10]:
            await event.delete()

            text = event.text.split('/voice', 1)[1]
            number = '1'  # default voice index (change as needed)

            # Optional: extract voice number if format is "/voice_2Some text"
            if text and text[0] == '_':
                number = text[1]
                text = text[2:]

            await tts(text.strip(), number)

            if event.is_reply:
                original = await event.get_reply_message()
                if original:
                    await client.send_file(
                        event.chat_id,
                        file='voice.ogg',
                        reply_to=original.id,
                        voice_note=True
                    )
                    return

            # fallback if not a reply
            await client.send_file(
                event.chat_id,
                file='voice.ogg',
                reply_to=event.id,
                voice_note=True
            )
        if event.message.text.lower().startswith('/>:) '):
            new_word = event.message.text[len('/>:) '):].strip().lower()
            if new_word not in banned_words():
                add_bad_word(new_word)
                await event.reply(f'Taqiqlangan soz  "{new_word}" muafiqiyatli qoshildi')
            elif new_word in banned_words():
                await event.reply(f'Tanlangan soz "{new_word}" allaqachon yozilgan')
            else:
                await event.reply('qoshishga berilgan soz yo\'q')
            return
        if event.message.text.lower().startswith('/>:( '):
            new_word = event.message.text[len('/>:( '):].strip().lower()
            if new_word in banned_words():
                delete_bad_word(new_word)
                await event.reply(f'Taqiqlangan soz  "{new_word}" muafiqiyatli ochrirldi')
            elif new_word not in banned_words():
                await event.reply(f'Tanlangan soz "{new_word}" ozi yoq')
            else:
                await event.respond('qoshishga berilgan soz yo\'q')
            return
        if event.message.text.lower().startswith('/>:)_message '):
            new_word = event.message.text[len('/>:)_message '):].strip().lower()
            reply_message = new_word.split('=')
            b = []
            for i in ready_messages():
                b.append(i.split('='))
            if reply_message not in b:
                add_message(reply_message[0], reply_message[1])
                await event.reply(f'"{new_word}" muafiqiyatli qoshildi')
            elif reply_message in b:
                await event.reply(f'"{new_word}" allaqachon qoshilgan va ozgartirishga ruxsat yoq')
            return
        if event.message.text.lower().startswith('/>:(_message '):
            new_word = event.message.text[len('/>:(_message '):].strip().lower()
            if new_word in banned_words():
                remove_message(new_word)
                await event.reply(f'soz  "{new_word}" muafiqiyatli ochrirldi')
            elif new_word not in banned_words():
                await event.reply(f'soz "{new_word}" ozi yoq')
            else:
                await event.respond('qoshishga berilgan soz yo\'q')
            return


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    if sender.bot:
        return
    if event.is_private:
        user_id = event.sender_id
        current_date = datetime.now().date()

        # Check if the user has been greeted before today
        last_greeted = greeted_users.get(user_id)
        if last_greeted is None or last_greeted < current_date:
            auto_replies = [
                "👋 Assalomu alaykum! Men Xusanboy tomonidan yaratilgan botman. Xabaringizni oldim, imkon topib albatta javob beraman! 💬",
                "😊 Salom do‘stim! Men Xusanboy'ning aqlli botiman. Hozircha avtojavob bermoqdaman, tez orada sizga javob qaytaman. 🧠",
                "📩 Xush kelibsiz! Bu bot Xusanboy tomonidan tuzilgan. Habarni yozing — ko‘rib chiqib albatta javob beraman!",
                "👋 Salom! Men yordamchi botman. Xabaringiz menga yetib keldi — imkon topib javob yozaman. 💌",
                "🌟 Assalomu alaykum! Men Xusanboyning avtojavobchi botiman. Xabaringiz menga yetdi, birozdan so‘ng javob beraman. 🤖",
                "💬 Salom! Sizning xabaringizni oldim. Men Xusanboy tomonidan ishlab chiqilgan avtomatik yordamchiman. ✨",
                "🤗 Assalomu alaykum! Men Xusanboyning botiman. Tez orada aloqaga chiqaman, sabr qiling!",
                "📝 Salom do‘st! Habarni yuborganingiz uchun rahmat — ko‘rib chiqaman va tez orada javob beraman!",
                "💡 Salom! Men Xusanboy tomonidan tuzilgan avtojavobchi botman. Xabaringiz yozib olindi!",
                "👀 Assalomu alaykum! Sizning xabaringizni qabul qildim. Iloji boricha tez javob beraman. 🤝",
                "🚀 Salom! Men avtomatik yordamchi botman. Xabaringiz menga yetib keldi — javob kuting!",
                "🧾 Salom! Habar yuborganingiz uchun rahmat. Ilk imkoniyatda javob beraman!",
                "✨ Assalomu alaykum! Men Xusanboy tomonidan tuzilgan quvnoq botman. Xabaringiz yozib olindi. 😊",
                "🤖 Salom! Men yordamchi botman. Xabarni oldim, tez orada javob qaytaman!",
                "👐 Xush kelibsiz! Bu bot Xusanboy tomonidan yaratilgan. Habar qoldiring — tez orada aloqaga chiqaman.",
                "💬 Salom do‘st! Xabaringiz menga yetib keldi. Imkon topganimda javob beraman!",
                "💖 Assalomu alaykum! Men Xusanboyning sodiq yordamchi botiman. Habar yozing — ko‘rib chiqaman!",
                "🌈 Salom! Bu bot Xusanboy tomonidan ishlab chiqilgan. Xabaringizni oldim — yaqin orada aloqaga chiqaman.",
                "✉️ Salom! Xabaringizni oldim. Iloji boricha tez javob beraman!",
                "🙌 Assalomu alaykum! Men Xusanboy tomonidan yaratilgan avtomatik yordamchiman. Habar yuborganingiz uchun rahmat! 📬"
            ]

            await asyncio.sleep(2)
            await event.reply(random.choice(auto_replies))
            greeted_users[user_id] = current_date

        message_text = event.message.message.lower()
        if any(banned_word in message_text for banned_word in banned_words()):
            respectful_replies = [
                "🤖 Men yordam berishga tayyorman, lekin iltimos, 😊 hurmat bilan muloqot qilaylik.",
                "🙏 Hurmatli do‘stim, iltimos, xushmuomalalikni unutmang. Har doim sizga yordam berishga tayyorman!",
                "🧠 Men ham his qilaman 🙂 Keling, bir-birimizga hurmat bilan yondashaylik!",
                "💬 Men do‘stona insonman. Iltimos, muomala madaniyatiga rioya qilaylik 😊",
                "🤗 Sizga chin dildan yordam beraman! Faqat iltimos, hurmatni saqlaylik 🙏",
                "🙌 Suhbatimiz yoqimli bo‘lishi uchun, hurmatli tarzda gaplashaylik. Rahmat! 😊",
                "😊 Sizni diqqat bilan eshitaman. Iltimos, odobni unutmaylik.",
                "👂 Men har doim tinglashga tayyorman. Yaxshi muomala suhbatga chiroy qo‘shadi 🌟",
                "📩 Xabaringizni kutyapman. Faqatgina iltimos, hurmat saqlang 🙏",
                "💖 Men odobli muomalani qadrlayman. Sizdan ham shuni kutaman 😊",
                "🌟 Har bir so‘z muhim. Keling, bir-birimizga nisbatan odobli bo‘laylik!",
                "📢 Yaxshi muloqot — hurmatli suhbatdan boshlanadi. Men esa har doim sizga ochiqman 🤝",
                "👋 Assalomu alaykum! Yaxshi so‘z qalbni ochadi. Keling, samimiy gaplashaylik 😊",
                "📚 Bilimli va madaniyatli bo‘lish har birimizning burchimiz. Iltimos, hurmatni saqlang 🙌",
                "🙋‍♂️ Men Xusanboyman, siz bilan yaxshi muloqot qilishni istayman. Iltimos, xushmuomala bo‘laylik 😊"
            ]

            # Example usage in Telethon:
            await asyncio.sleep(2)
            reply = await event.reply(random.choice(respectful_replies))
            asyncio.create_task(auto_delete_after_read(event, reply, user_id))
        for ready_message in ready_messages():
            parts = ready_message.split('=', 1)
            if len(parts) != 2:
                continue  # skip invalid lines
            key, reply = parts[0].strip(), parts[1].strip()

            if f' {key}' in f" {message_text}":
                await event.respond(reply)
                break  # stop after first match


with client:
    client.run_until_disconnected()
