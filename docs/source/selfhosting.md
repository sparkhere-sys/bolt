# Self-hosting Bolt

This nifty little guide will run you through setting up your own instance of Bolt on your machine.

## Prerequisites

Before starting, you'll need:

* Any OS that can run Python
* Python itself (duh)
  * recommended to use CPython, however PyPy works too.
* A Discord bot and a token

### Python dependencies

* Python 3.10+
* [`py-cord`](https://pypi.org/project/py-cord/) (`pip install py-cord`)
* [`python-dotenv`](https://pypi.org/project/python-dotenv/) (`pip install python-dotenv`)
* [`aiohttp`](https://pypi.org/project/aiohttp/) (`pip install aiohttp`)
* [`peewee`](https://pypi.org/project/peewee) (`pip install peewee`)
* If using Python 3.13+, also install [`audioop-lts`](https://pypi.org/project/audioop-lts)
  > pycord apparently insists on using it even without using audio features. thanks, pycord.
* Optional: [`colorama`](https://pypi.org/project/colorama) to make the logs look better

---

## Creating a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/home/)
2. Create a new application.
3. Go to the **Bot** tab.
4. Copy the token. You'll need it later.

> **IMPORTANT**
>
> Do **NOT** share your token with **anyone**.
>
> Anyone with your bot's token can control your bot.

5. **Optional**: Add a note in your bot's profile saying that it's powered by Bolt and link to the GitHub repo.

## Inviting the Bot to your Server

### Intents

After creating your Bot, you'll need to set up its intents.

Go to the **Bot** tab and enable:
- **Message content intent**
- **Server members intent**

You can find the permissions used on the main branch of Bolt here:
![Bolt's permissions](images/invite-permissions.png)

Then, go to the **Installation** tab and:
- select **Guild Install** in **Installation Contexts**
- select **Discord Provided Link** in **Install Link**
- in **Default Install Settings**, select the **`applications.commands`** and **`bot`** scopes,
- and the **Administrator** permission.
> Bolt requires admin because a lot of moderation actions need broad access to your server.
> This could change in the future.

![Bolt's installation settings](images/installation-settings.png)

Copy the link provided by Discord.

---

## Installing the Bot

> This probably goes without saying, but by installing Bolt, you're running your own instance of Bolt.
> **You** are responsible for keeping it updated, and keeping your token secure. 
> We, the Bolt developers, are not responsible and are not liable for any issues caused
> by running your own instance,
> as stated in the [license](https://github.com/sparkhere-sys/bolt/blob/main/LICENSE).

First, clone the repo:

```bash
git clone https://github.com/sparkhere-sys/bolt.git && cd bolt
```

(Optional, but highly recommended) Set up a virtual environment. (no, not a virtual machine.)

> Using a virtual environment keeps Bolt's dependencies isolated from the rest of your system, and is
> generally good practice.

The instructions will vary depending on your OS of choice.

* Linux/macOS:

```bash
python3 -m venv .venv # to create the venv
# activating the venv
source ./.venv/bin/activate # bash/zsh
source ./.venv/bin/activate.fish # fish
```

* Windows (PowerShell):

```powershell
py -m venv .venv # to create the venv
.\.venv\Scripts\Activate.ps1 # to activate the venv
```

Now install all the dependencies:

```bash
pip install -r requirements.txt # or you can install them manually
```

Create a `.env` file in the root directory of the repo, and add your bot's token:
```ini
TOKEN=your_token_here
```

Then, copy the `example_config.toml` file to `config.toml`, and edit it to your preferences.

Once all of that is done, run:
```bash
python -m bot
```

to start the bot.

To stop Bolt, press Ctrl+C in your console/terminal, or use your service manager if you're running Bolt as a service.

---

## Updating your Bot

Updating your bot is simple!

Pull the latest changes with Git:
```sh
git pull
```

Update the dependencies:
```sh
pip install -r requirements.txt
```

And then restart Bolt.

---

## Troubleshooting

Pay attention to the console output. Bolt will usually tell you what went wrong.

Some issues are caused by Discord API outages. Try again later.

Report any bugs on [Bolt's GitHub Issues](https://github.com/sparkhere-sys/bolt/issues).

### My bot doesn't start.

Common issues:
- Invalid bot token
- Missing dependencies
- Python is too old
- Your internet is just not working

### My bot is online, but its commands don't work.

Make sure:
- The bot has the required permissions
- The required intents are enabled
- The bot was invited with the `applications.commands` scope
- The cog you're trying to load isn't disabled in your `config.toml`

### My bot is reconnecting to Discord.

This usually means you have multiple instances of Bolt running with the same token, 
or you have issues with your internet.

Close any extra instances of Bolt. Only one instance should run per bot.

### My bot has _Administrator_, but it can't ban/kick/mute people.

If Bolt says "I don't have permission to [moderate] that user," it means Bolt's highest role is lower than
your target's.

Try moving Bolt's role up.