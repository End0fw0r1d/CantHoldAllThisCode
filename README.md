# CantHoldAllThisCode
A discord bot, using Python to automate meme creation

Currently the bot relies on manually starting up cantholdthis.py (which listens to and handles command inputs), processmanager.py, and msgserver.py

Commands are recognized by cantholdthis.py, then handed off to processmanager.py which handles image operations on parallel processes via multiprocessing, and hands the results off to msgserver.py, which uploads to discord.

Image edits are loaded as libraries in processmanager.py and handled based on the arguments passed through, returning a resultant image file, using multiprocessing.connection ports to send off the image filename or text string to the msgserver (which is listening always).

Msgserver.py and processmanager.py use lists to queue up relevant tasks for processing through/from listening or sending ports.

Additionally, I have reacting.py, but that's because for whatever reason, I can't have the bot listening to messages and commands in the same file, so I just have a small separate file for listening to messages and responding if/when appropriate.

it's a learning project kinda, but also as a long-term project of someone with a short attention span sometimes, there's some unnecessary redundancy in places, and a lot of improvements and changes to be made.
After I haven't touched it for a while, I often have to go back and reread old bits of code to remember how I did things and why.

It's fairly easy to set up, you just need to roll your own .env file with appropriate credentials in it(which involves making your own bot in discord dev portal to get a token from them)

I can't off the top of my head name all the python libraries besides PIL that you need, but just install anything python tells you it can't import because it doesn't exist.

.env needs:

DISCORD_TOKEN=
DISCORD_GUILD=
