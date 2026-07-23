import pandas as pd


class FeatureEngineer:

    def __init__(self, reference_date="2026-03-31"):
        self.reference_date = pd.Timestamp(reference_date)

    def build_usage_features(self, usage_df):

        usage_df = usage_df.sort_values(["account_id", "month"])

        features = []

        for account_id, group in usage_df.groupby("account_id"):

            first = group.iloc[0]
            last = group.iloc[-1]

            api_decline = (
                (first["api_calls"] - last["api_calls"])
                / first["api_calls"]
            ) * 100

            active_user_decline = (
                (first["active_users"] - last["active_users"])
                / first["active_users"]
            ) * 100

            workflow_decline = (
                (first["workflows_triggered"] - last["workflows_triggered"])
                / first["workflows_triggered"]
            ) * 100

            features.append({
                "account_id": account_id,
                "api_decline_pct": round(api_decline, 2),
                "active_user_decline_pct": round(active_user_decline, 2),
                "workflow_decline_pct": round(workflow_decline, 2),
                "latest_sdk": last["sdk_version"]
            })

        return pd.DataFrame(features)

    def build_ticket_features(self, ticket_df):

        features = []

        for account_id, group in ticket_df.groupby("account_id"):

            features.append({
                "account_id": account_id,
                "total_tickets": len(group),
                "open_tickets": (group["status"] == "Open").sum(),
                "escalated_tickets": (group["status"] == "Escalated").sum(),
                "p1_tickets": (group["priority"] == "P1").sum(),
                "avg_resolution_time": group["resolution_time_hours"].mean()
            })

        return pd.DataFrame(features)

    def build_nps_features(self, nps_df):

        nps_df = nps_df.copy()

        nps_df["nps_category"] = nps_df["score"].apply(
            lambda x: "Promoter" if x >= 9 else "Passive" if x >= 7 else "Detractor"
        )

        return nps_df

    def build_account_features(self, accounts_df):

        accounts_df = accounts_df.copy()

        accounts_df["days_to_renewal"] = (
            accounts_df["contract_end_date"] - self.reference_date
        ).dt.days

        accounts_df["renewing_next_90_days"] = (
            (accounts_df["days_to_renewal"] >= 0)
            &
            (accounts_df["days_to_renewal"] <= 90)
        )

        return accounts_df