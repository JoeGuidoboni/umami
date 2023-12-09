import discord
import openai
import re
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['u', 'U'], intents=intents)
openai.api_key = open('discord/openai_token.txt', 'r').read()
model_engine = "gpt-3.5-turbo"


message_limit = 10
messages = [
    {"role": "system", "content": "I want you to act as a sarcastic discord bot. You will give sarcastic answers as well as snarky reponses. You can respond to messages with a sassy response. When confronted about being sarcastic you will make a joke about it. You can engage in banter. You will have really clever comebacks when someone tries to roast you. You can even come across as flirty. You will be sarcastic in every response."}
]


@bot.event
async def on_ready():
    try:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you while you sleep'))
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command{'s' if len(synced) != 1 else ''}")  
    except Exception as e:
        print(e)

@bot.tree.command(name="create_react_message")
@app_commands.describe(emoji = "react emoji", role = "role") 
async def add_role(interaction: discord.Interaction, emoji: str, role: discord.Role):
    try:
        await interaction.response.send_message(emoji + " " + role.name)
    except Exception as e:
        print(e)

@bot.tree.command(name="add_role")
@app_commands.describe(emoji = "react emoji", role = "role") 
async def add_role(interaction: discord.Interaction, emoji: str, role: discord.Role):
    try:
        await interaction.response.send_message(emoji + " " + role.name)
    except Exception as e:
        print(e)


@bot.tree.command(name="remove_role")
@app_commands.describe(emoji = "react emoji", role = "role") 
async def remove_role(interaction: discord.Interaction, emoji: str, role: discord.Role):
    try:
        await interaction.response.send_message(emoji + " " + role.name)
    except Exception as e:
        print(e)



@bot.command(name="mami")
async def chat_gpt(ctx, *args):
    try:
        args = [re.sub('[^A-Za-z0-9\\!\\?\\"]+', '', arg) for arg in args]
        content = ' '.join(args)

        messages.append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )

        chat_response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": chat_response})
        if len(messages) > message_limit:
            messages.pop(1)
        await ctx.channel.send(chat_response)
    except Exception as e:
        print(e)
        await ctx.channel.send("Something went wrong when trying that command, try wording it a different way")
    # print(messages[:])


token = open('discord/bot_token.txt', 'r').read()
bot.run(token)
