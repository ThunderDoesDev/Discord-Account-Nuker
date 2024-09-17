
# Discord Account Nuker

This script is a selfbot tool that automates destructive actions such as deleting friends, leaving/deleting guilds, and removing direct messages (DMs) from your Discord account. It logs all activities and provides a user-friendly interface with multiple options. **Use with caution** as this script is designed for account nuking and may violate Discord's Terms of Service.

## Features

- **Account Info Display**: Fetch and display information about the user's Discord account, including payment methods and subscriptions.
- **Guild Management**: Automatically leave or delete Discord guilds depending on ownership status.
- **Friend Removal**: Mass remove all friends from the account.
- **DM Deletion**: Close and delete all direct messages.
- **Full Nuke**: Execute all of the above actions in sequence, effectively wiping the account's presence on Discord.

## Installation

### Prerequisites

- Python 3.8+
- [discord.py](https://pypi.org/project/discord.py/) (`pip install discord.py`)
- [aiohttp](https://pypi.org/project/aiohttp/) (`pip install aiohttp`)
- [tqdm](https://pypi.org/project/tqdm/) (`pip install tqdm`)

### Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/ThunderDoesDev/Discord-Account-Nuker.git
    cd Discord-Account-Nuker
    ```

2. Install the required dependencies:
    ```bash
    pip install discord.py aiohttp tqdm
    ```

3. Open the script `account_nuker.py` and run it.

## Usage

1. Run the script:
    ```bash
    python account_nuker.py
    ```

2. Enter your **Discord token** when prompted. To find your token, follow these [instructions](https://www.androidauthority.com/get-discord-token-3149920/).

3. Select an option from the menu:
    - **1**: Show account information.
    - **2**: Leave or delete guilds.
    - **3**: Remove all friends.
    - **4**: Delete all DMs.
    - **5**: Perform a full nuke (executes all actions).

### Logging

All activities are logged into the `account_nuker.log` file. Each action is recorded with details like the number of friends removed, guilds left or deleted, DMs closed, and any errors encountered.

### Confirmation

Before executing destructive actions, the script will ask for confirmation to prevent accidental execution. Simply type **Confirm** to proceed or **Cancel** to return to the main menu.

### Rate Limits

The script handles rate limiting with automatic retries if Discord API limits are hit during operations such as removing friends or leaving guilds.

## Notes

- **Selfbots are against Discord’s Terms of Service**. Use this tool responsibly and be aware of the potential consequences, such as your account being banned.
- This script uses **discord.py** in selfbot mode, meaning it logs in as a user account rather than a bot account.

## Future Enhancements

- Add support for managing roles and permissions.
- Option to handle individual guild actions (e.g., selectively leave or delete).
- More customization for logging and output.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

The creator of this script **does not take any responsibility for how the script is used**. Use this tool at your own risk. The author is not liable for any consequences or damages, including but not limited to account bans or data loss, that result from using this tool.
