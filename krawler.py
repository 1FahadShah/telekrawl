import os
import json
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from tqdm.asyncio import tqdm as async_tqdm

# ===== CONFIG =====
api_id = 12345678          # Replace with your api_id
api_hash = 'your_api_hash' # Replace with your api_hash
phone = '+919876543210'     # Your phone number with country code
    
DOWNLOAD_PATH = 'downloads'
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

client = TelegramClient('tg_session', api_id, api_hash)

async def scan_channel(dialog, last_id=0):
    """Scan channel to count total messages and total media (photos/videos)."""
    total_messages = 0
    total_media = 0
    async for message in client.iter_messages(dialog.entity, reverse=True):
        if message.id <= last_id:
            continue
        total_messages += 1
        if message.media:
            total_media += 1
    return total_messages, total_media

async def download_channel(dialog):
    channel = dialog.entity
    folder_name = f"{channel.id}_{channel.title.replace('/', '_')}"
    channel_folder = os.path.join(DOWNLOAD_PATH, folder_name)
    os.makedirs(channel_folder, exist_ok=True)

    messages_json = os.path.join(channel_folder, 'messages.json')
    last_id_file = os.path.join(channel_folder, 'last_id.txt')

    last_id = 0
    if os.path.exists(last_id_file):
        with open(last_id_file, 'r') as f:
            last_id = int(f.read().strip())

    total_messages, total_media = await scan_channel(dialog, last_id)
    print(f"\n🔹 Downloading messages from: {channel.title}")
    print(f"Found: No. of Messages: {total_messages}, No. of Photos & Videos: {total_media}\n")

    all_messages = []
    new_last_id = last_id

    # Phase 1: Download messages (text only) and save immediately
    async for message in async_tqdm(client.iter_messages(channel, reverse=True),
                                    total=total_messages,
                                    desc=f"Downloading messages",
                                    unit="msg"):
        if message.id <= last_id:
            continue

        all_messages.append({
            'id': message.id,
            'date': str(message.date),
            'sender_id': message.sender_id,
            'text': message.text,
            'media': True if message.media else None
        })

        # Update last_id
        if message.id > new_last_id:
            new_last_id = message.id

        # Save messages.json after each message (or you can batch after N messages)
        with open(messages_json, 'w', encoding='utf-8') as f:
            json.dump(all_messages, f, indent=2)

        await asyncio.sleep(0.01)

    # Update last_id after messages
    with open(last_id_file, 'w') as f:
        f.write(str(new_last_id))

    print(f"✅ Messages for '{channel.title}' saved successfully.")

    # Phase 2: Download media separately and update JSON as you go
    media_messages = [m for m in all_messages if m['media']]
    for m in async_tqdm(media_messages, desc="Downloading media", unit="file"):
        try:
            msg_obj = await client.get_messages(channel, ids=m['id'])
            media_path = await msg_obj.download_media(file=channel_folder)
            m['media'] = os.path.basename(media_path) if media_path else None
        except FloodWaitError as e:
            print(f"\n⏳ FloodWait hit. Sleeping {e.seconds}s...")
            await asyncio.sleep(e.seconds + 1)
        except Exception as e:
            print(f"\n❌ Error downloading media for message {m['id']}: {e}")
            m['media'] = None

        # Save JSON after each media download
        with open(messages_json, 'w', encoding='utf-8') as f:
            json.dump(all_messages, f, indent=2)

        await asyncio.sleep(0.01)

    print(f"\n✅ Channel '{channel.title}' updated with {len(all_messages)} messages and media downloaded.\n")
    return folder_name, channel.title


async def main():
    await client.start(phone)

    # Step 1: List all channels
    dialogs = [d for d in await client.get_dialogs() if d.is_channel]
    print("\n🔹 Channels your account is in:\n")
    for i, d in enumerate(dialogs):
        print(f"[{i}] {d.name}")

    # Step 2: Let user select channels
    selections = input("\nEnter channel numbers to download (comma-separated, e.g., 0,2,5): ")
    selected_indexes = [int(x.strip()) for x in selections.split(",")]

    # --- START OF FIX ---

    channels_json_path = os.path.join(DOWNLOAD_PATH, 'channels.json')

    # 1. Load existing channel data if the file exists
    if os.path.exists(channels_json_path):
        with open(channels_json_path, 'r', encoding='utf-8') as f:
            try:
                channels_info = json.load(f)
            except json.JSONDecodeError:
                channels_info = []  # If file is corrupted, start with an empty list
    else:
        channels_info = []

    # 2. Create a set of existing folder names for a fast check to avoid duplicates
    existing_folders = {c['folder'] for c in channels_info}

    # Step 3: Download selected channels
    for idx in selected_indexes:
        if 0 <= idx < len(dialogs):
            dialog = dialogs[idx]
            folder_name, title = await download_channel(dialog)

            # 3. Only add the new channel if it's not already in the list
            if folder_name not in existing_folders:
                channels_info.append({'folder': folder_name, 'title': title})
                existing_folders.add(folder_name)
                print(f"Added '{title}' to channels.json.")
            else:
                print(f"'{title}' already exists in channels.json. Skipping.")

            await asyncio.sleep(1.5)
        else:
            print(f"⚠️ Index {idx} is invalid. Skipping.")


    # 4. Save the updated, complete list back to the file
    with open(channels_json_path, 'w', encoding='utf-8') as f:
        json.dump(channels_info, f, indent=2)

    # --- END OF FIX ---

    print("\n🎯 Selected channels completed!")

with client:
    client.loop.run_until_complete(main())
