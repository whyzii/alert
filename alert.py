import requests
import time

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "7858524966:AAFNvUGs5uY6Q1WBVs29OS5d0JTRLKp8V7Y"  # Replace with your BotFather token
TELEGRAM_CHAT_ID = 645203317  # Replace with your chat ID

# Function to send Telegram alerts
def send_telegram_alert(crypto, old_price, new_price, change_percent):
    message = f"""
    🚨 **Crypto Alert** 🚨
    
    {crypto} has changed significantly:
    - Previous Price: ${old_price}
    - Current Price: ${new_price}
    - Change: {change_percent:.2f}%

    📈 Stay updated with your portfolio!
    """
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.get(url, params=params)

# Crypto portfolio (modify as needed)
portfolio = {
    "XRP": "ripple",
    "XLM": "stellar",
    "XDC": "xdce-crowd-sale",
    "DOGE": "dogecoin",
    "ADA": "cardano"
}

# Store previous prices
previous_prices = {}

print("🔄 Crypto Alert System Running...")

# Infinite loop to continuously check prices
while True:
    try:
        # Fetch latest prices from CoinGecko
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(portfolio.values())}&vs_currencies=usd"
        response = requests.get(url).json()

        # Check for significant price changes
        for crypto, coin_id in portfolio.items():
            new_price = response[coin_id]["usd"]
            old_price = previous_prices.get(crypto, new_price)  # Use new price if no old price exists
            
            # Calculate percentage change
            price_change_percent = ((new_price - old_price) / old_price) * 100
            
            # If price change exceeds ±10%, send alert
            if abs(price_change_percent) >= 0.25:
                send_telegram_alert(crypto, old_price, new_price, price_change_percent)

            # Update stored price
            previous_prices[crypto] = new_price
        
        # Wait 60 seconds before checking prices again
        time.sleep(60)

    except Exception as e:
        print(f"⚠️ Error fetching prices: {e}")
        time.sleep(60)  # Wait and retry if there's an error
