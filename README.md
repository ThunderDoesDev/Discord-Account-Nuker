
# Discord Account Nuker

This script is a **selfbot** tool available in both Python and JavaScript. It automates destructive actions such as deleting friends, leaving/deleting guilds, and removing direct messages (DMs) from your Discord account using **direct API calls** via `axios` (for JavaScript) or `aiohttp` (for Python). It logs all activities and provides a user-friendly interface with multiple options. **Use with caution** as this script is designed for account nuking and violates Discord's Terms of Service.

## Features (Both Python and JavaScript)

- **Account Info Display**: Fetch and display information about your Discord account, including payment methods and subscriptions.
- **Guild Management**: Automatically leave or delete Discord guilds depending on ownership status.
- **Friend Removal**: Mass remove all friends from the account.
- **DM Deletion**: Close and delete all direct messages.
- **Full Nuke**: Execute all of the above actions in sequence, effectively wiping the account's presence on Discord.

## Confirmation Prompt

Before performing any destructive action, the script prompts the user to confirm the action by typing "Confirm". If the user types "Cancel", the operation will be aborted and the script will return to the main menu. This provides an additional layer of security to prevent unintended data loss.

## Installation

### Prerequisites (JavaScript Version)

- Node.js 14+
- Required modules:
    ```bash
    npm install axios cli-progress
    ```

### Prerequisites (Python Version)

- Python 3.8+
- Required modules:
    ```bash
    pip install discord aiohttp tqdm
    ```

### Setup (JavaScript)

1. Clone this repository:
    ```bash
    git clone https://github.com/ThunderDoesDev/Discord-Account-Nuker.git
    cd Discord-Account-Nuker
    ```

2. Install the required dependencies:
    ```bash
    npm install axios cli-progress
    ```

3. Open the script `account_nuker.js` and run it.

### Setup (Python)

1. Clone this repository:
    ```bash
    git clone https://github.com/ThunderDoesDev/Discord-Account-Nuker.git
    cd Discord-Account-Nuker
    ```

2. Install the required dependencies:
    ```bash
    pip install discord aiohttp tqdm
    ```

3. Open the script `account_nuker.py` and run it.

## Usage

1. Run the script (JavaScript):
    ```bash
    node account_nuker.js
    ```

   OR

   Run the script (Python):
    ```bash
    python account_nuker.py
    ```

2. Enter your **Discord user token** when prompted. To find your token, follow these [instructions](https://www.androidauthority.com/get-discord-token-3149920/).

3. Select an option from the menu:
    - **1**: Show account information.
    - **2**: Leave or delete guilds.
    - **3**: Remove all friends.
    - **4**: Delete all DMs.
    - **5**: Perform a full nuke (executes all actions).

4. **Confirmation**: After selecting an option, the script will ask you to confirm the operation by typing **"Confirm"**. You can cancel the operation by typing **"Cancel"**.

### Logging

All activities are logged into the `account_nuker.log` file. Each action is recorded with details like the number of friends removed, guilds left or deleted, DMs closed, and any errors encountered.

### Rate Limits

Both scripts handle rate limiting with automatic retries if Discord API limits are hit during operations such as removing friends or leaving guilds.

## Notes

- **Selfbots are against Discord’s Terms of Service**. Use this tool responsibly and be aware of the potential consequences, such as your account being banned.
- This script uses **direct API calls** in selfbot mode, meaning it logs in as a user account rather than a bot account.

## Future Enhancements

- Add support for managing roles and permissions.
- Option to handle individual guild actions (e.g., selectively leave or delete).
- More customization for logging and output.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

The creator of this script **does not take any responsibility for how the script is used**. Use this tool at your own risk. The author is not liable for any consequences or damages, including but not limited to account bans or data loss, that result from using this tool.

## Support

For support, issues, or enhancements, please open an issue in this repository or join our discord support server.

[Join Support Server](https://discord.gg/thunderdoesdev)
