import pandas as pd


class RiskEngine:

    def calculate_risk(self, customer_360):

        df = customer_360.copy()

        risk_scores = []
        risk_tiers = []
        risk_reasons = []
        confidence_scores = []

        for _, row in df.iterrows():

            score = 0
            confidence = 50
            reasons = []

            # =====================================================
            # PRODUCT USAGE
            # =====================================================

            api_decline = row.get("api_decline_pct", 0)

            if pd.notna(api_decline):

                if api_decline >= 60:
                    score += 30
                    confidence += 10
                    reasons.append("Severe API usage decline")

                elif api_decline >= 40:
                    score += 20
                    confidence += 7
                    reasons.append("Significant API usage decline")

                elif api_decline >= 20:
                    score += 10
                    reasons.append("Moderate API usage decline")

            active_decline = row.get("active_user_decline_pct", 0)

            if pd.notna(active_decline):

                if active_decline >= 50:
                    score += 25
                    confidence += 8
                    reasons.append("Major drop in active users")

                elif active_decline >= 30:
                    score += 15
                    reasons.append("Active users declining")

            workflow_decline = row.get("workflow_decline_pct", 0)

            if pd.notna(workflow_decline):

                if workflow_decline >= 50:
                    score += 15
                    reasons.append("Workflow adoption dropped sharply")

                elif workflow_decline >= 30:
                    score += 10
                    reasons.append("Workflow activity reduced")

            # =====================================================
            # SDK VERSION
            # =====================================================

            sdk = str(row.get("latest_sdk", ""))

            if sdk.startswith("v3"):
                score += 20
                confidence += 5
                reasons.append("Customer still using deprecated SDK v3")

            # =====================================================
            # SUPPORT HEALTH
            # =====================================================

            p1 = row.get("p1_tickets", 0)

            if pd.notna(p1):

                if p1 >= 4:
                    score += 20
                    confidence += 5
                    reasons.append("Very high number of P1 incidents")

                elif p1 >= 2:
                    score += 12
                    reasons.append("Multiple critical support tickets")

            escalated = row.get("escalated_tickets", 0)

            if pd.notna(escalated):

                if escalated >= 2:
                    score += 10
                    reasons.append("Support escalations detected")

            resolution = row.get("avg_resolution_time", 0)

            if pd.notna(resolution):

                if resolution > 72:
                    score += 15
                    reasons.append("Very slow support resolution")

                elif resolution > 48:
                    score += 10
                    reasons.append("Slow support resolution")

            # =====================================================
            # NPS
            # =====================================================

            nps = row.get("score")

            if pd.notna(nps):

                if nps <= 6:
                    score += 20
                    confidence += 5
                    reasons.append("Customer is an NPS Detractor")

                elif nps <= 8:
                    score += 8
                    reasons.append("Customer is an NPS Passive")

                else:
                    score -= 5

            # =====================================================
            # CONTRACT RENEWAL
            # =====================================================

            renewal = row.get("days_to_renewal")

            if pd.notna(renewal):

                if renewal <= 30:
                    score += 15
                    reasons.append("Renewal due within 30 days")

                elif renewal <= 60:
                    score += 10
                    reasons.append("Renewal approaching")

                elif renewal <= 90:
                    score += 5

            # =====================================================
            # ARR IMPACT
            # =====================================================

            arr = row.get("arr", 0)

            if pd.notna(arr):

                if arr >= 1000000:
                    score += 10
                    reasons.append("High ARR account")

                elif arr >= 500000:
                    score += 5

            # =====================================================
            # PLAN TIER
            # =====================================================

            plan = str(row.get("plan_tier", "")).lower()

            if plan == "enterprise":
                score += 5

            elif plan == "scale":
                score += 3

            # =====================================================
            # LLM SIGNALS (Future Ready)
            # =====================================================

            if "overall_sentiment" in row:

                sentiment = str(row["overall_sentiment"]).lower()

                if sentiment == "negative":
                    score += 15
                    reasons.append("Negative customer sentiment")

                elif sentiment == "neutral":
                    score += 5

            if row.get("budget_issue", False):
                score += 15
                confidence += 5
                reasons.append("Budget concerns identified")

            if row.get("migration_issue", False):
                score += 15
                confidence += 5
                reasons.append("Migration concerns identified")

            if row.get("executive_involved", False):
                score += 12
                confidence += 5
                reasons.append("Executive leadership involved")

            competitor = str(row.get("competitor", "")).strip()

            if competitor != "":
                score += 15
                confidence += 5
                reasons.append(f"Evaluating competitor ({competitor})")


            if (
                pd.notna(nps)
                and nps >= 9
                and pd.notna(api_decline)
                and api_decline < 10
                and pd.notna(p1)
                and p1 == 0
            ):
                score -= 10
                reasons.append("Strong customer health offsets renewal risk") 
                   
            # =====================================================
            # SCORE NORMALIZATION
            # =====================================================

            if score < 0:
                score = 0

            if score > 100:
                score = 100

            if confidence > 100:
                confidence = 100

            # =====================================================
            # RISK TIER
            # =====================================================

            if score >= 70:
                tier = "High"

            elif score >= 40:
                tier = "Medium"

            else:
                tier = "Low"

            if len(reasons) == 0:
                reasons.append("No major renewal risks detected")

            risk_scores.append(score)
            risk_tiers.append(tier)
            confidence_scores.append(confidence)
            risk_reasons.append(" | ".join(reasons))

        df["risk_score"] = risk_scores
        df["risk_tier"] = risk_tiers
        df["confidence_score"] = confidence_scores
        df["risk_reasons"] = risk_reasons

        return df