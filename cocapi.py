import coc
import traceback
import discord
from discord.ext import commands

with open("adatok.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]
    
coc_client = coc.login(auth[2], auth[3], key_count=5, key_names="Bot key", client=coc.EventsClient, )
clan_tag = auth[4]
  
bot = commands.Bot(command_prefix="!")
CHANNEL_ID = int(auth[1])
    
@coc_client.event
async def on_clan_member_versus_trophies_change(old_trophies, new_trophies, player):
    await bot.get_channel(CHANNEL_ID).send(
    "{0.name} játékosnak {1} értékről {2} értékre változott a versus trófeájának a száma.".format(player, old_trophies, new_trophies))
    
@bot.command()
async def szia(ctx):
    await ctx.send("Szia! Én egy BOT vagyok! Néhány parancs: !hosok [játékos tag], !ctagok [klán tag]")
    
@bot.command()
async def hosok(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    
    to_send = ""
    for hero in player.heroes:
        to_send += "{}: level {}/{}\n".format(str(hero), hero.level, hero.max_level)
    
    await ctx.send(to_send)
@bot.command()
async def tagok(ctx, c_tag=None):
    if c_tag is None:
        members = await coc_client.get_members(clan_tag)
        clan = await coc_client.get_clan(clan_tag)
        
        to_send = ""
        claninfo = "...:::[{0}]:::...\n".format(clan.name)
        await ctx.send(claninfo)
        for player in members:
                jatekos = await coc_client.get_player(player.tag)
                to_send += "{0} ({1}) | Town hall szint: {2}\n".format(player.name, player.tag, jatekos.town_hall)
        
        await ctx.send(to_send)
    else:
        members = await coc_client.get_members(c_tag)
        clan = await coc_client.get_clan(c_tag)
        
        to_send = ""
        claninfo = "...:::[{0}]:::...\n".format(clan.name)
        await ctx.send(claninfo)
        for player in members:
                jatekos = await coc_client.get_player(player.tag)
                to_send += "{0} ({1}) | Town hall szint: {2}\n".format(player.name, player.tag, jatekos.town_hall)
        
        await ctx.send(to_send)
    
coc_client.add_clan_update(
    [clan_tag], retry_interval = 60)

coc_client.start_updates()

bot.run(auth[0])