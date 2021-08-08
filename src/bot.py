import datetime
import os
import random
import traceback

import discord
import inputimeout
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self._get_bot_prefix,
            owner_ids=[711444754080071714, 491630879085559808],
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False, users=True, replied_user=False
            ),
            description="The discord bot for the Linux Community discord server!",
            *args,
            **kwargs,
        )

        self.help_command = None
        self.secrets = {x: y for x, y in os.environ.items() if x in ["TOKEN"]}
        self.applying = []
        self.bot_cogs = [
            f"cogs.{cog[:-3]}"
            for cog in os.listdir("cogs")
            if cog.endswith(".py") and not cog.startswith("_")
        ]
        self.colors = [0xFFFDFC, 0x3A4047]
        self.launch_time = datetime.datetime.utcnow()

    def run(self):
        try:
            for cog in self.bot_cogs:
                try:
                    self.load_extension(cog)
                except Exception as e:
                    raise e
        except Exception as e:
            raise e

        prompt = """
Which mode do you want to boot to?

Available Modes: 
Secure [Only dev Commands]
Normal [Regular usage]
CDev [All commands but only devs can run commands]

After 5 seconds hyena will default to normal boot     
"""
        try:
            self.current_mode_type = inputimeout.inputimeout(
                prompt=prompt + "\n", timeout=5
            ).lower()
        except:
            self.current_mode_type = "normal"
        print(f"----Continuing with {self.current_mode_type} mode----")

        super().run(self.secrets["TOKEN"])

    async def _get_bot_prefix(self, bot, message):
        return [f"<@!{self.user.id}> ", f"<@{self.user.id}> ", "./", "sudo "]

    clear = lambda self: os.system("cls" if os.name == "nt" else "clear")

    async def on_ready(self):
        self.clear()
        self.change_status.start()
        print(f"Logged in as {self.user}.")

    async def process_commands(self, message):
        if message.guild is None or message.author.bot:
            return

        await super().process_commands(message)

    async def on_message(self, message):
        if self.current_mode_type == "cdev":
            if message.author.id not in self.owner_ids:
                return

        await self.process_commands(message)

    def get_cog_aliases(self, term: str):
        aliases = {
            ("utilities", "utils", "util"): "utilities",
        }

        for alias, cog in aliases.items():
            if term.lower() in alias:
                return cog
        return term

    async def handle_load(self, ctx, cog: str):
        if cog in ["*", "all"]:
            errored_out = []
            for cog in self.bot_cogs:
                try:
                    self.load_extension(cog)
                except commands.errors.ExtensionAlreadyLoaded:
                    errored_out.append((cog[5:], "This extension is already loaded"))
                except commands.errors.ExtensionNotFound:
                    errored_out.append((cog[5:], "This extension was not found"))
                except Exception as e:
                    errored_out.append((cog[5:], str(e)))
            if errored_out == []:
                return await ctx.send("Successfully completed the operation.")

            newline = "\n"

            await ctx.send(
                f"""
Successfully completed the operation. 
```
Errored out : {newline.join([f"{x[0]} : {x[1]}" for x in errored_out])}
```
"""
            )
            return

        if cog.endswith(".py"):
            cog = cog[:-3]

        cog = self.get_cog_aliases(cog)

        try:
            self.load_extension(f"cogs.{cog}")
            await ctx.message.add_reaction("<:OP_Verified:815589801586851840>")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"The cog `{cog}` is already loaded")
        except commands.errors.ExtensionNotFound:
            await ctx.send(f"The cog `{cog}` is Not found...")
        except:
            embed = discord.Embed(
                title=f"Error while loading ext: {cog}", color=discord.Colour.red()
            )
            embed.description = f"""
    ```py
    {traceback.format_exc()}
    ```
    """
            await ctx.send(embed=embed)

    async def handle_unload(self, ctx, cog: str):
        if cog in ["*", "all"]:
            errored_out = []
            for cog in self.bot_cogs:
                try:
                    self.unload_extension(cog)
                except commands.errors.ExtensionNotLoaded:
                    errored_out.append((cog[5:], "This extension was not loaded"))
                except commands.errors.ExtensionNotFound:
                    errored_out.append((cog[5:], "This extension was not found"))
                except Exception as e:
                    errored_out.append((cog[5:], str(e)))
            if errored_out == []:
                return await ctx.send("Successfully completed the operation.")

            newline = "\n"

            await ctx.send(
                f"""
Successfully completed the operation.
```
Errored out : {newline.join([f"{x[0]} : {x[1]}" for x in errored_out])}
```
"""
            )
            return

        if cog.endswith(".py"):
            cog = cog[:-3]

        cog = self.get_cog_aliases(cog)

        try:
            self.unload_extension(f"cogs.{cog}")
            await ctx.message.add_reaction("<:OP_Verified:815589801586851840>")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"The cog `{cog}` isn't even loaded.")
        except commands.errors.ExtensionNotFound:
            await ctx.send(f"The cog `{cog}` is Not found...")
        except:
            embed = discord.Embed(
                title=f"Error while loading ext: {cog}", color=discord.Colour.red()
            )
            embed.description = f"""
    ```py
    {traceback.format_exc()}
    ```
    """
            await ctx.send(embed=embed)

    async def handle_reload(self, ctx, cog: str):
        if cog in ["*", "all"]:
            errored_out = []
            for cog in self.bot_cogs:
                try:
                    self.reload_extension(cog)
                except commands.errors.ExtensionNotLoaded:
                    errored_out.append((cog[5:], "This extension was not loaded"))
                except commands.errors.ExtensionNotFound:
                    errored_out.append((cog[5:], "This extension was not found"))
                except Exception as e:
                    errored_out.append((cog[5:], str(e)))
            if errored_out == []:
                return await ctx.send("Successfully completed the operation.")

            newline = "\n"
            return await ctx.send(
                f"""
    Successfully completed the operation. 
    ```
    Errored out : {newline.join([f"{x[0]} : {x[1]}" for x in errored_out])}
    ```
    """
            )

        if cog.endswith(".py"):
            cog = cog[:-3]

        cog = self.get_cog_aliases(cog)

        try:
            self.reload_extension(f"cogs.{cog}")
            await ctx.message.add_reaction("<:OP_Verified:815589801586851840>")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"The cog `{cog}` isn't even loaded.")
        except commands.errors.ExtensionNotFound:
            await ctx.send(f"The cog `{cog}` is Not found...")
        except:
            embed = discord.Embed(
                title=f"Error while loading ext: {cog}", color=discord.Colour.red()
            )
            embed.description = f"""
    ```py
    {traceback.format_exc()}
    ```
    """
            await ctx.send(embed=embed)

    @tasks.loop(seconds=30)
    async def change_status(self):
        status = [
            discord.Game(name="Watching Linux Community! | sudo help"),
            discord.Activity(
                type=discord.ActivityType.watching, name="The chat! | sudo help"
            ),
            discord.Activity(
                type=discord.ActivityType.listening,
                name="the mods While eating donuts | sudo help",
            ),
        ]
        await self.change_presence(
            activity=random.choice(status), status=discord.Status.dnd
        )
