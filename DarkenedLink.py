import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
import requests
from bs4 import BeautifulSoup  # For Kick web scraping
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Load the Discord token
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN is not found in the .env file!")

# Define the bot and prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ---- Kick Integration ----
@bot.command(name='kick_live')
async def kick_live(ctx, username):
    """Check if a Kick streamer is live."""
    url = f"https://kick.com/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Look for the "LIVE" indicator on the page
        live_indicator = soup.find("span", text="LIVE")
        if live_indicator:
            await ctx.send(f"{username} is currently live on Kick! Watch here: {url}")
        else:
            await ctx.send(f"{username} is not live on Kick.")
    else:
        await ctx.send(f"Failed to fetch data for {username} (Status code: {response.status_code}).")

@tasks.loop(minutes=5)
async def monitor_kick_live():
    """Periodically check if specific Kick streamers are live."""
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your Discord channel ID
    streamers = ["streamer1", "streamer2"]  # Replace with the usernames of Kick streamers you want to monitor

    for username in streamers:
        url = f"https://kick.com/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            live_indicator = soup.find("span", text="LIVE")
            if live_indicator:
                await channel.send(f"{username} is live on Kick! Watch here: {url}")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # Start monitoring Kick live streams
    monitor_kick_live.start()

# ---- Centralized Task Manager (existing functionality) ----
tasks_db = {}

@bot.command(name='create_task')
async def create_task(ctx, task_name, deadline: str):
    """Create a new task with a deadline."""
    tasks_db[task_name] = {'deadline': deadline, 'status': 'Pending'}
    await ctx.send(f'Task "{task_name}" created with deadline: {deadline}')

@bot.command(name='assign_task')
async def assign_task(ctx, task_name, assignee: discord.Member):
    """Assign a task to a member."""
    if task_name in tasks_db:
        tasks_db[task_name]['assignee'] = assignee.name
        await ctx.send(f'Task "{task_name}" assigned to {assignee.mention}')
    else:
        await ctx.send(f'Task "{task_name}" not found.')

@bot.command(name='track_task')
async def track_task(ctx, task_name):
    """Track a task's progress."""
    if task_name in tasks_db:
        task = tasks_db[task_name]
        await ctx.send(f'Task: {task_name}\nDeadline: {task["deadline"]}\nStatus: {task["status"]}\nAssigned to: {task.get("assignee", "No one")}')
    else:
        await ctx.send(f'Task "{task_name}" not found.')

@bot.command(name='complete_task')
async def complete_task(ctx, task_name):
    """Mark a task as completed."""
    if task_name in tasks_db:
        tasks_db[task_name]['status'] = 'Completed'
        await ctx.send(f'Task "{task_name}" marked as completed!')
    else:
        await ctx.send(f'Task "{task_name}" not found.')

@bot.command(name='delete_task')
async def delete_task(ctx, task_name):
    """Delete a task."""
    if task_name in tasks_db:
        del tasks_db[task_name]
        await ctx.send(f'Task "{task_name}" has been deleted')
    else:
        await ctx.send(f'Task "{task_name}" not found.')

# ---- Role Request and Approval System (existing functionality) ----
@bot.command(name='request_role')
async def request_role(ctx, role_name):
    """Request a role by a user."""
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.send(f'{ctx.author.mention} has requested the role {role_name}. Awaiting approval...')
    else:
        await ctx.send(f'Role "{role_name}" does not exist in this server.')

@bot.command(name='approve_role')
@has_permissions(manage_roles=True)
async def approve_role(ctx, member: discord.Member, role_name):
    """Approve a role request."""
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been assigned the role {role_name}.')
    else:
        await ctx.send(f'Role "{role_name}" does not exist.')

@approve_role.error
async def approve_role_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have permission to approve roles.")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)

