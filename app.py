import streamlit as st
from main import (
    categorize_request,
    make_story_prompt,
    call_model,
    judge_story,
    generate_title,
)

st.set_page_config(page_title="🌙 Bedtime Story Generator", page_icon="✨")


def run_ui():
    st.title("🌙 Bedtime Story Generator (Ages 5–10)")
    st.write(
        "Choose a story category or write your own custom prompt for a cozy bedtime adventure!"
    )

    # Category selection
    story_mode = st.radio(
        "📚 How would you like to create your story?",
        ["Choose from categories", "Write custom prompt"],
        horizontal=True,
    )

    if story_mode == "Choose from categories":
        category = st.selectbox(
            "🎭 Pick a story category:",
            [
                "Animal Adventure",
                "Space Exploration",
                "Fantasy Tale",
                "Friendship Story",
                "General Bedtime",
            ],
        )

        category_prompts = {
            "Animal Adventure": "Tell me a story about animals going on an adventure",
            "Space Exploration": "Tell me a story about exploring space",
            "Fantasy Tale": "Tell me a story with magic and fantasy",
            "Friendship Story": "Tell me a story about friendship",
            "General Bedtime": "Tell me a gentle bedtime story",
        }

        default_prompt = category_prompts[category]
        user_input = st.text_area(
            f"💭 Customize your {category.lower()} (or use default):",
            value=default_prompt,
            height=80,
        )

    else:
        user_input = st.text_area(
            "💭 What kind of story do you want?",
            placeholder="e.g., A story about a brave little mouse who learns to swim...",
            height=100,
        )

    generate_button = st.button("✨ Generate Story")

    if generate_button and user_input.strip():
        with st.spinner("✨ Spinning a bedtime tale..."):
            try:
                # Use the functions from main1.py
                if story_mode == "Choose from categories":
                    # Map UI categories to internal categories
                    category_mapping = {
                        "Animal Adventure": "animal adventure",
                        "Space Exploration": "space exploration",
                        "Fantasy Tale": "fantasy tale",
                        "Friendship Story": "friendship story",
                        "General Bedtime": "general bedtime",
                    }
                    detected_category = category_mapping.get(
                        category, "general bedtime"
                    )
                else:
                    detected_category = categorize_request(user_input)

                prompt = make_story_prompt(user_input, detected_category)
                draft = call_model(prompt)
                final_story = judge_story(draft, user_input)
                story_title = generate_title(final_story, detected_category)

                st.success("✅ Story generated successfully!")
                st.subheader(f"📖 {story_title.strip()}")
                st.write(final_story)

                st.subheader("📊 Story Details")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"📖 **Title:** {story_title.strip()}")
                with col2:
                    st.info(f"🎭 **Category:** {detected_category.title()}")
                with col3:
                    st.info(f"📝 **Words:** ~{len(final_story.split())} words")

            except Exception as e:
                st.error(f"❌ Error generating story: {str(e)}")
                st.info("Make sure your environment is properly configured.")


if __name__ == "__main__":
    run_ui()
