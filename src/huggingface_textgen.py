import os
import torch
import requests
from transformers import pipeline

# LinkedIn API Credentials
ACCESS_TOKEN = "AQVBBQx6k-qLQAGiihmfyjmwXK1WwW0lKuslwdOBymQmzDU6Zjv-O-uzFEqOv802-fFEFa4LusEDuf4MMWo0ii-ndmK25RcEQ8bebqXdaMa5HYv2-TRluZOdxujZO0aNrifrmDMFIrIYt_zI9wLV3kkcPtu6UQsdzJUG08h-QAZRNW59eqq2XwGQBNWM-EkfLgjPmj89pajTCYfIdXOJVXOLOuhnRgZJQRIz_G22LfJjpKbaJNr6wQFr1W-W43r0OOlT77XAZAJks7JH2cS-c_RXs8Lycj0fAynNdkmA88Dc-5HFF0RbDKixUeTXhlchYOzUoHnT05oygHoxg4RLWIgI6IHq2g"
COMPANY_ID = "106167425"  # Use the correct ID

# Function to check if GPU is available
def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

# Choose an optimized model
MODEL_NAME = "EleutherAI/gpt-neo-1.3B"

# Initialize AI text generation model
generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=0 if get_device() == "cuda" else -1,
)

# Function to generate AI text
def generate_text(topic, min_lines=15, max_length=250):
    try:
        print("\nGenerating AI Content... Please wait.\n")

        # Improved prompt for structured LinkedIn posts
        prompt = (
            f"Write a professional, engaging LinkedIn post about {topic}. "
            f"The post must be at least {min_lines} lines long, structured with short paragraphs, "
            f"and include key industry insights. Use a professional yet engaging tone. "
            f"Add relevant hashtags like #AI #Tech #Innovation."
        )

        # Generate AI content
        result = generator(
            prompt,
            max_length=max_length,
            truncation=True,
            num_return_sequences=1,
            pad_token_id=50256,
        )

        ai_post = result[0]["generated_text"].strip()

        # Ensure the post has at least `min_lines`
        while ai_post.count("\n") < min_lines - 1:
            result = generator(
                prompt,
                max_length=max_length + 50,
                truncation=True,
                num_return_sequences=1,
                pad_token_id=50256,
            )
            ai_post = result[0]["generated_text"].strip()

        print("\nGenerated AI Post:\n", ai_post)
        return ai_post

    except torch.cuda.OutOfMemoryError:
        print("\n🚨 Out of Memory Error: Try using a smaller model.\n")
        return None
    except Exception as e:
        print(f"\n🚨 Error: {e}")
        return None

# Function to post AI-generated content to LinkedIn **Company Page**
def post_to_linkedin(content):
    # Remove the AI-generated prompt before posting
    clean_content = content.split("\n", 1)[-1].strip()

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }

    post_data = {
        "author": f"urn:li:organization:{COMPANY_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": clean_content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(url, headers=headers, json=post_data)

    if response.status_code == 201:
        print("\n✅ Successfully posted to the LinkedIn Company Page!\n")
        return response.json()
    else:
        print("\n❌ Failed to post to LinkedIn:", response.text)
        return None

# Run AI post generation and publish it on LinkedIn
if __name__ == "__main__":
    topic = "OS trends"
    ai_text = generate_text(topic, min_lines=15, max_length=250)

    if ai_text:
        print("\nPosting to LinkedIn Company Page...\n")
        post_to_linkedin(ai_text)

