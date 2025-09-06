import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv("discord.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} başarıyla giriş yaptı ve hazır!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    if "en çok kimi seviyorsun" in msg:
        await message.channel.send("Max Verstappen babam")

    await bot.process_commands(message)

# ================== Moderasyon komutları ==================

# Ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if not member:
        await ctx.send("Banlamak istediğin kişiyi etiketle: `!ban @üye sebep`")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} sunucudan banlandı. Sebep: {reason if reason else 'Belirtilmedi.'}")
    except Exception as e:
        await ctx.send(f"Ban işlemi başarısız oldu: {e}")

# Kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if not member:
        await ctx.send("Atmak istediğin kişiyi etiketle: `!kick @üye sebep`")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} sunucudan atıldı. Sebep: {reason if reason else 'Belirtilmedi.'}")
    except Exception as e:
        await ctx.send(f"Kick işlemi başarısız oldu: {e}")

# Mute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member = None, *, reason=None):
    if not member:
        await ctx.send("Mutelenecek kişiyi etiketle: `!mute @üye sebep`")
        return

    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        try:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, add_reactions=False)
        except Exception as e:
            await ctx.send(f"'Muted' rolü oluşturulamadı: {e}")
            return

    if mute_role in member.roles:
        await ctx.send(f"{member.mention} zaten muteli.")
    else:
        try:
            await member.add_roles(mute_role, reason=reason)
            await ctx.send(f"{member.mention} mutelendi. Sebep: {reason if reason else 'Belirtilmedi.'}")
        except Exception as e:
            await ctx.send(f"Mute işlemi başarısız oldu: {e}")

# Unmute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Unmute yapılacak kişiyi etiketle: `!unmute @üye`")
        return

    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        try:
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.mention} artık mute değil.")
        except Exception as e:
            await ctx.send(f"Unmute işlemi başarısız oldu: {e}")
    else:
        await ctx.send(f"{member.mention} mute'lu değil.")

# ================== Rol komutları ==================

# Rol Verme
@bot.command()
@commands.has_permissions(manage_roles=True)
async def rolver(ctx, member: discord.Member = None, role: discord.Role = None):
    if not member or not role:
        await ctx.send("Kullanım: `!rolver @kişi @rol`")
        return
    try:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} kullanıcısına {role.mention} rolü verildi.")
    except Exception as e:
        await ctx.send(f"Rol verilemedi: {e}")

# Rol Alma
@bot.command()
@commands.has_permissions(manage_roles=True)
async def rolal(ctx, member: discord.Member = None, role: discord.Role = None):
    if not member or not role:
        await ctx.send("Kullanım: `!rolal @kişi @rol`")
        return
    try:
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} kullanıcısından {role.mention} rolü alındı.")
    except Exception as e:
        await ctx.send(f"Rol alınamadı: {e}")

# --- WEB SERVER ---
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

# Botu çalıştır
bot.run(DISCORD_TOKEN)
