import json
import re
import pandas as pd

class ValidityChecker:

    def __init__(self, df, rules_path):
        self.df = df

        with open(rules_path, "r") as file:
            self.rules = json.load(file)


    def analyze_validity(self):

        results = []

        total_rows = len(self.df)


        for column, rules in self.rules.items():

            if column not in self.df.columns:
                continue


            datatype = rules.get("datatype")
            validation_rules = rules.get(
                "validation",
                {}
            )


            invalid_count = self.validate_column(
                self.df[column],
                datatype,
                validation_rules
            )


            invalid_percentage = round(
                (invalid_count / total_rows) * 100,
                2
            )


            severity = self.assign_severity(
                invalid_percentage
            )


            results.append(
                {
                    "Column": column,
                    "Invalid Count": invalid_count,
                    "Invalid Percentage": invalid_percentage,
                    "Severity": severity
                }
            )

        return results


    def validate_column(
        self,
        series,
        datatype,
        rules
    ):


        if datatype == "numeric":

            minimum = rules.get(
                "min",
                float("-inf")
            )

            maximum = rules.get(
                "max",
                float("inf")
            )

            # Convert values safely to numeric
            numeric_series = (
                pd.to_numeric(
                    series,
                    errors="coerce"
                )
            )

            # Invalid data type values
            invalid_type = (
                numeric_series.isna()
                &
                series.notna()
            )

            # Values outside valid range
            invalid_range = (
                (numeric_series < minimum)
                |
                (numeric_series > maximum)
            )

            invalid = (
                invalid_type
                |
                invalid_range
            )

            return int(
                invalid.sum()
            )

        elif datatype == "email":

            pattern = (
                r"^[\w\.-]+@[\w\.-]+\.\w+$"
            )


            invalid = (
                ~series.fillna("")
                .astype(str)
                .str.match(pattern)
            )


            return int(
                invalid.sum()
            )


        return 0



    def assign_severity(
        self,
        percentage
    ):

        if percentage == 0:
            return "None"

        elif percentage <= 1:
            return "Low"

        elif percentage <= 5:
            return "Medium"

        else:
            return "Critical"