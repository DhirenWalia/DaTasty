import numpy as np


class AccuracyChecker:

    def __init__(self, df):
        self.df = df


    def analyze_outliers(self):

        results = []

        total_rows = len(self.df)

        numeric_columns = self.df.select_dtypes(
            include="number"
        ).columns


        for column in numeric_columns:

            values = self.df[column].dropna()


            # Skip columns with too few unique values
            if values.nunique() < 5:
                continue


            q1 = np.percentile(values, 25)
            q3 = np.percentile(values, 75)

            iqr = q3 - q1


            lower_limit = q1 - (1.5 * iqr)
            upper_limit = q3 + (1.5 * iqr)


            outliers = (
                (values < lower_limit)
                |
                (values > upper_limit)
            )


            outlier_count = int(outliers.sum())


            outlier_percentage = round(
                (outlier_count / total_rows) * 100,
                2
            )


            severity = self.assign_severity(
                outlier_percentage
            )


            results.append(
                {
                    "Column": column,
                    "Method": "IQR",
                    "Outlier Count": outlier_count,
                    "Outlier Percentage": outlier_percentage,
                    "Severity": severity
                }
            )


        return results


    def assign_severity(self, percentage):

        if percentage == 0:
            return "None"

        elif percentage <= 1:
            return "Low"

        elif percentage <= 5:
            return "Medium"

        else:
            return "Critical"