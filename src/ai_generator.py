import torch
from transformers import pipeline
import config

# Check if GPU is available
def get_device():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🔹 Using Device: {device}\n")  # Debugging
    return device

# Load AI text generation model
print("\n🔹 Loading AI Model...\n")  # Debugging
try:
    generator = pipeline(
        "text-generation",
        model=config.HUGGINGFACE_MODEL,
        device=0 if get_device() == "cuda" else -1,
    )
    print("\n✅ Model Loaded Successfully!\n")  # Debugging
except Exception as e:
    print(f"\n🚨 Model Loading Error: {e}\n")
    exit(1)  # Stop execution if model fails to load

# Function to generate AI text
def generate_post(topic, min_lines=15, max_length=250):
    print(f"\n🔹 Generating AI Content for topic: {topic}...\n")

    # Improved prompt for structured LinkedIn posts
    prompt = (
        f"Write a professional, engaging LinkedIn post about {topic}. "
        f"The post must be at least {min_lines} lines long, structured with short paragraphs, "
        f"and include key industry insights. Use a professional yet engaging tone. "
        f"Add relevant hashtags like #AI #Tech #Innovation."
    )

    try:
        result = generator(prompt, max_length=max_length, truncation=True, num_return_sequences=1, pad_token_id=50256)
        ai_post = result[0]["generated_text"].strip()

        # Ensure the post has at least `min_lines`
        while ai_post.count("\n") < min_lines - 1:
            print("\n🔹 Regenerating AI content (was too short)...\n")
            result = generator(prompt, max_length=max_length + 50, truncation=True, num_return_sequences=1, pad_token_id=50256)
            ai_post = result[0]["generated_text"].strip()

        print("\n✅ Generated AI Post:\n", ai_post)
        return ai_post

    except Exception as e:
        print(f"\n🚨 Error Generating AI Content: {e}")
        return None

# Run AI post generation
if __name__ == "__main__":
    topic = "AI trends"
    ai_text = generate_post(topic)

    if ai_text:
        print("\n✅ AI Text Generated Successfully!")
    else:
        print("\n❌ AI Failed to Generate Content.")

