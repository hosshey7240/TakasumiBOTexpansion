import discord
import asyncio
from dotenv import load_dotenv
import os
from discord import app_commands
import asyncio
import shutil, psutil
import math


load_dotenv(verbose=True)
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()
    await client.change_presence(activity=discord.Game(name="TakasumiBOT work通知")) #をプレイ

@tree.command(name="help",description="botのヘルプを表示します")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Takasumi Work Notification", description="このBOTの使い方を確認しよう！", color=discord.Color.brand_green())
    embed.add_field(name="help", value="このヘルプコマンドを表示", inline=False)
    embed.add_field(name="work通知", value="workの時間を通知します", inline=False)
    embed.add_field(name="status", value="botのステータスを表示", inline=False)
    embed.add_field(name="guess get money", value="入力された金額においてguess時の勝ち負けの金額を表示します", inline=False)
    await interaction.response.send_message(embed=embed)    

@tree.command(name="status",description="BOTのステータスを表示します")
async def status(interaction: discord.Interaction):
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = shutil.disk_usage("/")
    disk_usage_percent = (disk_usage.used / disk_usage.total) * 100
    latency = client.latency * 1000    
    embed = discord.Embed(title="BOTのステータス", description="✅️ 正常に動作しています", color=discord.Color.blue())
    embed.add_field(name="CPU", inline=True, value=f"{cpu_usage}%")
    embed.add_field(name="RAM", inline=True, value=f"{ram_usage}%")
    embed.add_field(name="DISK", inline=True, value=f"{disk_usage_percent:.1f}%")
    embed.set_footer(text=f"TakasumiBOT work Notification | Ping: {latency:.2f}ms")
    await interaction.response.send_message(embed=embed)

@tree.command(name="roll simulation")   

@tree.command(name="guessinfo",description="guess時の勝ち負けの金額を表示します")
@discord.app_commands.describe(amount="賭ける金額を入力")
@discord.app_commands.choices(option=[
    discord.app_commands.Choice(name="手に入れる金額を表示", value="手に入れる金額を表示"),
    discord.app_commands.Choice(name="減らす最大金額をきめてguessの結果を表示", value="減らす最大金額をきめてguessの結果を表示")
])
async def guessinfo(interaction: discord.Interaction,amount:int, option: str):
    if option == "手に入れる金額を表示":
         #計算
         win_result = math.floor(amount * 2.8)
         lose_result = math.floor(amount * 1.5)
         #埋め込みの作成
         get_money_embed = discord.Embed(title="結果", color=discord.Color.blue())
         get_money_embed.add_field(name="入力金額", value=f"{amount}", inline=False)
         get_money_embed.add_field(name="勝った場合", value=f"最終金額: {win_result}", inline=False)
         get_money_embed.add_field(name="負けた場合", value=f"最終金額: {lose_result}", inline=False)
         #送信
         await interaction.response.send_message(embed=get_money_embed)
    elif option == "減らす最大金額をきめてguessの結果を表示":
         #計算
         useable_money= math.floor(amount//1.5)
         win_result_for_using_money = math.floor(useable_money*2.8)
         usable_money_embed = discord.Embed(title="結果",color=discord.Color.blue())
         usable_money_embed.add_field(name="買った場合",value=f"手に入れられる金額:{win_result_for_using_money}",inline=False)
         usable_money_embed.add_field(name="掛けられるコイン数",value=f"{useable_money}",inline=False)
        #送信
         await interaction.response.send_message(embed=usable_money_embed)
