# from telethon.sync import TelegramClient
# from telethon.sessions import StringSession
#
# # Replace these with your own values
# api_id = 23564987
# api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
#
# print("Enter your phone number:")
# phone_number = input().strip()
#
# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     client.start(phone=phone_number)
#     session_string = client.session.save()
#     print(f'Session string: {session_string}')
#
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime
import random
# from database import add_bad_word, delete_bad_word, add_message, ready_messages, banned_words

api_id = 23564987
api_hash = 'a3a5bf88d985dbf6b39ecb8a8283b33b'
string_session = '1ApWapzMBu3JZJLSYGJywWdlEA_2Lkr4yz_a_twSGd4-o3ZN9vp3CnAzp9kZ-OiJp3Gg26GoBlBFuPjcHjluGx7RNPww2DbLE4OOq0HSya2I2PHIad3xUWx0hdgapkT3WczBm3CQNyjBzjEIJlxsNzDsx6eIjsI3OWCWxtNp4BD1mSlV1ihjrtbicNxbMUwg1VCf_An8ymvMhJzvfW0Zhz0DZCT2DFCmjCOFRs1sBwhY1oaSFx4YaPeDNjoiMIvAigV9YxtNwJUjbEh4B0HklJIquaqam4mjTHQwdg75DwL_STN5rXCIjMGSErs6fuAGsIhoPJ4H5qOflV6AxrllqWMxaEM88oS0='

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


def add_message(message,response):
    with open('messages.txt', 'a', encoding='utf-8') as w:
        w.write(f'\n{message} = {response}')

async def auto_delete_after_read(event,msg, user_id, timeout=300):
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
        print(f"[Error in auto_delete_after_read] {e}")

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        user_id = event.sender_id
        current_date = datetime.now().date()


        # Check if the user has been greeted before today
        last_greeted = greeted_users.get(user_id)
        if last_greeted is None or last_greeted < current_date:

            auto_replies = [
                "👋 Assalomu alaykum! Men Xusanboy tomonidan yaratilgan avtojavob botiman. Xabaringizni yuboring, albatta javob beraman! 💬",
                "😊 Salom do‘stim! Men Xusanboy'ning aqlli botiman. Nima yordam kerak? 🧠",
                "📩 Xush kelibsiz! Men Xusanboyning avtojavob tizimiman. Yozing, kutyapman!",
                "👋 Salom! Men sizga yordam berishga tayyorman. Xabar qoldiring! 💌",
                "🌟 Assalomu alaykum! Xush kelibsiz! Xabaringizni kutyapman. 🤖",
                "💬 Salom! Men avtomatik yordamchiman. Xabaringiz muhim! ✨",
                "🤗 Assalomu alaykum! Bot Xusanboy tomonidan tuzilgan. Qanday yordam bera olaman?",
                "📝 Salom do‘st! Xabaringizni yuboring, sizga tez orada javob beraman!",
                "💡 Salom! Men avtojavob botiman. Yozing, savolingizni kutyapman!",
                "👀 Assalomu alaykum! Menga yozing, sizga yordam beraman. 🤝",
                "🚀 Salom! Men avtomatik javob beruvchi botman. Nima haqida yozmoqchisiz?",
                "🧾 Salom! Xabar qoldiring, imkon qadar tez javob beraman!",
                "✨ Assalomu alaykum! Men Xusanboy tomonidan yaratilgan do‘stona botman. 😊",
                "🤖 Salom! Men sizga xizmat ko‘rsatish uchun shu yerdaman. Xabaringizni kutaman!",
                "👐 Xush kelibsiz! Men yordam berishga tayyor botman. Yozing!",
                "💬 Salom do‘st! Xabaringizni yuboring — javob qaytarishga tayyorman!",
                "💖 Assalomu alaykum! Men Xusanboyning sodiq botiman. Xabaringizni kutyapman!",
                "🌈 Salom! Bot Xusanboy tomonidan ishlab chiqilgan. Nima haqida suhbatlashamiz?",
                "✉️ Salom! Men sizga yordam berish uchun shu yerdaman. Xabaringizni yuboring!",
                "🙌 Assalomu alaykum! Men avtomatik botman, sizga yordam berishga tayyorman. 📬"
            ]

            # Example usage in Telethon:
            await asyncio.sleep(2)
            await event.reply(random.choice(auto_replies))
            greeted_users[user_id] = current_date

        message_text = event.message.message.lower()
        if event.message.text.lower().startswith('/>:) '):
            new_word = event.message.text[len('/>:) '):].strip().lower()
            if new_word not in banned_words():
                add_bad_word(new_word)
                await event.reply(f'Taqiqlangan soz  "{new_word}" muafiqiyatli qoshildi')
            elif new_word in banned_words():
                await event.reply(f'Tanlangan soz "{new_word}" allaqachon yozilgan')
            else:
                await event.reply('qoshishga berilgan soz yo\'q')
        if event.message.text.lower().startswith('/>:( '):
            new_word = event.message.text[len('/>:( '):].strip().lower()
            if new_word in banned_words():
                delete_bad_word(new_word)
                await event.reply(f'Taqiqlangan soz  "{new_word}" muafiqiyatli ochrirldi')
            elif new_word not in banned_words():
                await event.reply(f'Tanlangan soz "{new_word}" ozi yoq')
            else:
                await event.respond('qoshishga berilgan soz yo\'q')
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
            asyncio.create_task(auto_delete_after_read(event,reply, user_id))
        if event.message.text.lower().startswith('/>:)_message '):
            new_word = event.message.text[len('/>:)_message '):].strip().lower()
            reply_message = new_word.split('=')
            b = []
            for i in ready_messages():
                b.append(i.split('='))
            if reply_message not in b:
                    add_message(reply_message[0],reply_message[1])
                    await event.reply(f'"{new_word}" muafiqiyatli qoshildi')
            elif reply_message in b:
                    await event.reply(f'"{new_word}" allaqachon qoshilgan va ozgartirishga ruxsat yoq')
        for ready_message in ready_messages():
            parts = ready_message.split('=', 1)
            if len(parts) != 2:
                continue  # skip invalid lines
            key, reply = parts[0].strip(), parts[1].strip()
            if key in message_text:
                await event.respond(reply)
                break  # stop after first match

with client:
    print("Client is running...")
    client.run_until_disconnected()
