import traceback

import discord

from bot import Bot

bot = Bot()  # dont pass in things here, pass in ./bot.py


@bot.command(name="load")
async def load(ctx, cog):
    if ctx.author.id not in bot.owner_ids:
        return await ctx.send("You are not the developer!")

    await bot.handle_load(ctx, cog)


@bot.command(name="unload")
async def unload(ctx, cog):
    if ctx.author.id not in bot.owner_ids:
        return await ctx.send("You are not the developer!")

    await bot.handle_unload(ctx, cog)


@bot.command(name="reload")
async def reload(ctx, cog):
    if ctx.author.id not in bot.owner_ids:
        return await ctx.send("You are not the developer!")

    await bot.handle_reload(ctx, cog)


@bot.command(name="eval", aliases=["exec"])
async def eval_command(ctx, *, code='await ctx.send("Hello World")'):
    if not ctx.author.id in bot.owner_ids:
        return await ctx.send("Sorry, this is a Developer only command!")
    try:
        code = code.strip("`")
        code = code.strip("py")
        code = code.split("\n")

        if len(code) > 1:
            code_to_process = code[1:-1]
            code = code_to_process

        with open("eval_command.py", "w") as file:
            file.writelines(
                """import asyncio, discord
async def code(ctx, bot): \n"""
            )

        with open("eval_command.py", "a") as file:
            for line in code:
                file.writelines("   " + line + "\n")

        import importlib

        import eval_command

        importlib.reload(eval_command)
        await eval_command.code(ctx, bot)
    except Exception as e:
        embed = discord.Embed(
            title="Error Occurred in eval.", color=discord.Colour.red()
        )
        embed.description = f"""
```py
{traceback.format_exc()}
```
"""
        await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run()
