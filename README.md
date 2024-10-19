# discord bots

- Horoscope Bot: get your daily horoscope
- [Stock Bot](stock_bot/README.md)

## **Setting Up a Discord Bot**

1. [Access the Discord Developer Portal](#access-the-discord-developer-portal)
1. [Create a New Application](#create-a-new-application)
1. [Add a Bot to Your Application](#add-a-bot-to-your-application)
1. [Copy Your Bot's Token](#copy-your-bots-token)
1. [Enable Privileged Gateway Intents (If Necessary)](#enable-privileged-gateway-intents-if-necessary)
1. [Invite Your Bot to a Server (OAuth2 Setup)](#invite-your-bot-to-a-server-oauth2-setup)
1. [Run the bot](#run-the-bot)

---

## **Access the Discord Developer Portal**

- Go to the [Discord Developer Portal](https://discord.com/developers/applications).
- Log in with your Discord credentials.

---

## **Create a New Application**

1. **Navigate to Applications:**

   - Click on **"Applications"** in the sidebar.

2. **Create Application:**

   - Click the **"New Application"** button at the top-right.
   - **Name Your Application:** Enter a name for your bot (e.g., "MyDiscordBot").
   - Click **"Create"**.

3. **Set Application Details (Optional):**

   - **Description:** Add a description for your bot.
   - **Icon:** Upload an icon to represent your bot.
   - Click **"Save Changes"** if you make any updates.

---

## **Add a Bot to Your Application**

1. **Navigate to the Bot Tab:**

   - In the sidebar, click on **"Bot"**.

2. **Add Bot:**

   - Click **"Add Bot"**.
   - Confirm by clicking **"Yes, do it!"**.

3. **Customize Your Bot (Optional):**

   - **Username:** Change the bot's username if desired.
   - **Profile Picture:** Upload a profile picture for your bot.

4. **Save Changes:**

   - Click **"Save Changes"** after making updates.

---

## **Copy Your Bot's Token**

Your bot's token is needed for authentication.

1. **Go to Token Section:**

   - Under the **"Bot"** tab, find the **"Token"** section.

2. **Reveal and Copy the Token:**

   - Click **"Reset Token"** if no token is displayed.
   - Click **"Copy"** to copy the token to your clipboard.
   - **Important:** **Do not share this token.**

---

## **Enable Privileged Gateway Intents (If Necessary)**

Depending on your bot's features, you may need to enable intents.

1. **Scroll to Privileged Gateway Intents:**

   - Still under the **"Bot"** tab.

2. **Enable Required Intents:**

   - **Presence Intent:** For monitoring user status.
   - **Server Members Intent:** For accessing member data.
   - **Message Content Intent:** For reading message content (needed for text commands).

3. **Toggle On the Required Intents:**

   - Click the switches to enable the intents your bot requires.

4. **Save Changes:**

   - Click **"Save Changes"**.

---

## **Invite Your Bot to a Server (OAuth2 Setup)**

To add your bot to a server, you need to generate an invite link using OAuth2.

1. **Navigate to OAuth2 URL Generator:**

   - In the sidebar, click on **"OAuth2"**.
   - Select **"URL Generator"**.

2. **Set Scopes:**

   - Under **"SCOPES"**, check the box for **"bot"**..

3. **Set Bot Permissions:**

   - Scroll down to **"BOT PERMISSIONS"**.
   - Select the permissions your bot needs. Common permissions include:
     - **Send Messages**
     - **Read Messages/View Channels**
     - **Embed Links**
     - **Attach Files**
     - **Read Message History**
     - **Add Reactions**

4. **Generate the Invite URL:**

   - The URL at the bottom updates as you select options.
   - **Copy** the generated URL.

5. **Invite the Bot to Your Server:**

   - Paste the URL into your browser's address bar and hit **Enter**.
   - Choose the server you want to add the bot to from the dropdown.
     - **Note:** You must have the **"Manage Server"** permission on that server.
   - Click **"Continue"**.
   - Review the permissions you're granting to the bot.
   - Click **"Authorize"**.
   - Complete the CAPTCHA if prompted.

6. **Verify the Bot is in Your Server:**

   - Open Discord and check if the bot appears in your server's member list.

---

## **Run the bot**

   - Use `python3 <file_name>.py` to run the bot.