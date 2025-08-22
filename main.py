import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Model Call Function


def call_model(prompt: str, max_tokens=1200, temperature=0.7) -> str:
    """Call OpenAI API for story generation"""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",  # can upgrade to gpt-4 if available
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content


# Title Generator


def generate_title(story: str, category: str) -> str:
    """Generate an engaging title for the bedtime story"""
    title_prompt = f"""
You are a creative title generator for children's bedtime stories.
Based on the story content and category, create a short, engaging title that would appeal to kids ages 5-10.

Category: {category}
Story excerpt: {story[:500]}...

Generate ONLY a creative, fun title (3-7 words max). Make it magical and appealing for bedtime.
Examples: "The Brave Little Mouse", "Adventures in Starland", "The Magic Forest Friends"
"""
    return call_model(title_prompt, max_tokens=50, temperature=0.8)


# Judge Agent


def judge_story(story: str, user_request: str) -> str:
    """LLM judge improves/refines the story to ensure safe, fun tone for 5–10 age group"""
    judge_prompt = f"""
You are a bedtime story quality judge for children ages 5–10.
The story must be:
- Safe, gentle, imaginative, fun
- No bad words or inappropriate themes
- Structured with a clear arc (beginning, middle, end)
- Written with a warm, kind tone
- Appropriate for bedtime (soothing ending)

User request: {user_request}
Generated story draft:
---
{story}
---

Please improve and rewrite the story if needed so it fully matches these rules. 
Return ONLY the improved bedtime story text.
"""
    return call_model(judge_prompt, max_tokens=1500, temperature=0.5)


# Categorization


def categorize_request(user_request: str) -> str:
    """Simple rule-based categorizer"""
    if any(
        word in user_request.lower()
        for word in ["animal", "dog", "cat", "dragon", "unicorn"]
    ):
        return "animal adventure"
    elif any(
        word in user_request.lower() for word in ["space", "star", "moon", "planet"]
    ):
        return "space exploration"
    elif any(
        word in user_request.lower() for word in ["magic", "fairy", "wizard", "castle"]
    ):
        return "fantasy tale"
    elif any(
        word in user_request.lower()
        for word in ["friend", "family", "school", "playground"]
    ):
        return "friendship story"
    else:
        return "general bedtime"


# Storyteller Agent


def make_story_prompt(user_request: str, category: str) -> str:
    """Craft tailored prompts for better stories"""
    base_prompt = (
        f"You are a bedtime storyteller for kids ages 5–10. Category: {category}."
    )
    base_prompt += "\nMake the story very imaginative, fun, and soothing for bedtime."
    base_prompt += (
        "\nUse a beginning, middle, and end. Include gentle dialogue if helpful."
    )
    base_prompt += "\nEnd with a calming note, like falling asleep peacefully."
    base_prompt += f"\nUser request: {user_request}\nNow tell the story:"
    return base_prompt


def run_terminal():
    """Run the agent in terminal mode"""
    print("🌙 Welcome to the Bedtime Story Generator! 🌙")
    print("\nChoose an option:")
    print("1. Animal Adventure")
    print("2. Space Exploration")
    print("3. Fantasy Tale")
    print("4. Friendship Story")
    print("5. General Bedtime")
    print("6. Custom Story (write your own prompt)")

    choice = input("\nEnter your choice (1-6): ").strip()

    category_map = {
        "1": (
            "animal adventure",
            "Tell me a story about animals going on an adventure",
        ),
        "2": ("space exploration", "Tell me a story about exploring space"),
        "3": ("fantasy tale", "Tell me a story with magic and fantasy"),
        "4": ("friendship story", "Tell me a story about friendship"),
        "5": ("general bedtime", "Tell me a gentle bedtime story"),
    }

    if choice in category_map:
        category, default_prompt = category_map[choice]
        user_input = input(
            f"\nGreat choice! You can use the default or customize:\nDefault: '{default_prompt}'\nCustom prompt (press Enter for default): "
        ).strip()
        if not user_input:
            user_input = default_prompt
    elif choice == "6":
        user_input = input("\nWhat kind of story do you want to hear? ")
        category = categorize_request(user_input)
    else:
        print("Invalid choice. Using custom prompt mode.")
        user_input = input("What kind of story do you want to hear? ")
        category = categorize_request(user_input)

    prompt = make_story_prompt(user_input, category)
    draft = call_model(prompt)
    final_story = judge_story(draft, user_input)
    story_title = generate_title(final_story, category)

    print(f"\n✨ Here's your {category} story ✨\n")
    print("=" * 60)
    print(f"📖 {story_title.strip()}")
    print("=" * 60)
    print()
    print(final_story)


# Main Entry

if __name__ == "__main__":
    run_terminal()

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

I would add memory so the agent remembers past stories and tailors them over multiple sessions,
add illustrations using AI-generated images,
add a voiceover feature so the child can listen to the story,
implement a feedback loop where the child can request "shorter," "sillier," or "more magical" edits instantly,
implement input and output guardrails to ensure the story is safe and appropriate for the audience.
"""
