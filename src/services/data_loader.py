from pathlib import Path
import pandas as pd


class DataLoader:
    """
    Responsible for loading all raw datasets.
    """

    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)

    def load_accounts(self):
        return pd.read_csv(self.data_dir / "accounts.csv")

    def load_usage(self):
        return pd.read_csv(self.data_dir / "usage_metrics.csv")

    def load_support_tickets(self):
        return pd.read_csv(self.data_dir / "support_tickets.csv")

    def load_nps(self):
        return pd.read_csv(self.data_dir / "nps_responses.csv")

    def load_csm_notes(self):
        with open(self.data_dir / "csm_notes.txt", "r", encoding="utf-8") as f:
            return f.read()

    def load_changelog(self):
        with open(self.data_dir / "changelog.md", "r", encoding="utf-8") as f:
            return f.read()