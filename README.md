# <p align=center> Bolt </p>

<p align=center>
  <img alt="Open Issues" src="https://img.shields.io/github/issues/sparkhere-sys/bolt?style=for-the-badge&logo=github&logoColor=white&color=%23f38ba8">
  <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues-pr/sparkhere-sys/bolt?style=for-the-badge&logo=git&logoColor=white&color=%23a6e3a1">
</p>

---

> This is where she writes a description.

Bolt is a (heavily WIP) general purpose Discord bot!

join the support (and also testing) server: https://discord.gg/hF6mgCE3gT

invite Bolt to your server: https://sparkhere-sys.github.io/bolt

## Installation

Follow these instructions if you want to self-host the bot.

Or just add the bot to your server. Feel free.

### Prerequisites

* Any OS that can run Python
* Python itself (duh)
  * recommended to use CPython, however PyPy works too
* A Discord bot token (go to https://discord.dev)

#### Python dependencies

* Python 3.10+ because we used `match-case` and not a ton of `if-elif-else`s
* [`py-cord`](https://pypi.org/project/py-cord/) (`pip install py-cord`)
* [`python-dotenv`](https://pypi.org/project/python-dotenv/) (`pip install python-dotenv`)
* If using Python 3.13, also install [`audioop-lts`](https://pypi.org/project/audioop-lts) (pycord apparently insists on using it even without using audio features. thanks, pycord.)
* Optional: [`colorama`](https://pypi.org/project/colorama) so your logs look :sparkles:pretty:sparkles:

---

### Instructions

First, clone the repo:

```bash
git clone https://github.com/sparkhere-sys/bolt.git && cd bolt
```

Next, set up a virtual environment. (no, not a virtual machine.) The instructions will vary depending on your OS of choice.

* Linux/macOS:

```bash
python3 -m venv venv && source ./venv/bin/activate
```

* Windows (PowerShell):

```powershell
python3 -m venv venv
.\venv\Scripts\Activate.ps1
```

Now install all the dependencies:

```bash
pip install -r requirements.txt # or you can install them manually
```

Then, create a `.env` file containing your bot's token and the prefix you want to use:

```ini
TOKEN=your_token_here
PREFIX=.
```

Once all of that is done, run:
```bash
python -m bot
```
to start the bot.

# uhhh bye

made with <3 by spark and the bolt dev team (currently only 3 people lol)

contact me:

* [my email](mailto:spark-aur@proton.me)
* my discord: `spark_sys`

---

<p align=center>
  <img alt="License: Apache 2.0" src="https://img.shields.io/github/license/sparkhere-sys/bolt?style=for-the-badge&logo=apache&logoColor=black&label=license&labelColor=white&color=%2374c7ec&link=https%3A%2F%2Fgithub.com%2Fsparkhere-sys%2Fbolt%2Fblob%2Fmain%2FLICENSE">
</p>
