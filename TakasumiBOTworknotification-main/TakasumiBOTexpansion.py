import discord
import asyncio
from dotenv import load_dotenv
import os
from discord import app_commands
import requests, json
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
    while True:
        await asyncio.sleep(60)
        with open("data.json", "r") as f:
            user_notifications = json.loads(f.read())
        
        for _ in user_notifications.keys():
            # んーーーーーーーーーーーーーーーーーーーーーーー
            # わかんねーーーーーーーーー
            pass
        
        with open("data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(user_notifications))


with open("data.json", "r") as f:
    user_notifications = json.loads(f.read()) #通知を受け取るユーザーのIDを格納する辞書

class button(discord.ui.View):
    def __init__(self, user_id, timeout=180):
        super().__init__(timeout=timeout)
        self.user_id = user_id

    @discord.ui.button(label="cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_notifications[self.user_id] = False #通知を受け取るユーザーから削除
        await interaction.response.send_message("通知をキャンセルしました", ephemeral=True)


@client.event
async def on_message(message: discord.Message):
    if message.author.id == 981314695543783484 and len(message.embeds) == 1 and "コイン手に入れました" in message.embeds[0].author.name:
        worknotification1 = discord.Embed(title="TakasumiBOT work通知", description="workを受信しました。\n20分後に通知します。", color=discord.Color.brand_green())
        await message.reply(embed=worknotification1)
        
        datetime = datetime.datetime
        
        user_notifications[message.author.id] = {
            "notify": True,
            "time": (datetime.datetime.now() + datetime.timedelta(minutes=20)).timestamp()
        }
        with open("data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(user_notifications))
        
        await asyncio.sleep(20 * 60)  # 20 minutes

        with open("data.json", "r") as f:
            user_notifications = json.loads(f.read())

        if user_notifications.get(message.author.id, {}).get("notify", True):
            worknotification2 = discord.Embed(title="TakasumiBOT work通知", description="workの時間です\n</work:1132868147519692871> でお金を得ましょう", color=discord.Color.brand_green())
            await message.channel.send(message.author.mention, embed=worknotification2, view=button(user_id=message.author.id))
            user_notifications[message.author.id]["notify"] = True #通知を受け取るユーザーに追加


@tree.command(name="help",description="botのヘルプを表示します")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Takasumi Work Notification", description="このBOTの使い方を確認しよう！", color=discord.Color.brand_green())
    embed.add_field(name="help", value="このヘルプコマンドを表示", inline=False)
    embed.add_field(name="work", value="workの時間を通知します", inline=False)
    embed.add_field(name="status", value="botのステータスを表示", inline=False)
    embed.add_field(name="guessinfo", value="guess時の勝ち負けの金額を表示します", inline=False)
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
    

@tree.command(name="guessinfo",description="guess時の勝ち負けの金額を表示します")
@discord.app_commands.describe(amount="賭ける金額を入力")
async def guessinfo_command(interaction: discord.Interaction, amount:int=100):
    req = requests.get("https://api.takasumibot.com/v1/money.php")
    moneydata = json.loads(req.content)
    for _ in moneydata["data"]:
        if _["id"] == interaction.user.id:
            #money = _["amount"]
            break
    # ↑で動くかどうか微妙


    #計算
    win_result = math.floor(amount * 2.8)
    lose_result = math.floor(amount * 1.5)
    #埋め込みの作成
    result_embed = discord.Embed(title="結果", color=discord.Color.blue())
    result_embed.add_field(name="入力金額", value=f"{amount}", inline=False)
    result_embed.add_field(name="勝った場合", value=f"最終金額: {win_result}", inline=False)
    result_embed.add_field(name="負けた場合", value=f"最終金額: {lose_result}", inline=False)
    #結果を送信
    await interaction.response.send_message(embed=result_embed)

client.run(TOKEN)
