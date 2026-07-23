from src.services.data_loader import DataLoader
from src.services.data_cleaner import DataCleaner
from src.services.feature_engineering import FeatureEngineer
from src.services.data_merger import DataMerger
from src.utils.eda import inspect_dataframe
from src.scoring.risk_engine import RiskEngine
from src.reporting.report_generator import ReportGenerator
from src.services.changelog_parser import ChangelogParser
from src.analysis.llm_analyzer import LLMAnalyzer

import pandas as pd


def safe_preview(text, max_chars=1000):
    preview = str(text)
    preview = preview.encode("ascii", errors="ignore").decode("ascii")
    return preview[:max_chars]


def main():

    print("\nLoading datasets...\n")

    # ======================================================
    # LOAD DATA
    # ======================================================

    loader = DataLoader()

    accounts = loader.load_accounts()
    usage = loader.load_usage()
    tickets = loader.load_support_tickets()
    nps = loader.load_nps()

    notes = loader.load_csm_notes()
    changelog = loader.load_changelog()

    # ======================================================
    # CHANGELOG ANALYSIS
    # ======================================================

    parser = ChangelogParser()

    changelog_info = parser.parse(changelog)

    print("\n")
    print("=" * 70)
    print("CHANGELOG ANALYSIS")
    print("=" * 70)

    print(changelog_info["summary"])

    # ======================================================
    # EDA
    # ======================================================

    inspect_dataframe(accounts, "Accounts")
    inspect_dataframe(usage, "Usage Metrics")
    inspect_dataframe(tickets, "Support Tickets")
    inspect_dataframe(nps, "NPS Responses")

    print("\n" + "=" * 70)
    print("CSM NOTES")
    print("=" * 70)
    print(safe_preview(notes[:1000]))

    print("\n" + "=" * 70)
    print("CHANGELOG")
    print("=" * 70)
    print(safe_preview(changelog[:1000]))

    # ======================================================
    # CLEAN DATA
    # ======================================================

    cleaner = DataCleaner()

    accounts = cleaner.clean_accounts(accounts)
    usage = cleaner.clean_usage(usage)
    tickets = cleaner.clean_tickets(tickets)
    nps = cleaner.clean_nps(nps)

    # ======================================================
    # FEATURE ENGINEERING
    # ======================================================

    engineer = FeatureEngineer(
        reference_date="2026-03-31"
    )

    usage_features = engineer.build_usage_features(usage)

    ticket_features = engineer.build_ticket_features(tickets)

    nps_features = engineer.build_nps_features(nps)

    account_features = engineer.build_account_features(accounts)

    usage_features.to_csv(
        "outputs/usage_features.csv",
        index=False
    )

    ticket_features.to_csv(
        "outputs/ticket_features.csv",
        index=False
    )

    nps_features.to_csv(
        "outputs/nps_features.csv",
        index=False
    )

    account_features.to_csv(
        "outputs/account_features.csv",
        index=False
    )

    print("\nFeature Engineering Completed Successfully!")

    # ======================================================
    # CUSTOMER 360
    # ======================================================

    merger = DataMerger()

    customer_360 = merger.merge_features(
        account_features,
        usage_features,
        ticket_features,
        nps_features
    )

    customer_360.to_csv(
        "outputs/customer_360.csv",
        index=False
    )

    print("\nCustomer 360 Dataset Created!")

    # ======================================================
    # LLM ANALYSIS
    # ======================================================

    print("\nRunning AI Analysis...\n")

    llm = LLMAnalyzer()

    llm_results = llm.analyze_notes(notes)

    llm_results.to_csv(
        "outputs/llm_analysis.csv",
        index=False
    )

    print(llm_results.head())

    # ======================================================
    # MERGE LLM FEATURES
    # ======================================================

    customer_360 = customer_360.merge(
        llm_results,
        on="account_id",
        how="left"
    )

    customer_360.to_csv(
        "outputs/customer_360_ai.csv",
        index=False
    )

    print("\nCustomer 360 + AI Features Created!")

    # ======================================================
    # RISK ENGINE
    # ======================================================

    risk_engine = RiskEngine()

    customer_360 = risk_engine.calculate_risk(customer_360)

    customer_360.to_csv(
        "outputs/risk_scored_accounts.csv",
        index=False
    )

    print("\nRisk Scoring Completed!")

    # ======================================================
    # NEXT 90 DAY RENEWALS
    # ======================================================

    renewal_accounts = customer_360[
        customer_360["renewing_next_90_days"] == True
    ].copy()

    renewal_accounts.to_csv(
        "outputs/renewals_next_90_days.csv",
        index=False
    )

    print(
        f"\nAccounts renewing in next 90 days : {len(renewal_accounts)}"
    )

    # ======================================================
    # REPORT GENERATION
    # ======================================================

    report_generator = ReportGenerator()

    final_report = report_generator.generate(
        renewal_accounts
    )

    final_report.to_csv(
        "outputs/final_report.csv",
        index=False
    )

    print("\nFinal Report Generated!")

    # ======================================================
    # NON-OBVIOUS INSIGHTS
    # ======================================================

    insights = []

    sdk_accounts = customer_360[
        customer_360["latest_sdk"].astype(str).str.startswith("v3")
    ]

    insights.append({

        "Insight":
        "Customers still using SDK v3",

        "Value":
        len(sdk_accounts)

    })

    high_risk = customer_360[
        customer_360["risk_tier"] == "High"
    ]

    insights.append({

        "Insight":
        "High Risk Accounts",

        "Value":
        len(high_risk)

    })

    arr_risk = high_risk["arr"].sum()

    insights.append({

        "Insight":
        "ARR at High Risk",

        "Value":
        arr_risk

    })

    passive = customer_360[
        customer_360["score"].between(7, 8, inclusive="both")
    ]

    insights.append({

        "Insight":
        "Passive NPS Customers",

        "Value":
        len(passive)

    })

    insight_df = pd.DataFrame(insights)

    insight_df.to_csv(
        "outputs/business_insights.csv",
        index=False
    )

    print("\nBusiness Insights Generated!")

    print(insight_df)

    # ======================================================
    # SAMPLE OUTPUT
    # ======================================================

    print("\n")
    print("=" * 80)
    print("TOP HIGH RISK CUSTOMERS")
    print("=" * 80)

    print(
        final_report[
            [
                "account_name",
                "risk_score",
                "risk_tier",
                "overall_sentiment",
                "competitor",
                "budget_issue",
                "migration_issue",
                "executive_involved",
                "recommended_action"
            ]
        ].head(10)
    )

    print("\nProject Completed Successfully!")


if __name__ == "__main__":
    main()