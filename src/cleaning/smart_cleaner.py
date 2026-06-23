import json
import os
import pandas as pd


class SmartCleaner:

    def __init__(self, df, rules_path):

        self.original_df = df.copy()
        self.df = df.copy()

        self.cleaning_log = []

        with open(rules_path, "r") as file:
            self.rules = json.load(file)

    def clean_data(self):

        self.remove_duplicates()

        for column, config in self.rules.items():

            if column not in self.df.columns:
                continue

            cleaning = config.get(
                "cleaning",
                {}
            )

            if not cleaning.get(
                "enabled",
                False
            ):
                continue

            self.clean_column(
                column,
                cleaning
            )

        return self.df, self.cleaning_log

    def clean_column(
        self,
        column,
        rules
    ):

        original = self.df[column].copy()

        series = self.df[column]

        # ==========================
        # Pipeline Based Cleaning
        # ==========================

        pipeline = rules.get(
            "pipeline",
            []
        )

        if "trim" in pipeline:

            series = (
                series
                .astype(str)
                .str.strip()
            )

        if "lower" in pipeline:

            series = (
                series
                .astype(str)
                .str.lower()
            )

        if "upper" in pipeline:

            series = (
                series
                .astype(str)
                .str.upper()
            )

        if "title" in pipeline:

            series = (
                series
                .astype(str)
                .str.title()
            )

        self.df[column] = series

        # ==========================
        # Phone Standardization
        # ==========================

        if rules.get(
            "remove_symbols",
            False
        ):

            self.standardize_phone(
                column,
                rules
            )

        # ==========================
        # Date Standardization
        # ==========================

        if "date_format" in rules:

            self.standardize_date(
                column,
                rules
            )

        changes = (
            original.astype(str)
            !=
            self.df[column].astype(str)
        ).sum()

        self.cleaning_log.append({

            "Column":
                column,

            "Action":
                "Rule Based Cleaning",

            "Records Modified":
                int(changes)

        })

    def remove_duplicates(self):

        before = len(self.df)

        self.df.drop_duplicates(
            inplace=True
        )

        removed = (
            before -
            len(self.df)
        )

        self.cleaning_log.append({

            "Column":
                "Entire Dataset",

            "Action":
                "Duplicate Removal",

            "Records Modified":
                int(removed)

        })

    def standardize_phone(
        self,
        column,
        rules
    ):

        digits = rules.get(
            "keep_last_digits",
            10
        )

        self.df[column] = (

            self.df[column]
            .astype(str)
            .str.replace(
                r"\D",
                "",
                regex=True
            )
            .str[-digits:]

        )

    def standardize_date(
        self,
        column,
        rules
    ):

        format_rule = rules.get(
            "date_format",
            "%Y-%m-%d"
        )

        dates = pd.to_datetime(
            self.df[column],
            errors="coerce"
        )

        self.df[column] = (
            dates.dt.strftime(
                format_rule
            )
        )

    def save_clean_data(
        self,
        path="data/output/cleaned_dataset.csv"
    ):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        self.df.to_csv(
            path,
            index=False
        )

        return path