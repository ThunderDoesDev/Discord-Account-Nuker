import aiohttp
import discord
import asyncio
import logging
from datetime import datetime
from tqdm import tqdm

logging.basicConfig(
    filename=f'account_nuker.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

intents = discord.Intents.all()
client = discord.Client(intents=intents, self_bot=True)
token = None

def display_banner():
    print("""                                                                                                                
    █████████                                                     █████       ██████   █████            █████                        
  ███░░░░░███                                                   ░░███       ░░██████ ░░███            ░░███                         
 ░███    ░███   ██████   ██████   ██████  █████ ████ ████████   ███████      ░███░███ ░███  █████ ████ ░███ █████  ██████  ████████ 
 ░███████████  ███░░███ ███░░███ ███░░███░░███ ░███ ░░███░░███ ░░░███░       ░███░░███░███ ░░███ ░███  ░███░░███  ███░░███░░███░░███
 ░███░░░░░███ ░███ ░░░ ░███ ░░░ ░███ ░███ ░███ ░███  ░███ ░███   ░███        ░███ ░░██████  ░███ ░███  ░██████░  ░███████  ░███ ░░░ 
 ░███    ░███ ░███  ███░███  ███░███ ░███ ░███ ░███  ░███ ░███   ░███ ███    ░███  ░░█████  ░███ ░███  ░███░░███ ░███░░░   ░███     
 █████   █████░░██████ ░░██████ ░░██████  ░░████████ ████ █████  ░░█████     █████  ░░█████ ░░████████ ████ █████░░██████  █████    
░░░░░   ░░░░░  ░░░░░░   ░░░░░░   ░░░░░░    ░░░░░░░░ ░░░░ ░░░░░    ░░░░░     ░░░░░    ░░░░░   ░░░░░░░░ ░░░░ ░░░░░  ░░░░░░  ░░░░░     
                                                      by ThunderDoesDev
""")
    print("---------------------------------------------------")
    print("                 OPTIONS MENU                     ")
    print("---------------------------------------------------")
    print("1. Show Account Info")
    print("2. Leave or Delete Guilds")
    print("3. Delete Friends")
    print("4. Delete DMs")
    print("5. Full Nuke (All actions)")
    print("---------------------------------------------------")

async def display_info():
    logging.info("Displaying account info.")
    print(f"\nAccount Information:")
    print(f"Username: {client.user.name}#{client.user.discriminator}")
    print(f"User ID: {client.user.id}")
    print(f"Email: {client.user.email if client.user.email else 'No email set'}")
    print(f"Phone: {client.user.phone if client.user.phone else 'No phone number set'}")
    print(f"Verified: {client.user.verified}")
    logging.info(f"Account Info: {client.user.name}#{client.user.discriminator}, ID: {client.user.id}")
    print("\nPayment Sources:")
    try:
        payment_sources = await client.http.request(discord.http.Route('GET', '/users/@me/billing/payment-sources'))
        if payment_sources:
            for source in payment_sources:
                print(f"Payment Type: {source['type']}")
                print(f"Last 4 Digits: {source['last_4']}")
                print(f"Expires: {source['expires_month']}/{source['expires_year']}")
                print(f"Billing Address: {source['billing_address']['country']}")
                logging.info(f"Payment Source: {source['type']}, Last 4: {source['last_4']}, Expires: {source['expires_month']}/{source['expires_year']}, Billing Country: {source['billing_address']['country']}")
        else:
            print("No payment sources found.")
            logging.info("No payment sources found.")
    except Exception as e:
        logging.error(f"Failed to retrieve payment sources: {str(e)}")
    print("\nBilling Information:")
    try:
        billing_info = await client.http.request(discord.http.Route('GET', '/users/@me/billing/payment-sources'))
        if billing_info:
            for info in billing_info:
                print(f"Billing Type: {info['type']}")
                print(f"Country: {info['billing_address']['country']}")
                print(f"Last 4 Digits: {info['last_4']}")
                print(f"Expires: {info['expires_month']}/{info['expires_year']}")
                logging.info(f"Billing Info: Type: {info['type']}, Country: {info['billing_address']['country']}, Last 4: {info['last_4']}, Expires: {info['expires_month']}/{info['expires_year']}")
        else:
            print("No billing information found.")
            logging.info("No billing information found.")
    except Exception as e:
        logging.error(f"Failed to retrieve billing information: {str(e)}")
    print("\nSubscription Information:")
    try:
        subscriptions = await client.http.request(discord.http.Route('GET', '/users/@me/billing/subscriptions'))
        if subscriptions:
            for sub in subscriptions:
                print(f"Subscription Type: {sub['type']}")
                print(f"Status: {sub['status']}")
                print(f"Current Period End: {sub['current_period_end']}")
                logging.info(f"Subscription: Type: {sub['type']}, Status: {sub['status']}, Period End: {sub['current_period_end']}")
        else:
            print("No active subscriptions.")
            logging.info("No active subscriptions.")
    except Exception as e:
        logging.error(f"Failed to retrieve subscription information: {str(e)}")
    print("\nReturning to the main menu...\n")
    main()

async def fetch_guilds(token):
    base_url = "https://discord.com/api/v9"
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"{base_url}/users/@me/guilds", headers=headers)
        if response.status == 200:
            guilds = await response.json()
            if guilds:
                logging.info(f"Fetched {len(guilds)} guilds.")
                return guilds
            else:
                logging.warning("No guilds found.")
                return None
        else:
            logging.error(f"Failed to fetch guilds (status code: {response.status})")
            return None

async def leave_guild(token, guild):
    guild_id = str(guild['id'])
    guild_name = guild['name']
    headers = {"Authorization": token}
    base_url = f"https://discord.com/api/v9"    
    async with aiohttp.ClientSession() as session:
        response = await session.delete(f"{base_url}/users/@me/guilds/{guild_id}", headers=headers)    
    if response.status in [200, 204]:
        logging.info(f"Left guild: {guild_name}")
        return True
    elif response.status == 429:
        retry_after = await response.json()
        logging.warning(f"Rate limited. Retrying after {retry_after['retry_after']} seconds...")
        await asyncio.sleep(retry_after['retry_after'])
        return await leave_guild(token, guild)  # Proper recursive call with token and guild
    else:
        error_text = await response.text()
        logging.error(f"Failed to leave guild: {guild_name} (status code: {response.status}, error: {error_text})")
        return False

async def delete_guild(session, guild, headers):
    guild_id = guild['id']
    guild_name = guild['name']
    url = f"https://discord.com/api/v9/guilds/{guild_id}"
    response = await session.delete(url, headers=headers)
    if response.status in [200, 204]:
        logging.info(f"Deleted guild: {guild_name}")
        return True
    elif response.status == 429:
        retry_after = await response.json()
        logging.warning(f"Rate limited. Retrying after {retry_after['retry_after']} seconds...")
        await asyncio.sleep(retry_after['retry_after'])
        return await delete_guild(session, guild, headers)
    else:
        logging.error(f"Failed to delete guild: {guild_name} (status code: {response.status})")
        return False

async def process_guilds(token):
    guilds = await fetch_guilds(token)
    if guilds and len(guilds) > 0:
        leave_count, delete_count = 0, 0        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": token}
            leave_guilds = [guild for guild in guilds if not guild['owner']]
            leave_results = []
            for guild in tqdm(leave_guilds, desc="Leaving guilds"):
                result = await leave_guild(token, guild)
                leave_results.append(result)
                leave_count += result
            logging.info(f"Processed {len(leave_results)} leave actions, Success: {leave_count}")
            delete_guilds = [guild for guild in guilds if guild['owner']]
            delete_results = []
            for guild in tqdm(delete_guilds, desc="Deleting guilds"):
                result = await delete_guild(session, guild, headers)
                delete_results.append(result)
                delete_count += result
            logging.info(f"Processed {len(delete_results)} delete actions, Success: {delete_count}")
    else:
        logging.info("No guilds to process.")

async def close_all_dms(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    base_url = "https://discord.com/api/v9"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/users/@me/channels", headers=headers) as response:
                if response.status == 200:
                    dms_data = await response.json()
                    total_dms = len(dms_data)
                    deleted_dms = 0
                    print(f"Deleting {total_dms} DMs...")
                    for dm in tqdm(dms_data, desc="Deleting DMs"):
                        try:
                            channel_id = dm['id']
                            async with session.delete(f"{base_url}/channels/{channel_id}", headers=headers) as delete_response:
                                if delete_response.status in [200, 204]:
                                    logging.info(f"Deleted DM: {channel_id}")
                                    deleted_dms += 1
                                elif delete_response.status == 420:  
                                    retry_after = await delete_response.json()  
                                    logging.warning(f"Rate limited. Retrying after {retry_after['retry_after']} seconds...")
                                    await asyncio.sleep(retry_after['retry_after'])
                                    await close_all_dms(session, base_url, headers, token) 
                                else:
                                    logging.error(f"Failed to delete DM: {channel_id} (status: {delete_response.status})")
                        except Exception as e:
                            logging.error(f"Error deleting DM {channel_id}: {str(e)}")
                    if deleted_dms == total_dms:
                        logging.info("All DMs were successfully deleted.")
                    else:
                        logging.warning(f"Only {deleted_dms} out of {total_dms} DMs were deleted.")
                else:
                    logging.error(f"Failed to fetch DMs (status code: {response.status})")
        except Exception as e:
            logging.error(f"Error fetching DMs: {str(e)}")

async def remove_all_friends(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    base_url = "https://discord.com/api/v9"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/users/@me/relationships", headers=headers) as response:
                if response.status == 200:
                    friends_data = await response.json()
                    total_friends = len(friends_data)
                    removed_friends = 0
                    print(f"Removing {total_friends} friends...")
                    for friend in tqdm(friends_data, desc="Removing Friends"):
                        try:  
                            if friend['type'] == 1:
                                friend_id = friend['id']
                                async with session.delete(f"{base_url}/users/@me/relationships/{friend_id}", headers=headers) as delete_response:
                                    if delete_response.status in [200, 204]:
                                        removed_friends += 1
                                        logging.info(f"Removed friend: {friend['user']['username']}")
                                    elif delete_response.status == 420:  
                                        retry_after = await delete_response.json()  
                                        logging.warning(f"Rate limited. Retrying after {retry_after['retry_after']} seconds...")
                                        await asyncio.sleep(retry_after['retry_after'])
                                        await remove_all_friends(session, base_url, headers, token) 
                                    else:
                                        logging.error(f"Failed to remove friend: {friend['user']['username']} (status: {delete_response.status})")
                        except Exception as e:
                            logging.error(f"Error removing friend {friend['user']['username']}: {str(e)}")
                    if removed_friends == total_friends:
                        logging.info("All friends were successfully removed.")
                        print("All friends were successfully removed.")
                    else:
                        logging.warning(f"Only {removed_friends} out of {total_friends} friends were removed.")
                        print(f"Only {removed_friends} out of {total_friends} friends were removed.")
                else:
                    logging.error(f"Failed to fetch friends (status code: {response.status})")
        except Exception as e:
            logging.error(f"Error fetching friends: {str(e)}")

async def nuke_all():
    logging.info("Executing full nuke (servers, DMs, friends, profile).")
    print("Nuking everything...")
    await process_guilds(token)
    await close_all_dms(token)
    await remove_all_friends(token)

def confirm_choice():
    confirmation = input("Type 'Confirm' to process or 'Cancel' to return to the main menu: ")
    if confirmation.lower() == "confirm":
        return True
    elif confirmation.lower() == "cancel":
        print("Returning to the main menu...")
        logging.info("User canceled the operation.")
        main()
    else:
        print("Invalid input. Returning to main menu.")
        logging.warning("Invalid input during confirmation.")
        main()

async def nuke_options(option, token):
    try:
        if option == '1':
            await display_info()
        elif option == '2':
            await process_guilds(token)
        elif option == '3':
            await remove_all_friends(token)
        elif option == '4':
             await close_all_dms(token)
        elif option == '5':
            await nuke_all()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    print("\nReturning to the main menu...\n")
    main()

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')
    print(f'Logged in as {client.user}')
    await nuke_options(option, token)

# Main flow
def main():
    display_banner()
    global option
    option = input("Choose an option (1-5): ")
    global token
    token = input("Enter your token: ")
    if confirm_choice():
        try:
            client.run(token, bot=False)
        except Exception as e:
            logging.error(f"Failed to log in: {str(e)}")

if __name__ == "__main__":
    main()
