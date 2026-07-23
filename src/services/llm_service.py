import os
import json

from dotenv import load_dotenv
from openai import OpenAI


class LLMService:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("OPENROUTER_API_KEY")

        self.client = None

        if api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )

    def analyze_text(self, text):

        prompt = f"""
You are an expert Customer Success Manager.

Analyze the customer note.

Return ONLY valid JSON.

Format:

{{
    "overall_sentiment": "",
    "budget_issue": false,
    "competitor": "",
    "migration_issue": false,
    "executive_involved": false,
    "renewal_risk_reason": ""
}}

Customer Note:

{text}
"""

        if self.client is None:
            lower_text = text.lower()

            budget_issue = any(
                token in lower_text
                for token in ["budget cut", "budget", "cost reduction", "cost", "renewal freeze"]
            )

            migration_issue = any(
                token in lower_text
                for token in ["migration", "migrate", "v3", "sunset", "deprecated"]
            )

            executive_involved = any(
                token in lower_text
                for token in ["cto", "vp", "executive", "leadership", "cfo", "ceo"]
            )

            competitor = ""
            for candidate in ["hygraph", "strapi", "sanity", "contentful", "craftcms", "wordpress"]:
                if candidate in lower_text:
                    competitor = candidate.title()
                    break

            negative_sentiment = any(
                token in lower_text
                for token in ["frustrated", "tense", "downgrade", "failed", "no show", "cut", "concern", "evaluate", "explore options"]
            )

            sentiment = "Negative" if negative_sentiment else "Neutral"

            reason_parts = []
            if budget_issue:
                reason_parts.append("budget constraints were mentioned")
            if migration_issue:
                reason_parts.append("migration pressure was raised")
            if executive_involved:
                reason_parts.append("executive interest or escalation was noted")
            if competitor:
                reason_parts.append(f"there is active competitor evaluation against {competitor}")

            return {
                "overall_sentiment": sentiment,
                "budget_issue": budget_issue,
                "competitor": competitor,
                "migration_issue": migration_issue,
                "executive_involved": executive_involved,
                "renewal_risk_reason": "; ".join(reason_parts) if reason_parts else "Text was analyzed with heuristic fallback logic."
            }

        try:

            response = self.client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct",
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            output = response.choices[0].message.content.strip()

            output = output.replace("```json", "")
            output = output.replace("```", "")

            return json.loads(output)

        except Exception as e:

            return {
                "overall_sentiment": "Unknown",
                "budget_issue": False,
                "competitor": "",
                "migration_issue": False,
                "executive_involved": False,
                "renewal_risk_reason": f"LLM Error: {str(e)}"
            }