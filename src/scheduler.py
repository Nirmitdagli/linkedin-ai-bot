import schedule
import time
from ai_generator import generate_post
from linkedin_api import post_to_linkedin

def daily_post():
    topic = "Latest AI Trends"
    post_content = generate_post(topic)
    if post_content:
        post_to_linkedin(post_content)

# Schedule daily AI post generation at 9 AM
schedule.every().day.at("09:00").do(daily_post)

while True:
    schedule.run_pending()
    time.sleep(60)

