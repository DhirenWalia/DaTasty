class CompletenessChecker:

    def __init__(self, df):
        self.df = df


    def calculate_missing_values(self):
        """
        Analyze missing values in each column.
        """

        results = []

        total_rows = len(self.df)

        for column in self.df.columns:

            missing_count = self.df[column].isna().sum()

            missing_percentage = round(
                (missing_count / total_rows) * 100,
                2
            )

            severity = self.assign_severity(
                missing_percentage
            )

            results.append(
                {
                    "Column": column,
                    "Missing Count": int(missing_count),
                    "Missing Percentage": missing_percentage,
                    "Severity": severity
                }
            )

        return results


    def assign_severity(self, percentage):
        """
        Assign risk level based on missing percentage.
        """

        if percentage == 0:
            return "None"

        elif percentage <= 5:
            return "Low"

        elif percentage <= 15:
            return "Medium"

        else:
            return "Critical"