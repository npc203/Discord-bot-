import discord
import os
from discord.ext import commands
import datetime
import aiohttp
import utils
from utils import database as db
client = commands.Bot(command_prefix='--')
client.remove_command('help')

client.session = aiohttp.ClientSession()


#client.load_extension('cogs.chats')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
     client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("ready")


@client.event
async def on_command(ctx):
    await client.get_channel(743038667362140262).send(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+','+str(ctx.command)+','+str(ctx.guild)+','+str(ctx.channel)+','+str(ctx.message.author)+'\n')
    if ctx.channel.name not in ("spams",):
        check = db.update_one({'id':ctx.author.id},{'$inc':{"cmd_count":1,"xp":4}})

    #print(ctx.command,ctx.guild,ctx.channel,ctx.message.author)

@client.event
async def on_command_error(ctx,err):
    try:
        if isinstance(err.original,discord.Forbidden):
            halp = discord.Embed(title='Missing permissions!',description="Please give me permissions senpai",color=discord.Color.red())
            halp.set_thumbnail(url="https://media1.tenor.com/images/9eff85aac8f21da39246ef40787864c8/tenor.gif?itemid=7357054")
            await ctx.send(embed=halp)
    except:
        pass
    if isinstance(err,commands.CommandNotFound):
        pass
    elif isinstance(err, commands.CommandOnCooldown):
            msg = 'UwU Don\'t abuse me senpai,try again in {:.2f}s'.format(err.retry_after)
            await ctx.send(msg)
    elif isinstance(err,TypeError):
        ctx.send('*Umm, check the way on how to use me baka!, type: `--help <command-name> to learn more`')
    else:
        await client.get_channel(745259187457490946).send(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+','+str(ctx.command)+','+str(ctx.message.author)+','+str(ctx.guild)+','+str(err))

'''
@client.command()
async def help(ctx):
    embed=discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name="Bot commands",icon_url="https://cdn.discordapp.com/avatars/601962388006109195/fb5e87a846e7e7ce12f07109f0a71802.png")
    embed.add_field(name='Information',value="ping,wiki",inline=True)
    embed.add_field(name='Chats',value="uwu,owo,xwx",inline=True)
    embed.add_field(name='Under construction',value="gomenasai",inline=False)
    await ctx.send(embed=embed)
'''

client.run(utils.auth["token"])
