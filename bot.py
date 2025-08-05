import discord
import config       
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f"Bot çevrimiçi: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    text = message.content.strip()

    
    if text == "!ping":
        await message.channel.send("pong")
        return

    # !faq komutu
    if text.startswith("!faq "):
        key = text[5:].lower()
        cevap = config.faqs.get(key)
        await message.channel.send(cevap or "Üzgünüm, bu soru SSS'de bulunamadı.")
        return

    
    if text.startswith("!destek "):
        parts = text.split(" ", 2)
        if len(parts) < 3:
            await message.channel.send("Kullanım: !destek <bölüm> <sorunuz>")
            return
        bolum, soru = parts[1].lower(), parts[2]
        if bolum not in config.departmanlar:
            await message.channel.send(
                f"Böyle bir bölüm yok. Destek alabileceğiniz bölümler: {', '.join(config.departmanlar)}"
            )
            return
        await message.channel.send(f"Sorunuz '{bolum}' departmanına iletildi!\n>Soru: {soru}")
        return

    # !sorular komutu
    if text == "!sorular":
        for i, soru in enumerate(config.faqs.keys(), start=1):
            await message.channel.send(f"{i}. {soru}")
        return

    
    if text.startswith("!"):
        await message.channel.send("Geçersiz komut. !faq, !destek veya !sorular kullanın.")
