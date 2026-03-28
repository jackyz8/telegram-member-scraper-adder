from telethon import TelegramClient, errors
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
import csv
import asyncio
from dotenv import load_dotenv
import os

# 🔥 FORCE LOAD ENV (FIX)
load_dotenv(dotenv_path=".env")

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

# ✅ CHECK ENV VALUES
if not api_id or not api_hash:
    print("❌ ERROR: API_ID or API_HASH not found in .env file!")
    exit()

api_id = int(api_id)

client = TelegramClient("session", api_id, api_hash)

print("=" * 70)
print("IMPORTANT WARNING & TERMS OF USE:")
print("=" * 70)

confirm = input("\nDo you accept? (yes/no): ").strip().lower()
if confirm != 'yes':
    exit()

target_group = input("\nEnter group username/link: ").strip()

if not target_group.startswith("@"):
    target_group = "@" + target_group.split("/")[-1]

admin_check = input("Are you admin? (yes/no): ").strip().lower()
if admin_check != 'yes':
    print("❌ You must be admin!")
    exit()

async def main():
    await client.start()

    try:
        group = await client.get_entity(target_group)
        print(f"✅ Group: {group.title}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    csv_path = "csv/members.csv"

    if not os.path.exists(csv_path):
        print("❌ CSV file not found!")
        return

    success = 0
    fail = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for username, user_id in reader:
            try:
                if username:
                    user = await client.get_entity(username)
                else:
                    user = InputPeerUser(int(user_id), 0)

                await client(InviteToChannelRequest(group, [user]))
                print(f"✅ Added: {username or user_id}")
                success += 1

                await asyncio.sleep(30)

            except errors.FloodWaitError as e:
                print(f"⏳ Wait {e.seconds}s")
                await asyncio.sleep(e.seconds)

            except Exception as e:
                print(f"❌ Failed: {username or user_id}")
                fail += 1

    print("\n🎯 DONE")
    print(f"Success: {success}")
    print(f"Failed: {fail}")

with client:
    client.loop.run_until_complete(main())
