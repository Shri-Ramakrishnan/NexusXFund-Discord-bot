import os
import re
import asyncio

import discord
from discord import app_commands
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is missing. Check your .env file."
    )


# NexusXfund branding
BRAND_COLOR = 0x6C2BD9
WEBSITE_URL = "https://nexusxfund.com/en"

# Your Discord server ID
GUILD_ID = 1570780534475595817
GUILD = discord.Object(id=GUILD_ID)


# ============================================================
# INTENTS
# ============================================================

intents = discord.Intents.default()


# ============================================================
# BOT SETUP
# ============================================================

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


# ============================================================
# EMBED HELPER
# ============================================================

def nexus_embed(
    title: str,
    description: str,
    emoji: str = "💎"
) -> discord.Embed:

    embed = discord.Embed(
        title=f"{emoji} {title}",
        description=description,
        color=BRAND_COLOR
    )

    embed.set_author(
        name="NexusXfund"
    )

    embed.set_footer(
        text="NexusXfund • Official Community"
    )

    return embed


# ============================================================
# NORMALIZE CHANNEL / CATEGORY NAME
# ============================================================

def normalize_channel_name(name: str) -> str:

    name = name.lower()

    # Keep letters, numbers and hyphens
    name = re.sub(
        r"[^a-z0-9-]",
        "",
        name
    )

    return name


# ============================================================
# FIND TEXT CHANNEL
# ============================================================

def find_channel(
    guild: discord.Guild,
    target_name: str
):

    target = normalize_channel_name(
        target_name
    )

    for channel in guild.text_channels:

        actual = normalize_channel_name(
            channel.name
        )

        if actual == target:
            return channel

    return None


# ============================================================
# FIND SUPPORT CATEGORY
# ============================================================

def find_support_category(
    guild: discord.Guild
):

    # First try to find the category containing #support
    support_channel = find_channel(
        guild,
        "support"
    )

    if support_channel and support_channel.category:
        return support_channel.category

    # Fallback: find a category named support
    for category in guild.categories:

        actual = normalize_channel_name(
            category.name
        )

        if actual == "support":
            return category

    return None


# ============================================================
# CHANNEL CONTENT
# ============================================================

CHANNEL_MESSAGES = {

    "welcome": {

        "title": "Welcome to NexusXfund",

        "emoji": "🌸",

        "description": """
Welcome to the official **NexusXfund** community! 🚀

NexusXfund is building a trader-focused community where traders can connect, discuss markets, share experiences and stay updated with the platform.

### What you can do here

📊 **Trading Discussions**
Discuss trading ideas, strategies and experiences.

📈 **Market Analysis**
Share and discuss market analysis with fellow traders.

🧠 **Education**
Learn, improve and exchange knowledge with the community.

💎 **NexusXfund Updates**
Stay informed about official platform and company updates.

🤝 **Community**
Connect with traders and be part of the growing NexusXfund community.

Before participating, please take a moment to read the **Rules** and **FAQ**.

Welcome aboard! 🤝
"""
    },


    "announcements": {

        "title": "NexusXfund Announcements",

        "emoji": "📢",

        "description": """
Welcome to the official **NexusXfund Announcements** channel.

Important official announcements, major updates and community information will be posted here.

🔔 **Stay updated**

Make sure you have notifications enabled so you don't miss important announcements.

Only official NexusXfund announcements should be posted in this channel.
"""
    },


    "rules": {

        "title": "NexusXfund Rules",

        "emoji": "📜",

        "description": """
Welcome to the official **NexusXfund** community.

Please read and follow the rules below to help us maintain a safe, respectful and useful environment for everyone.

### 🚨 Beware of Scammers

Be extremely careful with unsolicited DMs claiming to represent NexusXfund.

Never share your:

• Passwords
• OTPs
• API keys
• Payment credentials
• Private keys
• Other sensitive information

If someone suspicious contacts you claiming to be staff, verify their identity through the official NexusXfund channels.

### 🤝 Be Respectful

Treat all community members, traders and staff with respect.

Harassment, personal attacks, discrimination and unnecessary hostility are not allowed.

### 🚫 No Spam

Do not spam:

• Messages
• Mentions
• Links
• Repeated content
• Unrelated material

Keep discussions relevant to the community.

### 📢 No Unauthorized Promotion

Do not promote unrelated services, products, referral links or other communities without permission from the NexusXfund team.

### 🔒 Protect Your Information

Never publicly share sensitive account or payment information.

If you need help with an account-related issue, use the appropriate support channel.

### 📝 Use the Correct Channels

Please use the appropriate channel for your discussion.

📊 Trading → **#trading-discussion**

📈 Market Analysis → **#market-analysis**

🧠 Education → **#education**

🏆 Trader Experiences → **#trader-experiences**

🎟️ Support → **#support**

### ⚠️ Follow Staff Instructions

Please cooperate with moderators and staff when they are managing the community.

Moderators may remove content or take other action when necessary to protect the server.

### 🎉 Enjoy the Community

Share knowledge, discuss markets, help other traders and contribute positively to the NexusXfund community.

By participating in this server, you agree to follow these rules.
"""
    },


    "faq": {

        "title": "NexusXfund FAQ",

        "emoji": "❓",

        "description": f"""
### What is NexusXfund?

NexusXfund is a trading-focused prop firm with its own Nexus Pro platform.

### 🌐 Where can I learn more?

You can find official NexusXfund information on the website:

{WEBSITE_URL}

### 🎟️ Where can I get support?

For assistance, please use the official **#support** channel and open a support ticket.

### 📊 Where can I discuss trading?

Use **#trading-discussion** for general trading conversations.

Use **#market-analysis** for market-related analysis.

### 📢 Where can I find official updates?

Check:

📢 **#announcements**

📰 **#platform-updates**

### 💰 Where can I find payout information?

Official payout-related information will be shared in:

💰 **#payouts**

For personal account questions, please open a ticket in **#support** and never post sensitive information publicly.

### 🤝 Can I promote my own service?

Unauthorized promotion is not allowed.

If you are interested in an official partnership or affiliate opportunity, please contact the NexusXfund team.

### ❓ Still have a question?

Ask the community in **#general** or open a support ticket through **#support**.

⚠️ For important information, always verify details through official NexusXfund channels.
"""
    },


    "platform-updates": {

        "title": "NexusXfund Platform Updates",

        "emoji": "📰",

        "description": """
This channel is dedicated to official **NexusXfund platform updates**.

Updates relating to the Nexus Pro platform, features, maintenance and other important platform-related information will be shared here.

🔔 Keep notifications enabled to stay informed.

Only official NexusXfund updates should be posted in this channel.
"""
    },


    "payouts": {

        "title": "NexusXfund Payouts",

        "emoji": "💰",

        "description": """
Welcome to the official **NexusXfund Payouts** channel.

Official payout-related announcements, updates and community information will be shared here.

### 🔒 Keep Your Information Safe

Never post:

• Passwords
• Payment credentials
• Account credentials
• Personal financial information

For questions regarding an individual account or payout, please open a support ticket in **#support**.

⚠️ Be cautious of anyone asking you for money or sensitive information through DMs.
"""
    },


    "affiliates": {

        "title": "NexusXfund Affiliates",

        "emoji": "🤝",

        "description": """
Welcome to the official **NexusXfund Affiliates** channel.

This channel will be used for official affiliate information, campaigns, updates and resources.

### 🤝 Interested in becoming an affiliate?

Official information about affiliate opportunities and campaigns will be shared here.

### 🚨 Stay Alert

Be cautious of unofficial affiliate offers or individuals impersonating NexusXfund staff.

Always verify important information through official NexusXfund channels.
"""
    }
}


# ============================================================
# CREATE EMBED
# ============================================================

def create_embed(channel_key: str):

    data = CHANNEL_MESSAGES[channel_key]

    return nexus_embed(
        title=data["title"],
        description=data["description"],
        emoji=data["emoji"]
    )


# ============================================================
# WEBSITE BUTTON
# ============================================================

class NexusButtons(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(
                label="NexusXfund Website",
                url=WEBSITE_URL,
                emoji="🌐"
            )
        )


# ============================================================
# SUPPORT TICKET BUTTONS
# ============================================================

class SupportPanelView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Open Support Ticket",
        style=discord.ButtonStyle.primary,
        emoji="🎫",
        custom_id="nexus_open_ticket"
    )
    async def open_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ This button can only be used inside a server.",
                ephemeral=True
            )
            return

        # Check if user already has a ticket
        for channel in guild.text_channels:

            if (
                channel.name.startswith("ticket-")
                and interaction.user.id in [
                    member.id for member in channel.members
                ]
            ):
                await interaction.response.send_message(
                    f"❌ You already have an open ticket: {channel.mention}",
                    ephemeral=True
                )
                return

        # Find support category
        category = find_support_category(guild)

        if category is None:

            await interaction.response.send_message(
                "❌ Support category could not be found. Please contact an administrator.",
                ephemeral=True
            )

            return

        # Create private ticket
        ticket_name = f"ticket-{interaction.user.name}"

        # Discord channel names cannot contain certain characters
        ticket_name = re.sub(
            r"[^a-zA-Z0-9-]",
            "",
            ticket_name
        ).lower()

        # Limit channel name length
        ticket_name = ticket_name[:90]

        # Permission overwrites
        overwrites = {

            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True
            ),

            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True,
                manage_messages=True
            )
        }

        # Only the Moderator role can access support tickets
        moderator_role = discord.utils.get(
            guild.roles,
            name="Moderator"
        )

        if moderator_role:
            overwrites[moderator_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_messages=True
            )

        try:

            ticket_channel = await guild.create_text_channel(
                name=ticket_name,
                category=category,
                overwrites=overwrites,
                topic=f"NexusXfund support ticket | User ID: {interaction.user.id}"
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ I don't have permission to create ticket channels.",
                ephemeral=True
            )

            return

        except Exception as error:

            print(f"Ticket creation error: {error}")

            await interaction.response.send_message(
                "❌ Something went wrong while creating your ticket.",
                ephemeral=True
            )

            return

        # Ticket embed
        embed = nexus_embed(
            title="NexusXfund Support Ticket",
            description=f"""
Welcome {interaction.user.mention}! 👋

Thank you for contacting **NexusXfund Support**.

Please explain your issue clearly and provide any relevant information or screenshots.

### 📌 Please remember

• Do not share your password.
• Do not share OTPs.
• Do not share private keys.
• Do not share API keys.
• Do not share payment credentials.

A member of the NexusXfund team will assist you as soon as possible.

🔒 **This ticket is private.**
""",
            emoji="🎫"
        )

        # Send ticket message
        await ticket_channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=TicketCloseView()
        )

        await interaction.response.send_message(
            f"✅ Your support ticket has been created: {ticket_channel.mention}",
            ephemeral=True
        )


# ============================================================
# CLOSE TICKET BUTTON
# ============================================================

class TicketCloseView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="nexus_close_ticket"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        channel = interaction.channel

        if channel is None:
            return

        # Only allow closing inside ticket channels
        if not channel.name.startswith("ticket-"):

            await interaction.response.send_message(
                "❌ This is not a support ticket.",
                ephemeral=True
            )

            return

        # Check if user is ticket owner
        is_owner = False

        if isinstance(channel, discord.TextChannel):

            if channel.topic:
                owner_match = re.search(
                    r"User ID: (\d+)",
                    channel.topic
                )

                if owner_match:

                    owner_id = int(
                        owner_match.group(1)
                    )

                    if interaction.user.id == owner_id:
                        is_owner = True

        # Check admin permissions
        is_admin = interaction.user.guild_permissions.administrator

        # Check staff roles
        is_staff = False

        staff_role_names = [
            "NexusXfund Staff",
            "Support",
            "Moderator",
            "Admin",
            "Administrator"
        ]

        for role in interaction.user.roles:

            if role.name in staff_role_names:
                is_staff = True
                break

        if not is_owner and not is_admin and not is_staff:

            await interaction.response.send_message(
                "❌ You don't have permission to close this ticket.",
                ephemeral=True
            )

            return

        await interaction.response.send_message(
            "🔒 Closing this ticket in 5 seconds...",
            ephemeral=False
        )

        await asyncio.sleep(5)

        try:
            await channel.delete(
                reason=f"Ticket closed by {interaction.user}"
            )

        except discord.Forbidden:

            print(
                f"Could not delete ticket #{channel.name}"
            )

        except Exception as error:

            print(
                f"Ticket deletion error: {error}"
            )


# ============================================================
# CHECK IF BOT ALREADY POSTED
# ============================================================

async def already_setup(channel):

    try:

        async for message in channel.history(limit=50):

            if (
                message.author == bot.user
                and message.embeds
            ):
                return True

    except discord.Forbidden:

        return False

    return False


# ============================================================
# BOT READY
# ============================================================

@bot.event
async def on_ready():

    print("----------------------------------------")
    print(f"Logged in as {bot.user}")
    print(f"Connected to {len(bot.guilds)} server(s)")

    # Register persistent ticket buttons
    bot.add_view(SupportPanelView())
    bot.add_view(TicketCloseView())

    # Force slash commands to sync directly to this server
    tree.copy_global_to(guild=GUILD)

    synced = await tree.sync(
        guild=GUILD
    )

    print(
        f"Synced {len(synced)} slash command(s) to server"
    )

    print("----------------------------------------")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="NexusXfund Traders"
        )
    )


# ============================================================
# MEMBER JOIN
# ============================================================

@bot.event
async def on_member_join(member):

    channel = find_channel(
        member.guild,
        "welcome"
    )

    if channel is None:
        return

    embed = nexus_embed(
        title="Welcome to NexusXfund!",
        description=f"""
Welcome {member.mention}! 👋

We're glad to have you here.

Make sure to check out:

📜 **#rules**
❓ **#faq**
📊 **#trading-discussion**
📈 **#market-analysis**
🧠 **#education**
🎟️ **#support**

If you need assistance, open a private support ticket in **#support**.

Enjoy the community and trade responsibly! 🚀
""",
        emoji="🌸"
    )

    try:

        await channel.send(
            embed=embed
        )

    except discord.Forbidden:

        print(
            f"Cannot send welcome message in #{channel.name}"
        )


# ============================================================
# /SETUP
# ============================================================

@tree.command(
    name="setup",
    description="Set up the official NexusXfund information channels"
)
@app_commands.checks.has_permissions(
    administrator=True
)
async def setup(
    interaction: discord.Interaction
):

    await interaction.response.defer(
        ephemeral=True
    )

    guild = interaction.guild

    if guild is None:

        await interaction.followup.send(
            "❌ This command can only be used inside a server.",
            ephemeral=True
        )

        return

    posted_channels = []
    skipped_channels = []
    missing_channels = []

    for channel_key in CHANNEL_MESSAGES:

        channel = find_channel(
            guild,
            channel_key
        )

        if channel is None:

            missing_channels.append(
                channel_key
            )

            continue

        # Prevent duplicates
        if await already_setup(channel):

            skipped_channels.append(
                channel.name
            )

            continue

        try:

            embed = create_embed(
                channel_key
            )

            await channel.send(
                embed=embed,
                view=NexusButtons()
            )

            posted_channels.append(
                channel.name
            )

        except discord.Forbidden:

            missing_channels.append(
                f"{channel.name} (no permission)"
            )

        except Exception as error:

            print(
                f"Error posting to #{channel.name}: {error}"
            )

            missing_channels.append(
                f"{channel.name} (error)"
            )

    result = (
        "## ✅ NexusXfund Setup Completed!\n\n"
    )

    if posted_channels:

        result += "**Posted to:**\n"

        for channel in posted_channels:

            result += f"• #{channel}\n"

    if skipped_channels:

        result += "\n**Already configured:**\n"

        for channel in skipped_channels:

            result += f"• #{channel}\n"

    if missing_channels:

        result += "\n**⚠️ Not posted:**\n"

        for channel in missing_channels:

            result += f"• {channel}\n"

    result += (
        "\nThe NexusXfund information channels "
        "have been configured."
    )

    await interaction.followup.send(
        result,
        ephemeral=True
    )


# ============================================================
# /SETUP-SUPPORT
# ============================================================

@tree.command(
    name="setup-support",
    description="Set up the NexusXfund support ticket panel"
)
@app_commands.checks.has_permissions(
    administrator=True
)
async def setup_support(
    interaction: discord.Interaction
):

    await interaction.response.defer(
        ephemeral=True
    )

    guild = interaction.guild

    if guild is None:

        await interaction.followup.send(
            "❌ This command can only be used inside a server.",
            ephemeral=True
        )

        return

    support_channel = find_channel(
        guild,
        "support"
    )

    if support_channel is None:

        await interaction.followup.send(
            "❌ #support channel not found.",
            ephemeral=True
        )

        return

    # Check whether ticket panel already exists
    async for message in support_channel.history(limit=50):

        if (
            message.author == bot.user
            and message.embeds
            and message.embeds[0].title
            and "Support Center" in message.embeds[0].title
        ):

            await interaction.followup.send(
                "⚠️ The support ticket panel is already configured in #support.",
                ephemeral=True
            )

            return

    embed = nexus_embed(
        title="NexusXfund Support Center",
        description="""
Need help with NexusXfund?

Our support team is here to help.

### 🎫 Open a Support Ticket

Click the button below to create a **private support ticket**.

Your ticket will only be visible to you and authorized NexusXfund staff.

### 🔒 Security Reminder

NexusXfund staff will never ask you for:

• Passwords
• OTPs
• Private keys
• API keys
• Payment credentials

Never share sensitive information with anyone through Discord.

### 📌 Before opening a ticket

Please explain your issue clearly and include relevant screenshots or information when necessary.

**Click the button below to get started.**
""",
        emoji="🎫"
    )

    await support_channel.send(
        embed=embed,
        view=SupportPanelView()
    )

    await interaction.followup.send(
        "✅ Support ticket panel has been posted in #support.",
        ephemeral=True
    )


# ============================================================
# /HELP
# ============================================================

@tree.command(
    name="help",
    description="Show NexusXfund bot commands"
)
async def help_command(
    interaction: discord.Interaction
):

    embed = nexus_embed(
        title="NexusXfund Bot",
        description="""
### 👤 Community Commands

`/help` — Show available commands

`/rules` — View server rules

`/faq` — View frequently asked questions

`/support` — Open support information

`/links` — View official NexusXfund links

### 🎫 Support

Use **#support** to open a private support ticket.

### 🛡️ Admin Commands

`/setup` — Configure NexusXfund information channels

`/setup-support` — Configure the support ticket panel

`/announce` — Publish an announcement

`/update` — Publish a platform update

`/payout` — Publish a payout update

`/affiliate` — Publish an affiliate update

`/clear` — Delete recent messages

Only authorized administrators can use administrative commands.
""",
        emoji="🤖"
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )


# ============================================================
# /RULES
# ============================================================

@tree.command(
    name="rules",
    description="Show NexusXfund server rules"
)
async def rules_command(
    interaction: discord.Interaction
):

    embed = create_embed("rules")

    await interaction.response.send_message(
        embed=embed
    )


# ============================================================
# /FAQ
# ============================================================

@tree.command(
    name="faq",
    description="Show NexusXfund FAQ"
)
async def faq_command(
    interaction: discord.Interaction
):

    embed = create_embed("faq")

    await interaction.response.send_message(
        embed=embed
    )


# ============================================================
# /SUPPORT
# ============================================================

@tree.command(
    name="support",
    description="Show NexusXfund support information"
)
async def support_command(
    interaction: discord.Interaction
):

    embed = nexus_embed(
        title="NexusXfund Support",
        description="""
Need help with NexusXfund?

🎫 Go to **#support** and click **Open Support Ticket**.

A private ticket will be created for you where you can explain your issue directly to the support team.

### 🔒 Security Reminder

NexusXfund staff will never ask you to provide:

• Passwords
• OTPs
• Private keys
• API keys
• Payment credentials

Be careful with unsolicited DMs and always verify that you're communicating with an official NexusXfund representative.
""",
        emoji="🎟️"
    )

    await interaction.response.send_message(
        embed=embed,
        view=NexusButtons(),
        ephemeral=True
    )


# ============================================================
# /LINKS
# ============================================================

@tree.command(
    name="links",
    description="Show official NexusXfund links"
)
async def links_command(
    interaction: discord.Interaction
):

    embed = nexus_embed(
        title="Official NexusXfund Links",
        description=f"""
🌐 **Website**

{WEBSITE_URL}

Always verify links through official NexusXfund channels.

⚠️ Be careful with fake websites and impersonators.
""",
        emoji="🔗"
    )

    await interaction.response.send_message(
        embed=embed,
        view=NexusButtons(),
        ephemeral=True
    )


# ============================================================
# /ANNOUNCE
# ============================================================

@tree.command(
    name="announce",
    description="Publish an official NexusXfund announcement"
)
@app_commands.checks.has_permissions(
    administrator=True
)
@app_commands.describe(
    message="Announcement message"
)
async def announce_command(
    interaction: discord.Interaction,
    message: str
):

    channel = find_channel(
        interaction.guild,
        "announcements"
    )

    if channel is None:

        await interaction.response.send_message(
            "❌ #announcements channel not found.",
            ephemeral=True
        )

        return

    embed = nexus_embed(
        title="Official Announcement",
        description=message,
        emoji="📢"
    )

    await channel.send(
        embed=embed
    )

    await interaction.response.send_message(
        "✅ Announcement published.",
        ephemeral=True
    )


# ============================================================
# /UPDATE
# ============================================================

@tree.command(
    name="update",
    description="Publish a NexusXfund platform update"
)
@app_commands.checks.has_permissions(
    administrator=True
)
@app_commands.describe(
    message="Platform update"
)
async def update_command(
    interaction: discord.Interaction,
    message: str
):

    channel = find_channel(
        interaction.guild,
        "platform-updates"
    )

    if channel is None:

        await interaction.response.send_message(
            "❌ #platform-updates channel not found.",
            ephemeral=True
        )

        return

    embed = nexus_embed(
        title="Platform Update",
        description=message,
        emoji="📰"
    )

    await channel.send(
        embed=embed
    )

    await interaction.response.send_message(
        "✅ Platform update published.",
        ephemeral=True
    )


# ============================================================
# /PAYOUT
# ============================================================

@tree.command(
    name="payout",
    description="Publish a NexusXfund payout update"
)
@app_commands.checks.has_permissions(
    administrator=True
)
@app_commands.describe(
    message="Payout update"
)
async def payout_command(
    interaction: discord.Interaction,
    message: str
):

    channel = find_channel(
        interaction.guild,
        "payouts"
    )

    if channel is None:

        await interaction.response.send_message(
            "❌ #payouts channel not found.",
            ephemeral=True
        )

        return

    embed = nexus_embed(
        title="Payout Update",
        description=message,
        emoji="💰"
    )

    await channel.send(
        embed=embed
    )

    await interaction.response.send_message(
        "✅ Payout update published.",
        ephemeral=True
    )


# ============================================================
# /AFFILIATE
# ============================================================

@tree.command(
    name="affiliate",
    description="Publish a NexusXfund affiliate update"
)
@app_commands.checks.has_permissions(
    administrator=True
)
@app_commands.describe(
    message="Affiliate announcement"
)
async def affiliate_command(
    interaction: discord.Interaction,
    message: str
):

    channel = find_channel(
        interaction.guild,
        "affiliates"
    )

    if channel is None:

        await interaction.response.send_message(
            "❌ #affiliates channel not found.",
            ephemeral=True
        )

        return

    embed = nexus_embed(
        title="Affiliate Update",
        description=message,
        emoji="🤝"
    )

    await channel.send(
        embed=embed
    )

    await interaction.response.send_message(
        "✅ Affiliate update published.",
        ephemeral=True
    )


# ============================================================
# /CLEAR
# ============================================================

@tree.command(
    name="clear",
    description="Delete recent messages from this channel"
)
@app_commands.checks.has_permissions(
    administrator=True
)
@app_commands.describe(
    amount="Number of messages to delete"
)
async def clear_command(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 100]
):

    await interaction.response.defer(
        ephemeral=True
    )

    deleted = await interaction.channel.purge(
        limit=amount
    )

    await interaction.followup.send(
        f"🧹 Deleted {len(deleted)} message(s).",
        ephemeral=True
    )


# ============================================================
# COMMAND ERROR HANDLER
# ============================================================

async def permission_error(
    interaction: discord.Interaction,
    error
):

    if isinstance(
        error,
        app_commands.errors.MissingPermissions
    ):

        message = (
            "❌ You need Administrator permission "
            "to use this command."
        )

    else:

        print(
            f"Command error: {error}"
        )

        message = (
            "❌ Something went wrong while "
            "executing the command."
        )

    if interaction.response.is_done():

        await interaction.followup.send(
            message,
            ephemeral=True
        )

    else:

        await interaction.response.send_message(
            message,
            ephemeral=True
        )


# Attach permission error handlers
setup.error(permission_error)
setup_support.error(permission_error)
announce_command.error(permission_error)
update_command.error(permission_error)
payout_command.error(permission_error)
affiliate_command.error(permission_error)
clear_command.error(permission_error)


# ============================================================
# RUN BOT
# ============================================================

if __name__ == "__main__":
    bot.run(TOKEN)
