from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import os
import time
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg

# Initialize Pyrogram Client
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")  # Replace with your API ID
API_HASH = os.getenv("API_HASH")  # Replace with your API Hash

app = Client("pdf_genie", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

ABOUT_TXT = """<b><blockquote>⍟───[ MY ᴅᴇᴛᴀɪʟꜱ ]───⍟</blockquote>
    
‣ ᴍʏ ɴᴀᴍᴇ : <a href='https://t.me/PDF_Genie_Robot'>PDF Genie</a>
‣ ᴍʏ ʙᴇsᴛ ғʀɪᴇɴᴅ : <a href='tg://settings'>ᴛʜɪs ᴘᴇʀsᴏɴ</a> 
‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/Ur_amit_01'>ꫝᴍɪᴛ ꢺɪɴɢʜ ⚝</a> 
‣ ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ</a> 
‣ ʟᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/download/releases/3.0/'>ᴘʏᴛʜᴏɴ 3</a> 
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a> 
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ2.7.1 [sᴛᴀʙʟᴇ]</b>"""

# Start command
@app.on_message(filters.command("start"))
async def start(client, message):
    # Send a sticker first
    sticker_id = "CAACAgUAAxkBAAECEpdnLcqQbmvQfCMf5E3rBK2dkgzqiAACJBMAAts8yFf1hVr67KQJnh4E"
    sticker_message = await message.reply_sticker(sticker_id)
    time.sleep(2)
    await sticker_message.delete()

    # Define the inline keyboard with buttons
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("«ʜᴇʟᴘ» 🕵️", callback_data="help"),
            InlineKeyboardButton("«ᴀʙᴏᴜᴛ» 📄", callback_data="about")
        ],
        [InlineKeyboardButton("•Dᴇᴠᴇʟᴏᴘᴇʀ• ☘", url="https://t.me/Ur_amit_01")]
    ])
    image_url = "https://graph.org/file/0f1d046b4b3899e1812bf-0e63e80abb1bef1a8b.jpg"
    caption = "Aʜ, ᴀ ɴᴇᴡ ᴛʀᴀᴠᴇʟᴇʀ ʜᴀs ᴀʀʀɪᴠᴇᴅ... Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍʏ ᴍᴀɢɪᴄᴀʟ ʀᴇᴀʟᴍ !🧞‍♂️✨\n\n• I ᴀᴍ PDF ɢᴇɴɪᴇ, ɪ ᴡɪʟʟ ɢʀᴀɴᴛ ʏᴏᴜʀ ᴘᴅғ ᴡɪsʜᴇs! 📑🪄"
    await message.reply_photo(image_url, caption=caption, reply_markup=markup)

# Callback query handler
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    if data == "help":
        new_caption = "Hᴇʀᴇ Is Tʜᴇ Hᴇʟᴘ Fᴏʀ Mʏ Cᴏᴍᴍᴀɴᴅs.:\n1. Send PDF files.\n2. Use /merge when you're ready to combine them.\n3. Max size = 20MB per file.\n\n• Note: My developer is constantly adding new features in my program, if you found any bug or error please report at @Ur_Amit_01"
        new_image_url = "https://graph.org/file/0f1d046b4b3899e1812bf-0e63e80abb1bef1a8b.jpg"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]])
    elif data == "about":
        new_caption = ABOUT_TXT
        new_image_url = "https://graph.org/file/0f1d046b4b3899e1812bf-0e63e80abb1bef1a8b.jpg"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]])
    elif data == "back":
        new_caption = "Aʜ, ᴀ ɴᴇᴡ ᴛʀᴀᴠᴇʟᴇʀ ʜᴀs ᴀʀʀɪᴠᴇᴅ... Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍʏ ᴍᴀɢɪᴄᴀʟ ʀᴇᴀʟᴍ !🧞‍♂️✨\n\n• I ᴀᴍ PDF ɢᴇɴɪᴇ, ɪ ᴡɪʟʟ ɢʀᴀɴᴛ ʏᴏᴜʀ ᴘᴅғ ᴡɪsʜᴇs! 📑🪄"
        new_image_url = "https://graph.org/file/0f1d046b4b3899e1812bf-0e63e80abb1bef1a8b.jpg"
        markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("«ʜᴇʟᴘ» 🕵️", callback_data="help"),
                InlineKeyboardButton("«ᴀʙᴏᴜᴛ» 📄", callback_data="about")
            ],
            [InlineKeyboardButton("•Dᴇᴠᴇʟᴏᴘᴇʀ• ☘", url="https://t.me/Ur_amit_01")]
        ])
    else:
        return

    # Edit the message with the updated content
    await callback_query.edit_message_media(
        InputMediaPhoto(new_image_url, caption=new_caption, parse_mode="HTML"),
        reply_markup=markup
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups/Channels : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
