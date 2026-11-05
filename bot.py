"""Kiko: a Discord community automation bot for Gaming After Hours.

Features:
- Randomized embedded welcome messages
- Automatic role assignment to new members
- Administrator-only server rules command
- Welcome-message preview command
"""

import logging
import os
import random
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv


# Configuration ---------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1471286385276096648"))
AUTO_ROLE_ID = int(os.getenv("AUTO_ROLE_ID", "1471296422543495318"))

if not TOKEN or TOKEN == "your_new_token_here":
    raise RuntimeError("Set DISCORD_TOKEN in the .env file next to bot.py.")

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("kiko")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=commands.DefaultHelpCommand())


# Welcome embeds --------------------------------------------------------------
GREETINGS = [
    "Welcome to the realm, {user} 🖤.",
    "A new challenger appears, {user} ❗.",
    "The gospel grows stronger... welcome {user} 💯.",
    "Make way… {user} has entered the server 🔝.",
    "May your ping be low and your wins be many, {user} 🍀.",
    "Good to have you, {user}. Stay awhile 🤝.",
    "{user} just spawned in. Be kind 😘.",
    "Welcome, {user}. Your adventure starts now 🌹.",
    "The night watch welcomes you, {user} 🌑.",
    "All hail {user} 👑.",
]

WELCOME_TITLES = [
    "Welcome to the Guild",
    "A New Arrival",
    "Entry Confirmed",
    "Gate Opened",
    "Summoned to the Realm",
    "Initiation Complete",
]


def random_color() -> discord.Color:
    """Return a vivid but readable random embed accent color."""
    return discord.Color.from_rgb(*(random.randint(80, 255) for _ in range(3)))


def build_welcome_embed(member: discord.abc.User, guild: discord.Guild) -> discord.Embed:
    """Build a welcome embed for a new member or command preview."""
    embed = discord.Embed(
        title=random.choice(WELCOME_TITLES),
        description=random.choice(GREETINGS).format(user=member.mention),
        color=random_color(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    if guild.icon:
        embed.set_footer(text=guild.name, icon_url=guild.icon.url)
    else:
        embed.set_footer(text=guild.name)
    embed.add_field(name="Status", value="**Access Granted** ✅", inline=True)
    embed.add_field(name="Next Step", value="Read **#rules** ✅", inline=True)
    return embed


def build_rules_embed(guild: discord.Guild) -> discord.Embed:
    """Build the server's original code-of-conduct embed."""
    dark_colors = [
        discord.Color.dark_blue(),
        discord.Color.dark_purple(),
        discord.Color.dark_teal(),
        discord.Color.from_rgb(20, 20, 35),
        discord.Color.from_rgb(15, 10, 25),
    ]
    embed = discord.Embed(
        title="CODE OF CONDUCT",
        description="When the sleepmaxers log off… we lock in.\n\n**Late night grind zone.**",
        color=random.choice(dark_colors),
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="Gaming After Hours", icon_url=guild.icon.url)
    else:
        embed.set_footer(text="Gaming After Hours")
    embed.add_field(name="🎮 PLAY TO WIN!", value="Competitive energy is welcome.\nReal disrespect is not.", inline=False)
    embed.add_field(name="📵 No Spam", value="No flooding. No ping abuse. No random link dumps.", inline=False)
    embed.add_field(name="🚫 Keep It Clean", value="No NSFW content in GENERAL. Keep it in NSFW chat.", inline=False)
    embed.add_field(name="⚖️ Staff Authority", value="Respect Mods.", inline=False)
    embed.add_field(name="🔥 No Malding/Coping", value="Play to win or GTFO out.", inline=False)
    return embed


# Events ----------------------------------------------------------------------
@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id if bot.user else "unknown")


@bot.event
async def on_member_join(member: discord.Member) -> None:
    """Assign the configured role and post the member's welcome embed."""
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role is None:
        logger.warning("Auto-role %s not found in %s", AUTO_ROLE_ID, member.guild.name)
    else:
        try:
            await member.add_roles(role, reason="Auto-role on join")
        except discord.Forbidden:
            logger.error("Cannot assign role: check Manage Roles and role hierarchy")
        except discord.HTTPException as error:
            logger.error("Discord rejected role assignment: %s", error)

    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if not isinstance(channel, discord.TextChannel):
        logger.warning("Welcome text channel %s not found in %s", WELCOME_CHANNEL_ID, member.guild.name)
        return
    try:
        await channel.send(embed=build_welcome_embed(member, member.guild))
    except discord.Forbidden:
        logger.error("Cannot post welcome message: check Send Messages and Embed Links")
    except discord.HTTPException as error:
        logger.error("Discord rejected welcome message: %s", error)


# Text commands ---------------------------------------------------------------
@bot.command(name="testwelcome")
@commands.guild_only()
async def testwelcome(ctx: commands.Context) -> None:
    """Preview a randomly generated welcome message."""
    await ctx.send(embed=build_welcome_embed(ctx.author, ctx.guild))


@bot.command(name="rules")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def rules(ctx: commands.Context) -> None:
    """Post the server rules; requires Administrator permission."""
    await ctx.send(embed=build_rules_embed(ctx.guild))


@rules.error
async def rules_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server administrators can post the rules using this command.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command can only be used in a server.")
    else:
        logger.error("Rules command error: %s", error)


if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
