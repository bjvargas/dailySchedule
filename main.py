import discord
import datetime
import itertools
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from members import add_member_commands, get_schedule

GUILD_ID = 000 #

# Read members from a file
with open('members.txt', 'r') as f:
    members = {line.strip() for line in f}

schedule = get_schedule()
days = schedule['days']
time = datetime.datetime.strptime(schedule['time'], '%H:%M').time()


class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synced = False
        try:
            with open('last_member.txt', 'r') as f:
                last_member = f.read().strip()
            with open('members.txt', 'r') as f:
                members = [line.strip() for line in f]
            members_list = sorted(members)  # Sort the members list
            last_member_index = members_list.index(last_member) if last_member in members_list else 0
            self.member_cycle = itertools.cycle(members_list[last_member_index:] + members_list[:last_member_index])
            next(self.member_cycle)  # Advance the cycle once to get the next member
        except FileNotFoundError:
            self.member_cycle = itertools.cycle(sorted(members))  # Create the member cycle with the initial members
        self.tree = add_member_commands(self, self.member_cycle, GUILD_ID)

        # Create a background scheduler
        self.scheduler = BackgroundScheduler()
        # Add a job to the scheduler
        self.scheduler.add_job(self.daily_message, CronTrigger(day_of_week=days, hour=time.hour, minute=time.minute))
        # Start the scheduler
        self.scheduler.start()

    async def daily_message(self):
        channel = self.get_channel(
            000)  # Replace with the ID of the channel where you want to send the message
        member = next(self.member_cycle)  # Get the next member from the cycle
        with open('last_member.txt', 'w') as f:
            f.write(member)
        await channel.send(f'Hoje é a vez de {member}!')

    async def on_ready(self):
        if not self.synced:
            await self.tree.sync(guild=discord.Object(id=GUILD_ID))
            self.synced = True
        print(f"Entramos como {self.user}.")


bot = MyBot(intents=discord.Intents.default())
bot.run('discordToken')
