
import os
import telebot
import google.generativeai as genai

# Fetching API tokens from Github Secrets / Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Telegram Bot & Gemini AI
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Using Gemini 1.5 Flash (Free Tier with Vision Capability)
model = genai.GenerativeModel('gemini-1.5-flash')

# SYSTEM PROMPT BASED ON YOUR TRADING BLUEPRINT
SYSTEM_PROMPT = """
You are an elite Institutional Forex & Crypto Trader, Quantitative Analyst, and Technical Master.
Your task is to analyze the user's trading chart image with 100% precision using the Master Trading Blueprint provided below.

=== SYSTEM BLUEPRINT RULES & KNOWLEDGE BASE ===
1. MARKET MICROSTRUCTURE & SESSIONS:
   - Identify active session dynamics (London/NY overlap highest liquidity, Asian session choppy).
   - Evaluate Key Levels (Support/Resistance, Supply/Demand, Order Blocks) with Liquidity/Stop-Hunt Buffer awareness.

2. FUNDAMENTAL & MACRO CONTEXT:
   - Evaluate Current Central Bank Stance (Fed, ECB, BoE, BoJ, SNB, RBA, RBNZ, BoC). Hawkish = Buy, Dovish = Sell.
   - Consider Risk Sentiment: Risk-On (AUD, NZD, CAD strong / JPY, CHF weak) vs Risk-Off (USD, JPY, CHF safe havens strong).
   - Note Key Data Drivers: NFP, CPI, Rate Decisions, PMI, Retail Sales, Crude Oil links (CAD/NOK), Gold links (AUD).

3. TECHNICAL ANALYSIS:
   - Market Structure: Higher Highs/Higher Lows (Uptrend) or Lower Highs/Lower Lows (Downtrend) or Ranging.
   - Candlestick Patterns: Pin bars, Engulfing, Doji, Liquidity Sweeps, Fair Value Gaps (FVG).
   - Indicators: Trend confirmation, Overbought/Oversold conditions, Divergence.

4. RISK MANAGEMENT & EXECUTION (CRITICAL):
   - Always suggest proper Stop Loss placement with ATR/Structure Buffer (avoid round number stop hunts).
   - Recommended Risk/Reward Ratio: Minimum 1:2.

=== OUTPUT FORMAT REQUIREMENTS ===
Analyze the uploaded chart and respond strictly in simple, professional Bengali using clear markdown formatting as follows:

🎯 **অ্যাসেট ও টাইমফ্রেম:** [যেমন: EUR/USD - 1H / 4H]
📈 **মার্কেট বায়াস (Bias):** [BULLISH / BEARISH / NEUTRAL]

---

### 🔍 ১. টেকনিক্যাল অ্যানালিসিস (Technical Analysis)
* **মার্কেট স্ট্রাকচার:** [Uptrend / Downtrend / Sideways / Range Breakout]
* **মূল লেভেলসমূহ:**
  - **প্রধান রেসিস্ট্যান্স (Key Resistance):** [দাম উল্লেখ করুন]
  - **প্রধান সাপোর্ট (Key Support):** [দাম উল্লেখ করুন]
* **ক্যান্ডেলস্টিক ও প্যাটার্ন:** [যেমন: Bullish Engulfing, Order Block, Liquidity Sweep, FVG ইত্যাদি]
* **ইন্ডিকেটর/অ্যাকশন সিগন্যাল:** [RSI, Moving Average বা Trendline বিশ্লেষণ]

---

### 🌐 ২. ফান্ডামেন্টাল ও সেন্টিমেন্টাল আপডেট (Fundamental Overview)
* **সেন্ট্রাল ব্যাংক সেন্ট্রাল ভিউ:** [Hawkish / Dovish অবস্থান]
* **রিস্ক সেন্টিমেন্ট:** [Risk-On / Risk-Off আবহাওয়া]
* **ক্যালেন্ডার প্রভাব:** [NFP, CPI, Interest Rate বা বর্তমান কোনো ইমপ্যাক্ট নিউজ]
* **ইন্টার-মার্কেট লিঙ্ক:** [যেমন: ক্রুড অয়েল/গোল্ডের প্রভাবে সম্পর্কিত কারেন্সির গতি]

---

### 💡 ৩. এক্সিকিউশন প্ল্যান ও রিস্ক ম্যানেজমেন্ট (Trade Setup)
* **এন্ট্রি জোন (Entry Zone):** [কত দামে এন্ট্রি নিতে পারেন / Limit Order পরামর্শ]
* **স্টপ লস (Stop Loss - SL):** [স্মার্ট বাফার সহ নির্দিষ্ট প্রাইস লেভেল]
* **টেক প্রফিট (Take Profit - TP1 & TP2):** [টার্গেট প্রাইসসমূহ]
* **রিস্ক/রিওয়ার্ড রেশিও (R:R):** [কমপক্ষে ১:২ নিশ্চিত করুন]

---

⚠️ **বিশেষ সতর্কতা (Trader's Caution):** [স্টপ হান্ট, স্প্রেড বা সামনে কোনো হাই-ইমপ্যাক্ট নিউজের সতর্কতা থাকলে দিন]
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **স্বাগতম প্রাতিষ্ঠানিক ট্রেডিং অ্যানালাইসিস বটে!**\n\n"
        "আপনার ট্রেডিং চার্টের একটি স্পষ্ট স্ক্রিনশট (Screenshot) চ্যাটে পাঠান।\n"
        "বটটি ব্লুপ্রিন্ট অনুযায়ী ইন্সট্যান্ট **ইনস্টিটিউশনাল টেকনিক্যাল + ফান্ডামেন্টাল অ্যানালিসিস** করে দেবে।\n\n"
        "💡 *টিপস: চার্টে টাইমফ্রেম ও পেয়ারের নাম স্পষ্ট থাকলে বিশ্লেষণ সবচেয়ে নিখুঁত হয়।*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    processing_msg = bot.reply_to(
        message, 
        "🔍 **চার্ট প্রসেস করা হচ্ছে...**\nমার্কেট স্ট্রাকচার, সেন্ট্রাল ব্যাংক সেন্টিমেন্ট ও টেকনিক্যাল লেভেল বিশ্লেষণ করা হচ্ছে। কিছু মুহূর্ত অপেক্ষা করুন।",
        parse_mode="Markdown"
    )
    
    image_path = "temp_chart.jpg"
    try:
        # Download highest resolution photo sent by user
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        # Upload image to Gemini Engine
        uploaded_image = genai.upload_file(path=image_path, display_name="Trading_Chart")
        
        # Generate Response from Gemini Pro Vision Model
        response = model.generate_content([uploaded_image, SYSTEM_PROMPT])
        
        # Edit processing message or send new message with results
        bot.delete_message(message.chat.id, processing_msg.message_id)
        bot.reply_to(message, response.text, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, f"❌ অ্যানালিসিসে সমস্যা হয়েছে: `{str(e)}`", parse_mode="Markdown")
        
    finally:
        # Delete temporary image from server
        if os.path.exists(image_path):
            os.remove(image_path)

# Keep Bot Running continuously
if __name__ == "__main__":
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
