import json


class ConsistencyChecker:

    def __init__(
        self,
        df,
        rules_path
    ):

        self.df = df

        with open(
            rules_path,
            "r"
        ) as file:

            self.rules = json.load(file)

    def analyze_consistency(self):

        results = []

        for column, config in self.rules.items():

            if column not in self.df.columns:
                continue

            consistency_config = config.get(
                "consistency",
                False
            )

            # Support both:
            # "consistency": true
            # and
            # "consistency": {"enabled": true}

            enabled = False

            if isinstance(
                consistency_config,
                bool
            ):
                enabled = consistency_config

            elif isinstance(
                consistency_config,
                dict
            ):
                enabled = consistency_config.get(
                    "enabled",
                    False
                )

            if not enabled:
                continue

            values = (
                self.df[column]
                .dropna()
                .astype(str)
            )

            total_values = len(values)

            if total_values == 0:
                continue

            standardized = (
                values
                .str.strip()
                .str.title()
            )

            inconsistent_count = int(
                (values != standardized).sum()
            )

            percentage = round(
                (
                    inconsistent_count
                    / total_values
                ) * 100,
                2
            )

            severity = self.assign_severity(
                percentage
            )

            results.append({

                "Column":
                    column,

                "Dimension":
                    "Consistency",

                "Issue Type":
                    "Formatting Inconsistency",

                "Affected Records":
                    inconsistent_count,

                "Percentage":
                    percentage,

                "Severity":
                    severity

            })

        return results

    def assign_severity(
        self,
        percentage
    ):

        if percentage == 0:
            return "None"

        elif percentage <= 5:
            return "Low"

        elif percentage <= 15:
            return "Medium"

        else:
            return "Critical"