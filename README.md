# backup-to-discord

> [!WARNING]
> Use of this program might violate the [Discord Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy). Proceed with caution.
>
> I created this program, and use it, in good faith and with no ill intention. If you use this program with ill intent, Discord might punish you.

A simple program that automatically backs up a directory to Discord.

Originally made for backing up a Minecraft world, but could be used for other things.

## Setup

### Prerequisites

- Python 3.11 (use `python --version` to check if you have Python)

### Steps

1. Download the [latest release](https://github.com/valbuildr/backup-to-discord/releases/latest) from this repository.
2. Unzip the included zip file.
3. Fill out `.env.example` and rename it to `.env`.
4. Create a virtual environment with `python3 -m venv .venv`.
5. Activate the virtual environment.
    Depending on the type of terminal you're using, this varies. See [this table](https://docs.python.org/3/library/venv.html#how-venvs-work) for the correct command for your terminal.
6. Run the code with `python3 src/main.py`.

## License

Distributed under the MIT License. See `LICENSE` for more information.