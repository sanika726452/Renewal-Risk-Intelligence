import pandas as pd


class ReportGenerator:

    def generate(self, customer_360):

        report = customer_360.copy()

        explanations = []
        recommendations = []
        priorities = []

        for _, row in report.iterrows():

            tier = row["risk_tier"]

            reasons = []

            # ======================================================
            # Usage
            # ======================================================

            if pd.notna(row["api_decline_pct"]):

                if row["api_decline_pct"] >= 50:
                    reasons.append(
                        f"API usage has declined by {row['api_decline_pct']:.1f}% over the last six months."
                    )

                elif row["api_decline_pct"] >= 30:
                    reasons.append(
                        "API usage is showing a noticeable downward trend."
                    )

            if pd.notna(row["active_user_decline_pct"]):

                if row["active_user_decline_pct"] >= 40:
                    reasons.append(
                        f"Active users have dropped by {row['active_user_decline_pct']:.1f}%."
                    )

            if pd.notna(row["workflow_decline_pct"]):

                if row["workflow_decline_pct"] >= 30:
                    reasons.append(
                        "Workflow adoption is decreasing."
                    )

            # ======================================================
            # SDK
            # ======================================================

            sdk = str(row["latest_sdk"])

            if sdk.startswith("v3"):
                reasons.append(
                    "The customer is still using the deprecated SDK v3, increasing migration risk."
                )

            # ======================================================
            # Support
            # ======================================================

            if pd.notna(row["p1_tickets"]):

                if row["p1_tickets"] >= 3:
                    reasons.append(
                        f"{int(row['p1_tickets'])} critical P1 support tickets were raised."
                    )

            if pd.notna(row["escalated_tickets"]):

                if row["escalated_tickets"] >= 2:
                    reasons.append(
                        "Multiple support cases have been escalated."
                    )

            if pd.notna(row["avg_resolution_time"]):

                if row["avg_resolution_time"] > 48:
                    reasons.append(
                        f"Average support resolution time is {row['avg_resolution_time']:.1f} hours."
                    )

            # ======================================================
            # NPS
            # ======================================================

            if pd.notna(row["score"]):

                if row["score"] <= 6:
                    reasons.append(
                        f"The latest NPS score is {int(row['score'])}, indicating a dissatisfied customer."
                    )

                elif row["score"] <= 8:
                    reasons.append(
                        f"The customer is currently an NPS Passive (Score {int(row['score'])})."
                    )

            # ======================================================
            # Renewal
            # ======================================================

            if pd.notna(row["days_to_renewal"]):

                if row["days_to_renewal"] <= 30:
                    reasons.append(
                        "The renewal date is within the next 30 days."
                    )

                elif row["days_to_renewal"] <= 90:
                    reasons.append(
                        "The account is approaching renewal."
                    )

            # ======================================================
            # ARR
            # ======================================================

            if pd.notna(row["arr"]):

                if row["arr"] >= 1000000:
                    reasons.append(
                        "This is a strategic high-value ARR account."
                    )

            # ======================================================
            # LLM Signals
            # ======================================================

            if "overall_sentiment" in row:

                sentiment = str(row["overall_sentiment"]).lower()

                if sentiment == "negative":
                    reasons.append(
                        "AI analysis detected an overall negative customer sentiment."
                    )

            if "budget_issue" in row:

                if row["budget_issue"] is True:
                    reasons.append(
                        "Budget concerns were detected from CSM conversations."
                    )

            if "migration_issue" in row:

                if row["migration_issue"] is True:
                    reasons.append(
                        "Migration challenges were identified."
                    )

            if "executive_involved" in row:

                if row["executive_involved"] is True:
                    reasons.append(
                        "Executive stakeholders are actively involved."
                    )

            if "competitor" in row:

                competitor = str(row["competitor"]).strip()

                if competitor != "":
                    reasons.append(
                        f"The customer appears to be evaluating {competitor}."
                    )

            # ======================================================
            # Executive Summary
            # ======================================================

            if len(reasons) == 0:

                explanation = (
                    "Customer health indicators remain stable with no significant renewal risks detected."
                )

            else:

                explanation = (
                    f"{row['account_name']} has a {tier.lower()} renewal risk because "
                    + " ".join(reasons)
                )

            # ======================================================
            # Recommendations
            # ======================================================

            if tier == "High":

                recommendation = (
                    "Arrange an executive business review immediately. Engage the Customer Success Manager, Solutions Engineer and Product team to address technical blockers, resolve open support issues, discuss migration planning and prepare a renewal strategy before contract expiry."
                )

                priority = "Immediate"

            elif tier == "Medium":

                recommendation = (
                    "Schedule a proactive customer health check, review product adoption, address outstanding support concerns and monitor engagement closely until renewal."
                )

                priority = "High"

            else:

                recommendation = (
                    "Maintain regular engagement through periodic business reviews, continue adoption campaigns and monitor for any early warning signals."
                )

                priority = "Normal"

            explanations.append(explanation)
            recommendations.append(recommendation)
            priorities.append(priority)

        report["explanation"] = explanations
        report["recommended_action"] = recommendations
        report["priority"] = priorities

        return report