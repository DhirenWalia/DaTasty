class UniquenessChecker:

    def __init__(self, df):
        self.df = df


    def analyze_duplicates(self):
        """
        Analyze duplicate rows in the dataset.
        """

        total_records = len(self.df)

        duplicate_count = self.df.duplicated().sum()

        duplicate_percentage = round(
            (duplicate_count / total_records) * 100,
            2
        )

        severity = self.assign_severity(
            duplicate_percentage
        )

        results = {
            "Total Records": total_records,
            "Duplicate Records": int(duplicate_count),
            "Duplicate Percentage": duplicate_percentage,
            "Severity": severity
        }

        return results


    def assign_severity(self, percentage):
        """
        Assign risk level based on duplicate percentage.
        """

        if percentage == 0:
            return "None"

        elif percentage <= 1:
            return "Low"

        elif percentage <= 3:
            return "Medium"

        else:
            return "Critical"
        