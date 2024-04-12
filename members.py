import datetime

import discord
from discord import app_commands


def add_member_commands(bot, member_cycle, GUILD_ID):
    tree = app_commands.CommandTree(bot)

    @tree.command(guild=discord.Object(id=GUILD_ID), name='add_member', description='Adiciona um membro à lista')
    async def _add_member(interaction: discord.Interaction, name: str):
        with open('members.txt', 'a') as f:
            f.write(name + '\n')  # Add the new member to the file
        await interaction.response.send_message(f'{name} foi adicionado.', ephemeral=False)

    @tree.command(guild=discord.Object(id=GUILD_ID), name='list_members', description='Lista todos os membros')
    async def _list_members(interaction: discord.Interaction):
        with open('members.txt', 'r') as f:
            members_list = '\n'.join(sorted([line.strip() for line in f]))  # Read and sort the members from the file
        await interaction.response.send_message(f'Membros:\n{members_list}', ephemeral=False)

    @tree.command(guild=discord.Object(id=GUILD_ID), name='remove_member', description='Remove um membro da lista')
    async def _remove_member(interaction: discord.Interaction, name: str):
        with open('members.txt', 'r') as f:
            members = [line.strip() for line in f]
        if name in members:
            members.remove(name)
            with open('members.txt', 'w') as f:
                for member in members:
                    f.write(member + '\n')  # Write the updated members list to the file
            await interaction.response.send_message(f'{name} foi removido.', ephemeral=False)
        else:
            await interaction.response.send_message(f'{name} não foi encontrado.', ephemeral=False)

    @tree.command(guild=discord.Object(id=GUILD_ID), name='info', description='Mostra informações do servidor')
    async def _info(interaction: discord.Interaction):
        # Get the current server time
        server_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get the last member
        with open('last_member.txt', 'r') as f:
            last_member = f.read().strip()

        # Get the next member
        next_member = next(member_cycle)

        # Get the schedule
        schedule = get_schedule()
        day_map = {'mon': 'seg', 'tue': 'ter', 'wed': 'qua', 'thu': 'qui', 'fri': 'sex', 'sat': 'sab', 'sun': 'dom'}
        days = ', '.join(day_map[day] for day in schedule['days'].split(','))
        time = schedule['time']

        # Send the information
        await interaction.response.send_message(f'Hora atual do servidor: {server_time}\n'
                                                f'Último membro: {last_member}\n'
                                                f'Próximo membro: {next_member}\n'
                                                f'Escala: {days} às {time}', ephemeral=False)

    @tree.command(guild=discord.Object(id=GUILD_ID), name='set_schedule', description='Ajusta a escala')
    async def _set_schedule(interaction: discord.Interaction, days: str, time: str):
        # Validate and map the days
        day_map = {'seg': 'mon', 'ter': 'tue', 'qua': 'wed', 'qui': 'thu', 'sex': 'fri', 'sab': 'sat', 'dom': 'sun'}
        days = days.lower().split(',')
        if not all(day in day_map for day in days):
            await interaction.response.send_message('Dias inválidos. Use: seg, ter, qua, qui, sex, sab, dom',
                                                    ephemeral=False)
            return
        days_english = [day_map[day] for day in days]

        # Validate the time
        try:
            datetime.datetime.strptime(time, '%H:%M')
        except ValueError:
            await interaction.response.send_message('Hora inválida. Use o formato 24h, por exemplo: 14:30',
                                                    ephemeral=False)
            return

        # Write the new schedule to the file
        with open('schedule.txt', 'w') as f:
            f.write(f'days: {",".join(days_english)}\n')
            f.write(f'time: {time}\n')

        await interaction.response.send_message(
            f'Escala ajustada para: {", ".join(day.title() for day in days)} às {time}', ephemeral=False)

    return tree


def get_schedule():
    with open('schedule.txt', 'r') as f:
        lines = f.readlines()
    schedule = {}
    for line in lines:
        key, value = line.strip().split(': ')
        if key == 'days':
            # Convert the days to lowercase, take the first three characters, and remove spaces
            value = ','.join(day[:3].lower() for day in value.split(','))
        schedule[key] = value
    return schedule
