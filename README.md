# 🔍 LLM Forensic Interview Assistant

> An AI-powered web application that assists police officers in conducting forensic interviews with children in child sexual abuse (CSA) investigations — suggesting safe, non-leading questions in real time using GPT-3.5.

---

## Overview

Forensic interviews with child witnesses are highly sensitive. Research shows that leading, suggestive, or directive questions can contaminate a child's testimony and compromise an investigation. This tool uses large language model (LLM) prompt engineering to suggest high-quality, open-ended interview questions to officers during live interviews — and automatically filters out any potentially harmful or biased questions before surfacing them.

The system was built as a capstone project exploring prompt engineering strategies for a real-world, high-stakes NLP application.

---

## How It Works

### 1. Question Generation
Given an interview history (e.g. `Q1: Tell me what happened. A1: Something bad happened in the park.`), the system generates candidate follow-up questions using one of three prompting strategies:

| Strategy | Description |
|---|---|
| **Zero-Shot** | Generates questions without domain-specific examples, generalizing from broad training |
| **In-Context Learning** | Uses real CSA interview examples to guide the model toward appropriate questioning patterns |
| **Chain-of-Thought (CoT)** | Reasons step-by-step through the child's response before generating a question — best for complex or ambiguous situations |

### 2. Automatic Question Filtering
Each generated question is automatically classified into one of 5 categories based on forensic interview research:

| Category | Safe? | Description |
|---|---|---|
| **Invitation focus** | ✅ | Open-ended, free-recall questions — most desirable |
| **Facilitator** | ✅ | Non-suggestive encouragements to continue |
| **Directive** | ⚠️ | Focuses on details already mentioned by the child |
| **Option posing** | ❌ | Introduces new details the child hasn't mentioned |
| **Suggestive utterance** | ❌ | Leads the child or implies an expected response |

The system generates 5 candidate questions, filters out `Suggestive` and `Option posing` responses, and returns the best recommendation plus alternatives. If no safe question is found, it flags the result as potentially biased.

### 3. Evaluation
A separate evaluation pipeline (`prompt_engineering_evaluation.py`) benchmarks each prompting strategy against a labeled dataset of 500 real forensic interview questions (100 per category), measuring how often generated questions fall into desirable vs. undesirable categories.

---

## Project Structure

```
LLM-Forensic-Interview-Assistant/
│
├── init1.py                              # Flask app entry point
├── openai_logic.py                       # GPT-3.5 prompt logic + filtering
├── templates/
│   └── index.html                        # Main UI
├── static/
│   ├── css/style.css                     # Styling
│   └── js/index.js                       # Frontend logic + consulting history
├── evaluation/
│   └── prompt_engineering_evaluation.py  # Offline evaluation pipeline
├── .env                                  # API key — never committed
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repo
git clone https://github.com/qiyahuang72/LLM-Forensic-Interview-Assistant.git
cd LLM-Forensic-Interview-Assistant

# Install dependencies
pip install flask openai python-dotenv pandas openpyxl
```

### Set up your API key

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### Run the app

```bash
python init1.py
```

Open your browser and go to `http://127.0.0.1:5000`

---

## Key Findings

- **Chain-of-Thought** produced the most contextually appropriate questions for complex interview situations by reasoning through the child's response before generating
- **In-Context Learning** performed well on straightforward scenarios matching the training examples
- **Zero-Shot** was the most generalizable but least domain-specific
- The automatic classifier achieved strong performance on `Directive`, `Invitation focus`, and `Facilitator` categories
- ~58% of `Suggestive utterance` questions were misclassified as `Option posing` — but since both are filtered out, this does not affect the quality of recommendations surfaced to the user

---

## Tech Stack

- **Backend:** Python, Flask
- **LLM:** OpenAI GPT-3.5-turbo
- **Frontend:** HTML, CSS, JavaScript
- **Prompt strategies:** Zero-shot, In-context learning, Chain-of-Thought
- **Evaluation:** pandas, OpenAI API

---

## Background & Motivation

This project is grounded in forensic interview research, particularly the NICHD (National Institute of Child Health and Human Development) protocol, which emphasizes open-ended questioning to preserve the integrity of children's statements. Studies show that suggestive or leading questions can significantly alter a child's recollection, making question quality critical in abuse investigations.

This tool is intended as a decision-support aid — not a replacement for trained forensic interviewers.

---

## Limitations & Future Work

- Currently uses GPT-3.5-turbo; upgrading to GPT-4 may improve question quality
- The classifier could be fine-tuned on a larger labeled dataset for better accuracy
- Session history is stored in-browser only — a database backend would enable persistent case tracking
- Multilingual support is partially implemented (prompts include translation instructions) but not fully tested

---

## Author

**Qiya Huang** — NYU  
[GitHub](https://github.com/qiyahuang72)
