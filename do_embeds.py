import discord
import json

def do_embed(datos):
    embeds = []
    for dato in datos:
        title = dato['title']
        if 'color' in dato:
            color = dato['color']
        else:
            color = 0x000000
        if 'description' in dato:
            description = dato['description']
            embed = discord.Embed(title=title, description=description, color=color)
        else:
            embed = discord.Embed(title=title, color=color)
        if 'tumb' in dato:
            tum = dato['tumb']
            embed.set_thumbnail(url=tum)
        if 'footer' in dato:
            footer = dato['footer']
            embed.set_footer(text=footer)
        if 'fields' in dato:
            for field in dato['fields']:
                name = field[0]
                value = field[1]
                try:
                    inline = field[2]
                except:
                    inline = True
                embed.add_field(name=name, value=value, inline=inline)
        
        if 'image' in dato:
            img = dato['image']
            embed.set_image(url=img)
        embeds.append(embed)
    return embeds
