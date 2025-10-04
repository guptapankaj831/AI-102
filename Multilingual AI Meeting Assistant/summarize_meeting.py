"""
summarize_meeting.py
--------------------
Module 3 of Multilingual AI Meeting Assistant.
Takes transcript text and generates:
- Concise meeting summary
- Bullet-point action items

Uses Azure OpenAI GPT model.

Requirements:
    pip install langchain_openai streamlit pydantic langchain

Environment Variables:
    OPENAI_API_KEY
    OPENAI_MODEL
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()
OPENAI_MODEL = os.getenv('OPENAI_MODEL')

# ---------------- Pydantic Model ----------------
class MeetingSummary(BaseModel):
    summary: str = Field(..., description="Concise meeting summary (3-5 sentences)")
    actions: list[str] = Field(..., description="List of action items in bullet points")

# ---------------- LangChain Prompt ----------------
prompt_template = """
You are an AI meeting assistant.
Given the transcript below, generate:
1. A concise summary (3-5 sentences)
2. Action items in bullet points

Format the response as:
Summary: <summary>
Actions:
- action1
- action2
- ...

Transcript:
{transcript}
"""

chat_prompt = ChatPromptTemplate.from_template(prompt_template)

# LLM Setup
llm = ChatOpenAI(model=OPENAI_MODEL)
llm = llm.with_structured_output(MeetingSummary)

llm_chain = chat_prompt | llm

def summarize_meeting(transcript: str) -> MeetingSummary:
    """
    Summarize transcript into a concise summary and extract action items.

    Args:
        transcript (str): Full meeting transcript.

    Returns:
        MeetingSummary: Pydantic object with summary + actions
    """
    if not transcript.strip():
        return {"error": "❌ No transcript text provided."}

    return llm_chain.invoke({"transcript": transcript})

# ==============================
# STREAMLIT UI
# ==============================

def main():
    st.title('Multilingual AI Meeting Assistant')
    st.subheader('Summarize Transcript & Extract Action Items')

    transcript_input = st.text_area('Paste transcript text here:', height=200)

    if st.button('Generate Summary & Action Items'):
        with st.spinner("Processing..."):
            try:
                result = summarize_meeting(transcript_input)
                st.markdown("### 📌 Meeting Summary")
                st.info(result.summary)

                st.markdown("### ✅ Action Items")
                for action in result.actions:
                    st.success(f"- {action}")

                # Download option
                download_text = "Meeting Summary:\n" + result.summary + "\n\nAction Items:\n"
                download_text += "\n".join([f"- {a}" for a in result.actions])
                st.download_button("📥 Download Notes", download_text, file_name="meeting_summary.txt")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

if __name__ == '__main__':
    main()
