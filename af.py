import feedparser
import asyncio
import logging
from aiogram import Bot, Dispatcher

# تنظیمات
TOKEN = "7532649332:AAEHbIfjPuNSwD2LBFb8El29ZatTepTpzY4"  # توکن بات تلگرام
CHANNEL_ID = "@ahmadiahah"  # نام کاربری کانال
BBC_RSS_FEED = "http://feeds.bbci.co.uk/persian/rss.xml"  # لینک RSS بی‌بی‌سی فارسی
GROUP_LINK = "https://t.me/ahmadiahah"  # لینک گروه موردنظر

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# لیست اخبار قبلی برای جلوگیری از ارسال تکراری
sent_articles = set()

async def fetch_news():
    """دریافت و ارسال اخبار جدید بی‌بی‌سی فارسی"""
    feed = feedparser.parse(BBC_RSS_FEED)
    
    for entry in feed.entries:  # بررسی تمام اخبار جدید
        if entry.link not in sent_articles:
            # **ایجاد پیام با لینک گروه و کانال**
            message = (
                f"📰 {entry.title}\n"
                f"{entry.summary}\n"
                f"🔗 {entry.link}\n\n"
                f"💬 برای بحث و گفتگو به گروه بپیوندید: {GROUP_LINK}\n"
                f"📢 کانال ما را دنبال کنید: {GROUP_LINK}"
            )
            
            # **بررسی وجود تصویر در خبر**
            image_url = None
            if "media_content" in entry:  # بررسی تگ media برای تصاویر
                image_url = entry.media_content[0]["url"]
            elif "enclosures" in entry and len(entry.enclosures) > 0:  # بررسی تصاویر در enclosure
                image_url = entry.enclosures[0]["href"]

            # **ارسال خبر (با تصویر یا بدون تصویر)**
            if image_url:
                await bot.send_photo(CHANNEL_ID, photo=image_url, caption=message)
            else:
                await bot.send_message(CHANNEL_ID, message)

            # ذخیره لینک برای جلوگیری از ارسال تکراری
            sent_articles.add(entry.link)

async def news_scheduler():
    """اجرای دریافت اخبار در بازه‌های زمانی مشخص"""
    while True:
        await fetch_news()
        await asyncio.sleep(600)  # هر ۱۰ دقیقه یکبار اخبار جدید بررسی می‌شود

async def main():
    """اجرای بات"""
    asyncio.create_task(news_scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
