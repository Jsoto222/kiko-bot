import random
import discord
import os
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = 1471286385276096648
AUTO_ROLE_ID = 1471296422543495318

# -----------------------------
# INTENTS
# -----------------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# WELCOME CONTENT
# -----------------------------
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
    "All hail {user} 👑."
]

WELCOME_TITLES = [
    "Welcome to the Guild",
    "A New Arrival",
    "Entry Confirmed",
    "Gate Opened",
    "Summoned to the Realm",
    "Initiation Complete"
]

def random_color():
    return discord.Color.from_rgb(
        random.randint(80, 255),
        random.randint(80, 255),
        random.randint(80, 255)
    )

def build_welcome_embed(member_or_user, guild):
    greeting = random.choice(GREETINGS).format(user=member_or_user.mention)
    title = random.choice(WELCOME_TITLES)

    embed = discord.Embed(
        title=title,
        description=greeting,
        color=random_color()
    )

    embed.set_thumbnail(url=member_or_user.display_avatar.url)

    if guild and guild.icon:
        embed.set_footer(text=guild.name, icon_url=guild.icon.url)
    elif guild:
        embed.set_footer(text=guild.name)

    embed.add_field(name="Status", value="**Access Granted** ✅", inline=True)
    embed.add_field(name="Next Step", value="Read **#rules** ✅", inline=True)

    return embed

# -----------------------------
# EVENTS
# -----------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_member_join(member: discord.Member):
    # Auto-role
    try:
        role = member.guild.get_role(AUTO_ROLE_ID)
        if role:
            await member.add_roles(role, reason="Auto-role on join")
        else:
            print("❌ Role not found. Check AUTO_ROLE_ID.")
    except discord.Forbidden:
        print("❌ Missing Manage Roles or role hierarchy issue.")
    except Exception as e:
        print(f"❌ Role error: {e}")

    # Welcome message
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = build_welcome_embed(member, member.guild)
        await channel.send(embed=embed)
    else:
        print("❌ Welcome channel not found. Check WELCOME_CHANNEL_ID.")

# -----------------------------
# COMMANDS
# -----------------------------
@bot.command()
async def testwelcome(ctx):
    embed = build_welcome_embed(ctx.author, ctx.guild)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def rules(ctx):
    dark_colors = [
        discord.Color.dark_blue(),
        discord.Color.dark_purple(),
        discord.Color.dark_teal(),
        discord.Color.from_rgb(20, 20, 35),
        discord.Color.from_rgb(15, 10, 25)
    ]

    embed = discord.Embed(
        title="CODE OF CONDUCT",
        description=(
            "When the sleepmaxers log off… we lock in.\n\n"
            "**Late night grind zone.**"
        ),
        color=random.choice(dark_colors)
    )

    # Server icon thumbnail (animated if available)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)

    embed.add_field(
        name="🎮 PLAY TO WIN! ",
        value="Competitive energy is welcome.\nReal disrespect is not.",
        inline=False
    )

    embed.add_field(
        name="📵 No Spam",
        value="No flooding. No ping abuse. No random link dumps.",
        inline=False
    )

    embed.add_field(
        name="🚫 Keep It Clean",
        value="No NSFW content in GENERAL. Keep it in NSFW chat.",
        inline=False
    )

    embed.add_field(
        name="⚖️ Staff Authority",
        value="Respect Mods.",
        inline=False
    )

    embed.add_field(
        name="🔥 No Malding/Coping",
        value="Play to win or GTFO out.",
        inline=False
    )

    if ctx.guild.icon:
        embed.set_footer(
            text="Gaming After Hours",
            icon_url=ctx.guild.icon.url
        )
    else:
        embed.set_footer(text="Gaming After Hours")

    await ctx.send(embed=embed)

# -----------------------------
# RUN
# -----------------------------
if not TOKEN:
    raise ValueError("DISCORD_TOKEN env var not set!")

bot.run(TOKEN)