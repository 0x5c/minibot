"""
Minibot, a bot for basic guild stuff
---

Copyright 2019-2021 0x5c <dev@0x5c.io>

Released under the terms of the MIT License.
See LICENSE for the full text of the license.
"""

import logging

import discord
from discord.ext import commands, tasks

import selfrole

import info

import data.keys as keys
import data.options as opt


logging.basicConfig(level=logging.WARNING)

# --- Vars ---

embed_colour = 0x005682

nobranding = False

# Defining the intents to use
intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.messages = True
intents.dm_messages = True
intents.presences = True
intents.message_content = True

# Setting up the member cache
member_cache_flags = discord.MemberCacheFlags.none()
member_cache_flags.joined = True

bot = commands.Bot(command_prefix=opt.command_prefix, intents=intents, member_cache_flags=member_cache_flags,
                   chunk_guilds_at_startup=True, case_insensitive=True, strip_after_prefix=opt.strip_after_prefix)


# --- Commands ---

@bot.command(name="info", aliases=["about"])
async def _info(ctx: commands.Context):
    """Bot information."""
    embed = discord.Embed()
    embed.colour = embed_colour
    if not nobranding:
        embed.add_field(name="Author", value=info.author)
        embed.add_field(name="Contributing", value=info.contributing)
        embed.add_field(name="License", value=info.license)
        embed.add_field(name="Official Guild", value=info.guild_invite)
        embed.title = "About Minibot\n"
        embed.description = info.description
    if ctx.guild is not None:
        guild_perms = ctx.guild.me.guild_permissions
        channel_perms = ctx.channel.permissions_for(ctx.guild.me)
        botinfo = ("```\n"
                   f"Version: {info.release}\n"
                   f"Pycord version: {discord.__version__}\n"
                   f"Instance ID: {bot.user.id}\n"
                   "---\n"
                   f"Server ID: {ctx.guild.id}\n"
                   "\n"
                   "Bot permissions:\n"
                   f"- manage_roles: {guild_perms.manage_roles}\n"
                   "\n"
                   "Bot permissions in this channel:\n"
                   f"- manage_messages: {channel_perms.manage_messages}"
                   "```")
        embed.add_field(name="Bot Status", value=botinfo, inline=False)
    else:
        embed.add_field(name="Bot Status", value="```\nStatus unavailable in DMs.\n```", inline=False)
    await ctx.send(embed=embed)


# @bot.command(name="purge", aliases=["prune", "nuke"])
# async def _purge(ctx: commands.Context, limit: int):
#     ...


# --- Events ---

@bot.event
async def on_ready():
    print(f"[II] Logged in as {bot.user}")
    print("------")

    invalid_guilds = False
    invalid_roles = False
    for guild_id in opt.autoroles:
        guild = bot.get_guild(guild_id)
        if guild is None:
            invalid_guilds = True
        else:
            for role_id in opt.autoroles[guild_id]:
                role = guild.get_role(role_id)
                if role is None:
                    invalid_roles = True
    if invalid_guilds:
        print("[WW] Invalid/unknown guild IDs found in the autorole config!")
    if invalid_roles:
        print("[WW] Invalid/unknown role IDs found in the autorole config!")

    refresh_status.start()


@bot.event
async def on_member_join(member: discord.Member):
    if not member.pending:
        await do_autoroles(member)


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.pending and not after.pending:
        await do_autoroles(after)


async def do_autoroles(member: discord.Member):
    if opt.no_autorole_bots and member.bot:
        print(f"[II] Not applying autoroles to bot {member}.")
        return
    guild = member.guild
    if guild.id in opt.autoroles:
        roles = opt.autoroles[guild.id]
        existing_roles = member.roles.copy()
        for role_id in roles:
            existing_roles.append(guild.get_role(role_id))
        try:
            print(f"[II] Applying autoroles to {member}.")
            await member.edit(roles=existing_roles, reason="minibot-autorole")
        except discord.Forbidden as ex:
            print(f"[EE] discord.Forbidden in {guild.id}: {ex}")


@tasks.loop(minutes=10)
async def refresh_status():
    await bot.change_presence(activity=discord.Game(name=f"{opt.display_prefix}help"))


# --- Init ---

bot.add_cog(selfrole.SelfRole(bot))

try:
    bot.run(keys.discord_token)

except discord.LoginFailure as ex:
    # Miscellaneous authentications errors: borked token and co
    raise SystemExit("Error: Failed to authenticate: {}".format(ex))

except discord.ConnectionClosed as ex:
    # When the connection to the gateway (websocket) is closed
    raise SystemExit("Error: Discord gateway connection closed: [Code {}] {}".format(ex.code, ex.reason))

except ConnectionResetError as ex:
    # More generic connection reset error
    raise SystemExit("ConnectionResetError: {}".format(ex))
