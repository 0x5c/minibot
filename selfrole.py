"""
Selfrole module for Minibot
---

Copyright 2020 0x5c <dev@0x5c.io>

Released under the terms of the MIT License.
See LICENSE for the full text of the license.
"""


from typing import Optional

import discord
import discord.ext.commands as commands

import data.options as opt


class SelfRole(commands.Cog):
    """Selfrole functionality"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- Events ---

    @commands.Cog.listener()
    async def on_ready(self):
        invalid_guilds = False
        invalid_roles = False
        for guild_id in opt.selfroles:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                invalid_guilds = True
            else:
                for role_id in opt.selfroles[guild_id]:
                    role = guild.get_role(role_id)
                    if role is None:
                        invalid_roles = True
        if invalid_guilds:
            print("[WW] Invalid/unknown guild IDs found in the selfrole config!")
        if invalid_roles:
            print("[WW] Invalid/unknown role IDs found in the selfrole config!")

    @commands.command()
    @commands.guild_only()
    async def roleme(self, ctx: commands.Context, number: Optional[int] = None):
        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)
        member: discord.Member = ctx.author

        if guild_id not in opt.selfroles:
            # There is no selfrole configured for this guild.
            embed = discord.Embed(title="Error!", colour=0xF04747)
            embed.description = "This guild is not configured for self-assignable roles!"
            await ctx.send(embed=embed)
            return

        if number is not None:
            # We've got a role selection.
            embed = discord.Embed(title="Error!", colour=0xF04747)
            embed.description = f"Invalid role number: `{number}`"
            try:
                role_id = opt.selfroles[guild_id][number]
            except IndexError:
                # Selection is out of range.
                embed.description += "\n\n`NOT_A_ROLE`"
                await ctx.send(embed=embed)
                return
            role = guild.get_role(role_id)
            if role is None:
                # Selection
                embed.description += "\n\n`BONK_ROLE`"
                await ctx.send(embed=embed)
                return
            if role in member.roles:
                await member.remove_roles(role, reason="Self-assignable role")
                status = "Removed"
            else:
                await member.add_roles(role, reason="Self-assignable role")
                status = "Added"
            print(f"[II] {status} role '{role.name}' to {member} in {guild.id}")
            embed = discord.Embed(title="Roleme", colour=0x43B581)
            embed.description = f"**{status} {role.mention}**"
            await ctx.send(embed=embed)
            return
        else:
            # Let's list roles.
            available_roles = []
            removable_roles = []
            for index, role_id in enumerate(opt.selfroles[guild_id]):
                role = guild.get_role(role_id)
                if role is not None:
                    # The role is not bonk.
                    if role in member.roles:
                        # The member already has the role.
                        removable_roles.append((index, role))
                    else:
                        # The member does not have the role.
                        available_roles.append((index, role))

            # Checking if we have any not bonk roles.
            if not available_roles and not removable_roles:
                embed = discord.Embed(title="Error!", colour=0xF04747)
                embed.description = "No valid self-assignable roles availlable in this guild!"
                await ctx.send(embed=embed)
                return

            # Presenting the list of roles.
            embed = discord.Embed(title="Assignable roles list", colour=0x005682)
            embed.description = f"Use `{ctx.prefix}roleme <number>` to select a role."
            if available_roles:
                available_list = str("\n".join([f"`{idx}`: {role.mention}" for idx, role in available_roles]))
                embed.add_field(name="Available roles", value=available_list, inline=False)
            if removable_roles:
                removable_list = str("\n".join([f"`{idx}`: {role.mention}" for idx, role in removable_roles]))
                embed.add_field(name="Removable roles", value=removable_list, inline=False)
            await ctx.send(embed=embed)
