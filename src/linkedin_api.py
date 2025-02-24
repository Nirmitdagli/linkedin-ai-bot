import requests
import config

# Function to post AI-generated content to LinkedIn **Company Page**
def post_to_linkedin(content):
    # Ensure the AI-generated prompt is not uploaded
    clean_content = content.split("\n", 1)[-1].strip()

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {config.LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }

    post_data = {
        "author": f"urn:li:organization:{config.LINKEDIN_COMPANY_ID}",
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
        print("\n✅ Successfully posted to LinkedIn Company Page!\n")
    else:
        print("\n❌ Failed to post to LinkedIn:", response.text)

