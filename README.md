
# Daily Schedule Bot for Discord


The Daily Schedule bot for Discord is here to help your team coordination. With just a simple setup, this bot leverages a list of your team members and autonomously selects one to lead your daily meetings. Gone are the days of manual selection or awkward rotations – our bot ensures a smooth and fair rotation of meeting leaders.

## Setup

To run this bot, you need to provide the server ID, the channel ID, and the token. These can be set in the main.py file.

```
GUILD_ID = 000  # Replace with your server ID
channel = self.get_channel(000)  # Replace with your channel ID
bot.run('discordToken')  # Replace with your token
```

## Installation

This bot can be run on your local machine or on a cloud bot server like DisCloudBot. To install the necessary dependencies, run the following command:

```
pip install -r requirements.txt
```

Note: **requirements.txt** and **discloud.config** are necessary only for DisCloudBot.

## Features

The bot provides the following commands:

1. **add_member:** Adds a member to the list.
2. **list_members:** Lists all members.
3. **remove_member:** Removes a member from the list.
4. **info:** Shows server information.
5. **set_schedule:** Adjusts the schedule.
   

## File Structure

The bot uses the following files:

1. **discloud.config:** Configuration file for DisCloudBot.
2. **last_member.txt:** Stores the last member who led the meeting.
3. **main.py:** Main script of the bot.
4. **members.py:** Contains functions to manage members and schedule.
5. **members.txt:** Stores the list of members.
6. **requirements.txt:** Contains the necessary Python packages to run the bot.
7. **schedule.txt:** Stores the schedule of the meetings.
   
## Schedule

The bot uses a schedule to determine when to send the daily message. The schedule is stored in schedule.txt and can be adjusted with the set_schedule command. The format of the schedule is as follows:

```
days: mon,tue,wed,thu,fri
time: 08:00
```

## Running the Bot
To run the bot, simply execute the main.py script:

```
python main.py
```
## Cloud Deployment
This bot can be easily deployed on a cloud bot server like DisCloudBot (https://docs.discloudbot.com/). Simply upload the bot's files and set the necessary environment variables (server ID, channel ID, and token).
