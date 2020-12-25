"""
Selfrole module for Minibot
---

Copyright 2020 0x5c <dev@0x5c.io>

Released under the terms of the MIT License.
See LICENSE for the full text of the license.
"""


from typing import Dict

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
    async def roleme(self, ctx: commands.Context, *numbers: int):
        """Lists or self-assignable roles."""
        numbers = set(sorted(numbers))

        if ctx.guild.id not in opt.selfroles:
            # There is no selfrole configured for this guild.
            embed = discord.Embed(title="Error!", colour=0xF04747)
            embed.description = "This guild is not configured for self-assignable roles!"
            await ctx.send(embed=embed)
            return

        if numbers:
            # We've got a(many) role selection(s).
            async with ctx.typing():
                await self.apply_roles(ctx, numbers)
        else:
            # Let's list roles.
            await self.send_roles(ctx)

    async def send_roles(self, ctx: commands.Context):
        """Lists the availlable roles for the message author."""
        member: discord.Member = ctx.author

        available_roles = []
        removable_roles = []
        for index, role_id in enumerate(opt.selfroles[ctx.guild.id]):
            role = ctx.guild.get_role(role_id)
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
        embed.description = f"""Use `{ctx.prefix}roleme <number>` to select a role.
                            You can select multiple roles by separating them with a space: `0 1 2 3`."""
        if available_roles:
            available_list = str("\n".join([f"`{idx}`: {role.mention}" for idx, role in available_roles]))
            embed.add_field(name="Available roles", value=available_list, inline=False)
        if removable_roles:
            removable_list = str("\n".join([f"`{idx}`: {role.mention}" for idx, role in removable_roles]))
            embed.add_field(name="Removable roles", value=removable_list, inline=False)
        await ctx.send(embed=embed)

    async def apply_roles(self, ctx: commands.Context, roles: set):
        """Adds/removes the selected roles from the message author."""
        member: discord.Member = ctx.author

        assigned_roles = []
        removed_roles = []
        errors = []
        for role_num in roles:
            try:
                role_id = opt.selfroles[ctx.guild.id][role_num]
            except IndexError:
                # Selection is out of range.
                errors.append(f"`{role_num}`: `NOT_A_ROLE`")
                continue
            role = ctx.guild.get_role(role_id)
            if role is None:
                # Selection is a in invalid role present in the config.
                errors.append(f"`{role_num}`: `BONK_ROLE`")
                continue
            if role in member.roles:
                # Selection is a valid role and user has it.
                print(f"[II] Removing role '{role.name}' from {member} in {ctx.guild.id}")
                await member.remove_roles(role, reason="Self-assignable role")
                removed_roles.append(f"`{role_num}`: {role.mention}")
            else:
                # Selection is a valid role and user does not have it.
                print(f"[II] Assigning role '{role.name}' to {member} in {ctx.guild.id}")
                await member.add_roles(role, reason="Self-assignable role")
                assigned_roles.append(f"`{role_num}`: {role.mention}")
        embed = discord.Embed(title="Roleme", colour=0x43B581)
        if assigned_roles:
            embed.add_field(name="Assigned roles", value="\n".join(assigned_roles), inline=False)
        if removed_roles:
            embed.add_field(name="Removed roles", value="\n".join(removed_roles), inline=False)
        if errors:
            if not (assigned_roles or removed_roles):
                embed.title = "Error!"
                embed.colour = 0xF04747
            embed.add_field(name="Invalid roles", value="\n".join(errors), inline=False)
        await ctx.send(embed=embed)

    @commands.group(name="rolestats", enabled=opt.enable_role_stats)
    @commands.guild_only()
    async def _role_stats(self, ctx: commands.Context):
        """Show statistics for roleme-managed roles."""
        if ctx.invoked_subcommand is None:
            role_stats: Dict[discord.Role, int] = {}

            if ctx.guild.id not in opt.selfroles:
                # There is no selfrole configured for this guild.
                embed = discord.Embed(title="Error!", colour=0xF04747)
                embed.description = ("This guild is not configured for self-assignable roles!\n"
                                     "Roleme statistics are not available.")
                await ctx.send(embed=embed)
                return

            roles = [ctx.guild.get_role(r) for r in opt.selfroles[ctx.guild.id]]

            for role in roles:
                if role:
                    role_stats[role] = len(role.members)

            embed = discord.Embed(title="Roleme Statistics", colour=0x005682)
            embed.description = ""
            r_stats_sorted = sorted(role_stats.items(), key=lambda x: x[1], reverse=True)
            desc_n = 65
            chunk_n = 30
            for r, c in r_stats_sorted[:desc_n]:
                embed.description += f"`{c}` {r.mention}\n"
            # if too long for embed description
            if len(r_stats_sorted) > desc_n:
                # chunk and put in fields
                stats_chunks = [r_stats_sorted[i:i + chunk_n]
                                for i in range(desc_n, len(r_stats_sorted), chunk_n)]
                for chunk in stats_chunks:
                    stats_str = ""
                    for r, c in chunk:
                        stats_str += f"`{c}` {r.mention}\n"
                    embed.add_field(name="...", value=stats_str, inline=False)
            user_count = len([x for x in ctx.guild.members if not x.bot])
            bot_count = ctx.guild.member_count - user_count
            embed.add_field(name="Total Members", value=f"Users: `{user_count}`\nBots: `{bot_count}`", inline=False)
            await ctx.send(embed=embed)

    @_role_stats.command(name="--all", aliases=["all", "-a", "a"], enabled=opt.enable_role_stats)
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def role_stats_all(self, ctx: commands.Context):
        """Show statistics for all roles. This command is admin-only."""
        role_stats: Dict[discord.Role, int] = {}

        roles = ctx.guild.roles
        for role in roles:
            if role.name != "@everyone":
                role_stats[role] = len(role.members)

        embed = discord.Embed(title="Role Statistics", colour=0x005682)
        embed.description = ""
        r_stats_sorted = sorted(role_stats.items(), key=lambda x: x[1], reverse=True)
        desc_n = 65
        chunk_n = 30
        for r, c in r_stats_sorted[:desc_n]:
            embed.description += f"`{c}` {r.mention}\n"
        # if too long for embed description
        if len(r_stats_sorted) > desc_n:
            # chunk and put in fields
            stats_chunks = [r_stats_sorted[i:i + chunk_n]
                            for i in range(desc_n, len(r_stats_sorted), chunk_n)]
            for chunk in stats_chunks:
                stats_str = ""
                for r, c in chunk:
                    stats_str += f"`{c}` {r.mention}\n"
                embed.add_field(name="...", value=stats_str, inline=False)
        user_count = len([x for x in ctx.guild.members if not x.bot])
        bot_count = ctx.guild.member_count - user_count
        embed.add_field(name="Total Members", value=f"Users: `{user_count}`\nBots: `{bot_count}`", inline=False)
        await ctx.send(embed=embed)
