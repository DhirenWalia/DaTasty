from turtle import pd

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
# from src.reporting.pdf_report import PDFReportGenerator

class DATATSTYEngine:

    def __init__(
        self,
        dataset_path,
        rules_path="../config/rules.json"
    ):
        self.dataset_path = dataset_path
        self.rules_path = rules_path

    def run(self):

        loader = DataLoader()

        df = loader.load_data(
            self.dataset_path
        )

        profile = DataProfiler(
            df,
            self.dataset_path
        ).generate_profile()

        missing_report = (
            CompletenessChecker(df)
            .calculate_missing_values()
        )

        duplicate_report = (
            UniquenessChecker(df)
            .analyze_duplicates()
        )

        business_duplicate_report = (
            BusinessDuplicateChecker(
                df,
                self.rules_path
            ).analyze()
        )

        validity_report = (
            ValidityChecker(
                df,
                self.rules_path
            ).analyze_validity()
        )

        consistency_report = (
            ConsistencyChecker(
                df,
                self.rules_path
            ).analyze_consistency()
        )

        accuracy_report = (
            AccuracyChecker(df)
            .analyze_outliers()
        )

        dts_report = (
            DTSCalculator(
                missing_report,
                duplicate_report,
                validity_report,
                consistency_report,
                accuracy_report
            ).calculate_score()
        )

        recommendations = (
            RecommendationEngine(
                missing_report,
                duplicate_report,
                validity_report,
                consistency_report,
                accuracy_report
            ).generate_recommendations()
        )

        import pandas as pd

        findings_df = pd.DataFrame()

        for item in missing_report:
            findings_df = pd.concat([
                findings_df,
                pd.DataFrame([{
                    "Dimension": "Completeness",
                    "Column": item["Column"],
                    "Issue": "Missing Values",
                    "Count": item["Missing Count"],
                    "Percentage": item["Missing Percentage"],
                    "Severity": item["Severity"]
                }])
            ])

        for item in validity_report:
            findings_df = pd.concat([
                findings_df,
                pd.DataFrame([{
                    "Dimension": "Validity",
                    "Column": item["Column"],
                    "Issue": "Invalid Values",
                    "Count": item["Invalid Count"],
                    "Percentage": item["Invalid Percentage"],
                    "Severity": item["Severity"]
                }])
            ])

        report_path = (
            ReportGenerator(
                profile,
                missing_report,
                duplicate_report,
                business_duplicate_report,
                validity_report,
                consistency_report,
                accuracy_report,
                dts_report,
                recommendations
            ).generate_report()
        )

        # pdf_path = (
        #     PDFReportGenerator(
        #         profile,
        #         dts_report,
        #         recommendations,
        #         findings_df
        #     ).generate()
        # )

        cleaner = SmartCleaner(
            df,
            self.rules_path
        )

        cleaner.clean_data()

        cleaned_path = (
            cleaner.save_clean_data()
        )

# ==========================
# AFTER CLEANING ANALYSIS
# ==========================

        cleaned_profile = DataProfiler(
            cleaner.df,
            "Cleaned Dataset"
        ).generate_profile()

        cleaned_missing = (
            CompletenessChecker(
                cleaner.df
            ).calculate_missing_values()
        )

        cleaned_duplicate = (
            UniquenessChecker(
                cleaner.df
            ).analyze_duplicates()
        )

        cleaned_validity = (
            ValidityChecker(
                cleaner.df,
                self.rules_path
            ).analyze_validity()
        )

        cleaned_consistency = (
            ConsistencyChecker(
                cleaner.df,
                self.rules_path
            ).analyze_consistency()
        )

        cleaned_accuracy = (
            AccuracyChecker(
                cleaner.df
            ).analyze_outliers()
        )

        cleaned_dts = (
            DTSCalculator(
                cleaned_missing,
                cleaned_duplicate,
                cleaned_validity,
                cleaned_consistency,
                cleaned_accuracy
            ).calculate_score()
        )

        improvement = round(
            cleaned_dts["DTS Score"]
            -
            dts_report["DTS Score"],
            2
        )
        return {

            "report_path":
                report_path,

            # "pdf_path":
            #     pdf_path,

            "cleaned_path":
                cleaned_path,

            "before_dts":
                dts_report["DTS Score"],

            "after_dts":
                cleaned_dts["DTS Score"],

            "improvement":
                improvement,

            "status":
                cleaned_dts["Status"]
        }