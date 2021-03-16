import discord
from discord.ext import commands
from pydactyl import PterodactylClient


botclient = commands.Bot(command_prefix = '$')
botclient.remove_command('help')

######################
#### CHANGE THESE ####
######################

url = 'https://example.com'
api_key = 'apiKey'

discord_token = "token"

server_ip = 'play.server.com'

###############
@botclient.event
async def on_ready():
    print('Bot is ready.')

client = PterodactylClient(url, api_key)
my_servers = client.client.list_servers()
srv_id = my_servers[0]['identifier']

@botclient.command(name='start')
async def start(ctx):
    srv_utilization = client.client.get_server_utilization(srv_id)
    if(srv_utilization.get("state") == 'off' or "offline"):
            client.client.send_power_action(srv_id, 'start')
            embed = discord.Embed(
                colour = discord.Color.blue(),
                title="Starting server", 
                description="**Have fun**"
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send('Server is already up or starting up!')

@botclient.command(name='restart')
async def restart(ctx):
    srv_utilization = client.client.get_server_utilization(srv_id)
    if(srv_utilization.get("state") == 'on' or 'online'):
            client.client.send_power_action(srv_id, 'restart')
            embed = discord.Embed(
                colour = discord.Color.blue(),
                title="Restarting server", 
                description="**See you soon**"
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send('Server is offline!')

@botclient.command(name='status')
async def status(ctx):
    srv_utilization = client.client.get_server_utilization(srv_id)
    if(srv_utilization.get("state") == 'on' or 'online'):
            clor = discord.Colour.green()
    elif(srv_utilization.get("state") == 'starting'):
        clor = discord.Colour.orange()
    else:
        clor = discord.Colour.red()

    embed = discord.Embed(
        colour = clor
    )
    embed.set_author(name=ctx.author)
    embed.add_field(name='Server status: ', value=srv_utilization.get("state"), inline=False)
    embed.add_field(name='Memory(RAM) usage: ', value=str(srv_utilization.get('memory').get('current')) + 'MB' + '/' + str(srv_utilization.get('memory').get('limit')) + 'MB', inline=False)
    embed.add_field(name='CPU usage: ', value=str(srv_utilization.get("cpu").get("current")) + '%', inline=False)
    embed.add_field(name='Disk usage: ', value=str(srv_utilization.get('disk').get('current')) + 'MB' + '/' + str(srv_utilization.get('disk').get('limit')) + 'MB', inline=False)

    await ctx.send(embed=embed)

@botclient.command(name='stop')
async def stop(ctx):
    srv_utilization = client.client.get_server_utilization(srv_id)
    if(srv_utilization.get("state") == 'on' or 'online'):
            client.client.send_power_action(srv_id, 'stop')
            embed = discord.Embed(
                colour = discord.Color.blue(),
                title="Stopping server", 
                description="**Hope you had a great time**"
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send('Server is already off!')

@botclient.command(name='ip')
async def ip(ctx):
    embed = discord.Embed(
        colour = discord.Color.blue(),
        title="Server IP:", 
        description="**{server_ip}**"
    )

    embed.add_field(name="Version", value="1.16.5", inline=True)

    await ctx.send(embed=embed)

botclient.run(discord_token)