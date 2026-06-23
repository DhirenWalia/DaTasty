import time

from src.ingestion.loader import DataLoader
from src.profiling.profiler import DataProfiler

from src.quality.completeness import CompletenessChecker
from src.quality.uniqueness import UniquenessChecker
from src.quality.business_duplicates import BusinessDuplicateChecker
from src.quality.validity import ValidityChecker
from src.quality.consistency import ConsistencyChecker
from src.quality.accuracy import AccuracyChecker

from src.scoring.dts_calculator import DTSCalculator

from src.recommendations.advisor import RecommendationEngine

from src.cleaning.smart_cleaner import SmartCleaner
from src.reporting.report_generator import ReportGenerator




def main():
    start_time = time.time()

    print("\n========== DATATSTY ==========")
    print("AI Data Readiness Assessment Platform\n")

    # ==============================
    # DATA LOADING
    # ==============================
   
    file_path = input("Enter dataset path: ")

    loader = DataLoader()

    df = loader.load_data(file_path)


    # ==============================
    # DATA PROFILING
    # ==============================

    profiler = DataProfiler(
        df,
        file_path
    )

    profile = profiler.generate_profile()


    # ==============================
    # QUALITY ANALYSIS
    # ==============================

    completeness = CompletenessChecker(df)
    missing_report = completeness.calculate_missing_values()


    uniqueness = UniquenessChecker(df)
    duplicate_report = uniqueness.analyze_duplicates()


    business_duplicates = BusinessDuplicateChecker(
        df,
        "config/rules.json"
    )

    business_duplicate_report = (
        business_duplicates.analyze()
    )


    validity = ValidityChecker(
        df,
        "config/rules.json"
    )

    validity_report = validity.analyze_validity()


    consistency = ConsistencyChecker(
        df,
        "config/rules.json"
    )


    consistency_report = (
        consistency.analyze_consistency()
    )

    accuracy = AccuracyChecker(df)

    accuracy_report = (
        accuracy.analyze_outliers()
    )


    # ==============================
    # DTS SCORING
    # ==============================

    dts = DTSCalculator(
        missing_report,
        duplicate_report,
        validity_report,
        consistency_report,
        accuracy_report
    )

    dts_report = dts.calculate_score()


    # ==============================
    # BUSINESS RECOMMENDATIONS
    # ==============================

    advisor = RecommendationEngine(
        missing_report,
        duplicate_report,
        validity_report,
        consistency_report,
        accuracy_report
    )

    recommendations = (
        advisor.generate_recommendations()
    )


    # ==============================
    # DISPLAY RESULTS
    # ==============================


    print("\n========== DATASET PROFILE ==========")

    for key, value in profile.items():

        if key != "Column Details":
            print(f"{key}: {value}")

    print("\nCOLUMN DETAILS")

    for column in profile["Column Details"]:

        print(
            f"{column['Column']} : {column['Data Type']}"
        )


    print("\n========== MISSING VALUE ANALYSIS ==========")

    for item in missing_report:

        print(
            f"{item['Column']} | "
            f"Missing: {item['Missing Count']} | "
            f"{item['Missing Percentage']}% | "
            f"Severity: {item['Severity']}"
        )


    print("\n========== DUPLICATE ANALYSIS ==========")

    for key, value in duplicate_report.items():

        print(f"{key}: {value}")


    print("\n========== BUSINESS KEY DUPLICATES ==========")

    if not business_duplicate_report:

        print("No business key duplicate issues found.")

    else:

        for item in business_duplicate_report:

            print(
                f"{item['Business Key']} | "
                f"Duplicates: {item['Duplicate Records']} | "
                f"{item['Duplicate Percentage']}% | "
                f"Severity: {item['Severity']}"
            )


    print("\n========== VALIDITY ANALYSIS ==========")

    for item in validity_report:

        print(
            f"{item['Column']} | "
            f"Invalid: {item['Invalid Count']} | "
            f"{item['Invalid Percentage']}% | "
            f"Severity: {item['Severity']}"
        )


    print("\n========== CONSISTENCY ANALYSIS ==========")

    for item in consistency_report:

        print(
            f"{item['Column']} | "
            f"Affected: {item['Affected Records']} | "
            f"{item['Percentage']}% | "
            f"Severity: {item['Severity']}"
        )


    print("\n========== ACCURACY ANALYSIS ==========")

    if not accuracy_report:

        print(
            "No suitable numeric columns found for outlier analysis."
        )

    else:

        for item in accuracy_report:

            print(
                f"{item['Column']} | "
                f"Outliers: {item['Outlier Count']} | "
                f"{item['Outlier Percentage']}% | "
                f"Severity: {item['Severity']}"
            )


    print("\n========== DATATSTY SCORE ==========")

    for dimension, score in (
        dts_report["Dimension Scores"].items()
    ):

        print(
            f"{dimension}: {score}"
        )

    print("\n---------------------")

    print(
        f"DTS Score: {dts_report['DTS Score']}"
    )

    print(
        f"AI Readiness: {dts_report['Status']}"
    )


    print("\n========== RECOMMENDATIONS ==========")

    if not recommendations:

        print(
            "No major data quality issues detected."
        )

    else:

        for item in recommendations:

            print(
                f"\nIssue: {item['Issue']}"
            )

            print(
                f"Impact: {item['Business Impact']}"
            )

            print(
                f"Priority: {item['Priority']}"
            )

            print(
                f"Recommendation: {item['Recommendation']}"
            )

            print("-" * 50)


    # ==============================
    # OPTIONAL SMART CLEANING
    # ==============================

    print("\n========== SMART CLEANING ==========")

    choice = input(
        "Apply DATATSTY smart cleaning? (Y/N): "
    )


    if choice.upper() == "Y":

        cleaner = SmartCleaner(
            df,
            "config/rules.json"
        )

        cleaned_df, cleaning_log = (
            cleaner.clean_data()
        )

        path = cleaner.save_clean_data()


        print("\nCleaning Completed!")

        print(
            f"Cleaned dataset saved at: {path}"
        )


        print("\nCLEANING LOG")

        for item in cleaning_log:

            print(item)


    else:

        print(
            "No automatic cleaning applied."
        )


    print(
        "\nDATATSTY analysis completed successfully."
    )

    report = ReportGenerator(
    profile,
    missing_report,
    duplicate_report,
    business_duplicate_report,
    validity_report,
    consistency_report,
    accuracy_report,
    dts_report,
    recommendations
)

    report.generate_report()
    # from src.dashboard.dashboard_export import DashboardExporter

    end_time = time.time()

    execution_time = round(
        end_time - start_time ,
        2
    )

    print("\n========== PERFORMANCE REPORT ==========")

    print(
        f"Total Execution Time: {execution_time} seconds"
    )
if __name__ == "__main__":
    main()