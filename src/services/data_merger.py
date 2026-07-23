import pandas as pd


class DataMerger:

    def merge_features(
        self,
        accounts,
        usage,
        tickets,
        nps
    ):

        merged = accounts.merge(
            usage,
            on="account_id",
            how="left"
        )

        merged = merged.merge(
            tickets,
            on="account_id",
            how="left"
        )

        merged = merged.merge(
            nps,
            on="account_id",
            how="left"
        )

        merged["total_tickets"] = merged["total_tickets"].fillna(0)
        merged["open_tickets"] = merged["open_tickets"].fillna(0)
        merged["escalated_tickets"] = merged["escalated_tickets"].fillna(0)
        merged["p1_tickets"] = merged["p1_tickets"].fillna(0)

        merged["avg_resolution_time"] = merged["avg_resolution_time"].fillna(0)

        merged["score"] = merged["score"].fillna(-1)
        merged["nps_category"] = merged["nps_category"].fillna("No Response")
        merged["verbatim_comment"] = merged["verbatim_comment"].fillna("")

        return merged