import re
import pandas as pd

from src.services.llm_service import LLMService


class LLMAnalyzer:

    def __init__(self):

        self.llm = LLMService()

    def analyze_notes(self, notes_text):

        results = []

        chunks = notes_text.split("---")

        for chunk in chunks:

            chunk = chunk.strip()

            if len(chunk) < 20:
                continue

            # =====================================================
            # ACCOUNT ID
            # =====================================================

            account_id = None

            match = re.search(r"\b(10\d{2}|11[01]\d|1119)\b", chunk)

            if match:
                account_id = int(match.group())
            else:
                continue

            # =====================================================
            # LLM ANALYSIS
            # =====================================================

            try:

                analysis = self.llm.analyze_text(chunk)

            except Exception as e:

                analysis = {
                    "overall_sentiment": "Unknown",
                    "budget_issue": False,
                    "competitor": "",
                    "migration_issue": False,
                    "executive_involved": False,
                    "renewal_risk_reason": str(e)
                }

            sentiment = analysis.get(
                "overall_sentiment",
                "Unknown"
            )

            budget_issue = analysis.get(
                "budget_issue",
                False
            )

            competitor = analysis.get(
                "competitor",
                ""
            )

            migration_issue = analysis.get(
                "migration_issue",
                False
            )

            executive = analysis.get(
                "executive_involved",
                False
            )

            summary = analysis.get(
                "renewal_risk_reason",
                ""
            )

            # =====================================================
            # AI RISK SCORE
            # =====================================================

            ai_score = 0

            if str(sentiment).lower() == "negative":
                ai_score += 25

            elif str(sentiment).lower() == "neutral":
                ai_score += 10

            if budget_issue:
                ai_score += 20

            if migration_issue:
                ai_score += 15

            if executive:
                ai_score += 10

            if competitor != "":
                ai_score += 20

            if ai_score > 100:
                ai_score = 100

            # =====================================================
            # AI RISK LEVEL
            # =====================================================

            if ai_score >= 60:
                ai_level = "High"

            elif ai_score >= 30:
                ai_level = "Medium"

            else:
                ai_level = "Low"

            # =====================================================
            # RESULTS
            # =====================================================

            results.append({

                "account_id": account_id,

                "overall_sentiment": sentiment,

                "budget_issue": budget_issue,

                "competitor": competitor,

                "migration_issue": migration_issue,

                "executive_involved": executive,

                "renewal_risk_reason": summary,

                "ai_risk_score": ai_score,

                "ai_risk_level": ai_level,

                "note_length": len(chunk),

                "raw_note": chunk

            })

        df = pd.DataFrame(results)

        if len(df):

            df = df.drop_duplicates(
                subset="account_id",
                keep="first"
            )

        return df