import pandas as pd


class DataCleaner:

    def clean_accounts(self, df):

        df = df.copy()

        # Convert renewal date to datetime
        df["contract_end_date"] = pd.to_datetime(df["contract_end_date"])

        # Standardize text columns
        text_cols = [
            "account_name",
            "plan_tier",
            "industry",
            "csm_name",
            "region",
        ]

        for col in text_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

        return df


    def clean_usage(self, df):

        df = df.copy()

        df["month"] = pd.to_datetime(df["month"])

        return df


    def clean_tickets(self, df):

        df = df.copy()

        df["created_date"] = pd.to_datetime(df["created_date"])

        df["status"] = df["status"].str.strip()

        df["priority"] = df["priority"].str.upper()

        return df


    def clean_nps(self, df):

        df = df.copy()

        df["verbatim_comment"] = (
            df["verbatim_comment"]
            .fillna("")
            .str.strip()
        )

        return df