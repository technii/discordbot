import discord
import json
import yt_dlp
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import asyncio
import os
import io
import datetime
from PIL import Image
import PIL
import requests
jsonfile = open("token.json")
jsondict = json.load(jsonfile)




class sclient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)
    async def setup_hook(self) -> None:
        await self.tree.sync()
        print(f"we have signed in as {client.user}")
        os.mkdir("images")
        os.mkdir("sounds")

client = sclient()



    


@client.tree.command(name="uploadsound", description="...")
async def _uploadsound(interaction: discord.Interaction, sound: discord.Attachment) -> None:
    print(sound.content_type)
    if sound.content_type == "audio/mpeg":
        print("true")
    else:
        print("False")
    
@client.tree.command(name="imagetogif", description="Make a image to a gif")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def _imagetogif(interaction: discord.Interaction, image: discord.Attachment ):
    try:    
        await image.save(f"images/{image.filename}")
        if image.content_type == "image/png" or "image/webp" or "image/apng" or"image/avif" or "image/bmp" or"image/jpeg" or"image/tiff":
            convertimage = Image.open(f"images/{image.filename}")
            exportfilenames = str.split(image.filename, ".", 1)
            exportfilename = f"images/{exportfilenames[0]}.gif"
            convertimage.save(exportfilename)
            attachedfile = discord.File(exportfilename)
            await interaction.response.send_message("Converted to gif :)", file=attachedfile)
            convertimage.close()
            attachedfile.close()
            os.remove(f"images/{image.filename}")
            print(exportfilename)
            os.remove(exportfilename)
        else:
           await interaction.response.send_message("Not a Image")
    except Exception as e:
        await interaction.response.send_message(e)


## reply to a message with an attachment and convert it to a gif
@client.tree.command(name="attachmenttogif", description="Make a image to a gif")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def _attachmenttogif(interaction: discord.Interaction, imagelink: str ):
    try:
        imagepath = await linktoimage(imagelink)
        giffilepath = await imagetogif(imagepath)
        await interaction.response.send_message("Converted to gif :]", file=discord.File(giffilepath))
        os.remove(giffilepath)
    except Exception as e:
        await interaction.response.send_message(e)

# send link and get gif back using Requests
async def linktoimage(link : str):
    query_params = {"downloadformat": "png"}
    response = requests.get(link,params=query_params)
    filename = str(await getfilename(link))
    with open(filename,mode="wb") as file:
        file.write(response.content)
    return filename

#shockingly makes a image a gif using PIL

async def imagetogif(imagepath : str):
    imagename = str.split(imagepath, "/")
    exportfilenames = str.split(imagename[1], ".", 1)
    exportfilename = f"images/{exportfilenames[0]}.gif"
    os.rename(imagepath,exportfilename)
    return exportfilename

# splits the inputted link down into the file name contained in the url for the link to image function
async def getfilename(link : str):
    linkparts1 = link.split("/")
    linkparts2 = linkparts1[-1].split("?")
    name = f"images/{linkparts2[0]}"
    return name


client.run(jsondict.get("token"))
