# LLM Agents MOOC, Fall 2024 - UC Berkeley

This repository contains three assignments from the **Large Language Model Agents MOOC, Fall 2024**, offered by UC Berkeley. The assignments focus on building and orchestrating AI agents using LLMs and the AutoGen framework.

For more information about the course, visit the official [ website](https://llmagents-learning.org/f24).

---

## Lab 01: Restaurant Review Summarizer with AutoGen Framework

This project is a Python-based application that uses **AutoGen**, a multi-agent LLM framework, to analyze restaurant reviews, summarize them, and provide a final score for the queried restaurant. The project focuses on leveraging AI models to process unstructured text data efficiently.

---

### Features

1. **Fetch Reviews:** Extract all reviews for a restaurant based on the user query.
2. **Analyze Reviews:** Evaluate food quality and customer service based on adjectives in the reviews.
3. **Score Calculation:** Generate an overall score for the restaurant by combining individual scores.

---

### How It Works

#### Workflow
The project workflow consists of three agents:
1. **Fetch Agent:** Retrieves all reviews for a queried restaurant.
2. **Analysis Agent:** Analyzes each review for adjectives that determine:
   - `food_score`: Based on adjectives like "awesome" (5/5) or "average" (3/5).
   - `customer_service_score`: Based on adjectives like "horrible" (1/5) or "satisfying" (4/5).
3. **Scoring Agent:** Uses scores from the analysis to calculate a final score for the restaurant.

#### Final Score Calculation
The final score is derived using the formula:
\[
\text{Overall Score} = \frac{10}{N \sqrt{125}} \sum_{i=1}^N \sqrt{\text{food_score}_i^2 \times \text{customer_service_score}_i}
\]
Where \(N\) is the number of reviews.

