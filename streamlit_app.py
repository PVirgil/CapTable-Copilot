# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# LLM Helper

def call_llm(prompt: str, model: str = "mixtral-8x7b-32768") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a startup CFO, cap table expert, and funding strategist."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Modules

def generate_captable(founders: str, investors: str, notes: str) -> str:
    prompt = (
        f"Founders: {founders}\nInvestors: {investors}\nConvertible Notes/SAFEs: {notes}\n"
        "Generate a detailed cap table including % ownership, total shares, and post-money valuation assumptions."
    )
    return call_llm(prompt)

def simulate_round(existing_captable: str, new_investment: str) -> str:
    prompt = (
        f"Existing cap table: {existing_captable}\nNew investment round: {new_investment}\n"
        "Simulate the resulting cap table, including dilution and new ownership breakdown."
    )
    return call_llm(prompt)

def explain_term_sheet(term_sheet_text: str) -> str:
    prompt = f"Explain the following term sheet in plain language: {term_sheet_text}"
    return call_llm(prompt)

def answer_investor_question(question: str, context: str) -> str:
    prompt = f"Startup context: {context}\nQuestion: {question}\nProvide a concise, strategic answer as a CFO."
    return call_llm(prompt)

# UI

def main():
    st.set_page_config("CapTable Copilot", page_icon="📈", layout="wide")
    st.title("📈 CapTable Copilot - AI CFO for Founders")
    st.write("Build, simulate, and explain startup equity like a pro.")

    st.sidebar.header("🔢 Input Data")
    founders = st.sidebar.text_area("Founders & % (e.g. Alice 60%, Bob 40%)")
    investors = st.sidebar.text_area("Investors (e.g. Angel A $250K at $5M)")
    notes = st.sidebar.text_area("SAFEs/Notes (optional)")
    captable_context = f"Founders: {founders}\nInvestors: {investors}\nNotes: {notes}"

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Generate Cap Table", "🔁 Simulate Round", "📄 Term Sheet Q&A", "💬 CFO Q&A"])

    with tab1:
        st.subheader("📊 Generate Cap Table")
        if st.button("Create Cap Table"):
            output = generate_captable(founders, investors, notes)
            st.text_area("Cap Table Output", value=output, height=400)

    with tab2:
        st.subheader("🔁 Simulate Investment Round")
        new_investment = st.text_area("Describe new investment (e.g. $2M at $10M post)")
        if st.button("Simulate Round"):
            result = simulate_round(captable_context, new_investment)
            st.text_area("Post-Round Cap Table", value=result, height=400)

    with tab3:
        st.subheader("📄 Term Sheet Explainer")
        term = st.text_area("Paste term sheet excerpt")
        if st.button("Explain Term Sheet"):
            summary = explain_term_sheet(term)
            st.text_area("Term Sheet Summary", value=summary, height=300)

    with tab4:
        st.subheader("💬 Ask a CFO")
        q = st.text_input("Investor-style question (e.g. How much dilution next round?)")
        if st.button("Answer Question"):
            answer = answer_investor_question(q, captable_context)
            st.markdown(f"**AI CFO:** {answer}")

if __name__ == "__main__":
    main()
