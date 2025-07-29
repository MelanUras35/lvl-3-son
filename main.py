import asyncio
import logging
import config
from bot import client


def start_bot():
    try:
        asyncio.run(client.start(config.TOKEN))
    except KeyboardInterrupt:
        logging.info("Bot kapatma isteği alındı. Kapatılıyor...")
    except Exception:
        logging.exception("Bot çalışırken hata oluştu:")
    finally:
        asyncio.run(client.close())
        logging.info("Bot başarıyla durduruldu.")

if __name__ == "__main__":
    start_bot()
