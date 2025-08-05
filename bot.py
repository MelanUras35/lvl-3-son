port discord
import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


stok_adet = {
    "Kalem": 50,
    "Defter": 120,
    "Silgi": 75,
    "Kalemtıraş": 30,
    "Cetvel": 40,
    "Boya Kalemi": 200,
    "Makas": 25,
    "Zımba": 15,
    "Klasör": 60,
    "Post-it Not": 90,
    "Marker": 45,
    "Tükenmez Kalem": 80,
}


@client.event
async def on_ready():
    logging.info(f"Bot çevrimiçi: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.strip()
    lower = text.lower()

    # ping-pong
    if lower == "!ping":
        await message.channel.send("pong")
        return

    # !stokdurumu komutu ve alias olarak !faq stok durumu / !faq stokdurumu
    if lower in ("!stokdurumu", "!faq stok durumu", "!faq stokdurumu"):
        mesaj = "🔍 **Stok Durumu** 🔍\n" + "\n".join(
            f"- **{urun}**: {adet} adet stokta"
            for urun, adet in stok_adet.items()
        )
        await message.channel.send(mesaj)
        return

    # !faq komutu (diğer SSS komutları)
    if lower.startswith("!faq "):
        key = text[5:].lower()
        cevap = config.faqs.get(key)
        await message.channel.send(cevap or "Üzgünüm, bu soru SSS'de bulunamadı.")
        return

    # !destek komutu
    if lower.startswith("!destek "):
        parts = text.split(" ", 2)
        if len(parts) < 3:
            await message.channel.send("Kullanım: !destek <departman> <soru>")
            return

        bolum, soru = parts[1].lower(), parts[2]
        if bolum not in config.departmanlar:
            await message.channel.send(
                f"Böyle bir bölüm yok.\n"
                f"Destek alabileceğiniz bölümler: {', '.join(config.departmanlar)}"
            )
            return

        await message.channel.send(f"Sorunuz '{bolum}' departmanına iletildi!\n>Soru: {soru}")
        return

    # !sorular komutu
    if lower == "!sorular":
        for i, soru in enumerate(config.faqs.keys(), start=1):
            await message.channel.send(f"{i}. {soru}")
        return

    # geçersiz komut
    if text.startswith("!"):
        await message.channel.send(
            "Geçersiz komut. Kullanabileceğin komutlar:\n"
            "`!ping`, `!stokdurumu`, `!faq <soru>`, `!destek <departman> <soru>`, `!sorular`"
        )
        return

if __name__ == "__main__":
    client.run(config.TOKEN)
