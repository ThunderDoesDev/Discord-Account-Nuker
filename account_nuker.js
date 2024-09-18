const axios = require('axios');
const readline = require('readline');
const fs = require('fs');
const cliProgress = require('cli-progress');

// Logging setup
const logStream = fs.createWriteStream('account_nuker.log', { flags: 'w' });
const log = (message) => {
    const timestamp = new Date().toISOString();
    logStream.write(`[${timestamp}] ${message}\n`);
    console.log(message);
};

let token = null;
const baseURL = 'https://discord.com/api/v9';

// Banner display
function displayBanner() {
    console.log(`
█████████                                                     █████       ██████   █████            █████                        
███░░░░░███                                                   ░░███       ░░██████ ░░███            ░░███                         
███    ░███   ██████   ██████   ██████  █████ ████ ████████   ███████      ░███░███ ░███  █████ ████ ░███ █████  ██████  ████████ 
███████████  ███░░███ ███░░███ ███░░███░░███ ░███ ░░███░░███ ░░░███░       ░███░░███░███ ░░███ ░███  ░███░░███  ███░░███░░███░░███
███░░░░░███ ░███ ░░░ ░███ ░░░ ░███ ░███ ░███ ░███  ░███ ░███   ░███        ░███ ░░██████  ░███ ░███  ░██████░  ░███████  ░███ ░░░ 
███    ░███ ░███  ███░███  ███░███ ░███ ░███ ░███  ░███ ░███   ░███ ███    ░███  ░░█████  ░███ ░███  ░███░░███ ░███░░░   ░███     
█████   █████░██████ ░░██████ ░░██████  ░░████████ ████ █████  ░░█████     █████  ░░█████ ░░████████ ████ █████░░██████  █████    
░░░░░   ░░░░░  ░░░░░░   ░░░░░░   ░░░░░░    ░░░░░░░░ ░░░░ ░░░░░    ░░░░░     ░░░░░    ░░░░░   ░░░░░░░░ ░░░░ ░░░░░  ░░░░░░  ░░░░░     
                                                    by ThunderDoesDev
---------------------------------------------------
                 OPTIONS MENU
---------------------------------------------------
1. Show Account Info
2. Leave or Delete Guilds
3. Delete Friends
4. Delete DMs
5. Full Nuke (All actions)
---------------------------------------------------
`);
}

async function displayInfo() {
    log("Displaying account info.");
    let retry = true;
    while (retry) {
        try {
            const userResponse = await axios.get(`${baseURL}/users/@me`, {
                headers: { Authorization: token }
            });
            const user = userResponse.data;
            console.log(`\nAccount Information:`);
            console.log(`Username: ${user.username}#${user.discriminator}`);
            console.log(`User ID: ${user.id}`);
            console.log(`Email: ${user.email || 'No email set'}`);
            console.log(`Phone: ${user.phone || 'No phone number set'}`);
            console.log(`Verified: ${user.verified}`);
            log(`Account Info: ${user.username}#${user.discriminator}, ID: ${user.id}, Verified: ${user.verified}`);            
            const paymentResponse = await axios.get(`${baseURL}/users/@me/billing/payment-sources`, {
                headers: { Authorization: token }
            });
            const paymentSources = paymentResponse.data;
            if (paymentSources.length > 0) {
                console.log("\nPayment Sources:");
                paymentSources.forEach((source) => {
                    console.log(`Payment Type: ${source.type}`);
                    console.log(`Last 4 Digits: ${source.last_4}`);
                    console.log(`Expires: ${source.expires_month}/${source.expires_year}`);
                    console.log(`Billing Country: ${source.billing_address.country}`);
                    log(`Payment Source: ${source.type}, Last 4: ${source.last_4}`);
                });
            } else {
                console.log("No payment sources found.");
                log("No payment sources found.");
            }
            const subscriptionResponse = await axios.get(`${baseURL}/users/@me/billing/subscriptions`, {
                headers: { Authorization: token }
            });
            const subscriptions = subscriptionResponse.data;
            if (subscriptions.length > 0) {
                console.log("\nSubscription Information:");
                subscriptions.forEach((sub) => {
                    console.log(`Subscription Type: ${sub.type}`);
                    console.log(`Status: ${sub.status}`);
                    console.log(`Current Period End: ${new Date(sub.current_period_end).toLocaleDateString()}`);
                    log(`Subscription: Type: ${sub.type}, Status: ${sub.status}, Period End: ${sub.current_period_end}`);
                });
            } else {
                console.log("No subscriptions found.");
                log("No subscriptions found.");
            }
            retry = false;
        } catch (error) {
            if (error.response && error.response.status === 429) {
                const retryAfter = error.response.headers['retry-after'];
                log(`Rate limit hit. Retrying after ${retryAfter} seconds...`);
                await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
            } else {
                log(`Error fetching account info: ${error.message}`);
                retry = false;
            }
        }
    }
}

async function processGuilds() {
    try {
        const response = await axios.get(`${baseURL}/users/@me/guilds`, {
            headers: { Authorization: token }
        });
        const guilds = response.data;
        let leaveCount = 0;
        let deleteCount = 0;
        const guildBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
        guildBar.start(guilds.length, 0);
        for (const guild of guilds) {
            let retry = true;
            while (retry) {
                try {
                    if (!guild.owner) {
                        // Leave guild
                        await axios.delete(`${baseURL}/users/@me/guilds/${guild.id}`, {
                            headers: { Authorization: token }
                        });
                        leaveCount++;
                        log(`Left guild: ${guild.name}`);
                    } else {
                        // Delete guild
                        await axios.delete(`${baseURL}/guilds/${guild.id}`, {
                            headers: { Authorization: token }
                        });
                        deleteCount++;
                        log(`Deleted guild: ${guild.name}`);
                    }
                    retry = false;
                } catch (error) {
                    if (error.response && error.response.status === 429) {
                        const retryAfter = error.response.headers['retry-after'];
                        log(`Rate limit hit. Retrying after ${retryAfter} seconds...`);
                        await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
                    } else {
                        log(`Error processing guild: ${error.message}`);
                        retry = false;
                    }
                }
            }
            guildBar.increment();
        }
        guildBar.stop();
        log(`Processed ${leaveCount} leave actions and ${deleteCount} delete actions.`);
    } catch (error) {
        log(`Error processing guilds: ${error.message}`);
    }
}

async function confirmChoice() {
    return new Promise((resolve) => {
        rl.question("Type 'Confirm' to process or 'Cancel' to return to the main menu: ", (input) => {
            if (input.toLowerCase() === 'confirm') {
                resolve(true);
            } else if (input.toLowerCase() === 'cancel') {
                console.log("Returning to the main menu...");
                log("User canceled the operation.");
                resolve(false);
            } else {
                console.log("Invalid input. Returning to main menu.");
                log("Invalid input during confirmation.");
                resolve(false);
            }
        });
    });
}

async function closeAllDMs() {
    try {
        const response = await axios.get(`${baseURL}/users/@me/channels`, {
            headers: { Authorization: token }
        });
        const dms = response.data;
        const dmBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
        dmBar.start(dms.length, 0);
        for (const dm of dms) {
            let retry = true;
            while (retry) {
                try {
                    await axios.delete(`${baseURL}/channels/${dm.id}`, {
                        headers: { Authorization: token }
                    });
                    log(`Deleted DM with ID: ${dm.id}`);
                    retry = false;
                } catch (error) {
                    if (error.response && error.response.status === 429) {
                        const retryAfter = error.response.headers['retry-after'];
                        log(`Rate limit hit. Retrying after ${retryAfter} seconds...`);
                        await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
                    } else {
                        log(`Error deleting DM: ${error.message}`);
                        retry = false;
                    }
                }
            }
            dmBar.increment();
        }
        dmBar.stop();
    } catch (error) {
        log(`Error closing DMs: ${error.message}`);
    }
}

async function removeAllFriends() {
    try {
        const response = await axios.get(`${baseURL}/users/@me/relationships`, {
            headers: { Authorization: token }
        });
        const friends = response.data;
        const friendsBar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
        friendsBar.start(friends.length, 0);
        for (const friend of friends) {
            let retry = true;
            while (retry) {
                try {
                    await axios.delete(`${baseURL}/users/@me/relationships/${friend.id}`, {
                        headers: { Authorization: token }
                    });
                    log(`Removed friend: ${friend.user.username}`);
                    retry = false;
                } catch (error) {
                    if (error.response && error.response.status === 429) {
                        const retryAfter = error.response.headers['retry-after'];
                        log(`Rate limit hit. Retrying after ${retryAfter} seconds...`);
                        await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
                    } else {
                        log(`Error removing friend: ${error.message}`);
                        retry = false;
                    }
                }
            }
            friendsBar.increment();
        }
        friendsBar.stop();
    } catch (error) {
        log(`Error removing friends: ${error.message}`);
    }
}

async function fullNuke() {
    log("Executing full nuke...");
    await processGuilds();
    await closeAllDMs();
    await removeAllFriends();
}

async function executeAction(option) {
    const confirmed = await confirmChoice();
    if (!confirmed) {
        main();
        return;
    }
    switch (option) {
        case '1':
            await displayInfo();
            break;
        case '2':
            await processGuilds();
            break;
        case '3':
            await removeAllFriends();
            break;
        case '4':
            await closeAllDMs();
            break;
        case '5':
            await fullNuke();
            break;
        default:
            console.log("Invalid option.");
    }
    console.log("\nReturning to the main menu...\n");
    main();
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function main() {
    displayBanner();
    rl.question('Choose an option (1-5): ', (option) => {
        rl.question('Enter your token: ', async (inputToken) => {
            token = inputToken;
            log(`User selected option ${option}`);
            await executeAction(option);
        });
    });
}

main();
