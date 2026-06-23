import pandas as pd


class DataProfiler:

    def __init__(self, df, dataset_name="Unknown"):
        self.df = df
        self.dataset_name = dataset_name


    def generate_profile(self):
        """
        Generate basic dataset metadata.
        """

        profile = {
            "Dataset Name": self.dataset_name,
            "Total Rows": self.get_rows(),
            "Total Columns": self.get_columns(),
            "Memory Usage (MB)": self.get_memory_usage(),
            "Numeric Columns": self.get_numeric_count(),
            "Text Columns": self.get_text_count(),
            "Datetime Columns": self.get_datetime_count(),
            "Column Details": self.get_column_details()
        }

        return profile


    def get_rows(self):
        return self.df.shape[0]


    def get_columns(self):
        return self.df.shape[1]


    def get_memory_usage(self):
        memory = self.df.memory_usage(deep=True).sum()
        return round(memory / (1024 ** 2), 2)


    def get_numeric_count(self):
        return len(
            self.df.select_dtypes(
                include="number"
            ).columns
        )


    def get_text_count(self):
        return len(
            self.df.select_dtypes(
                include="object"
            ).columns
        )


    def get_datetime_count(self):
        return len(
            self.df.select_dtypes(
                include="datetime"
            ).columns
        )


    def get_column_details(self):

        details = []

        for column in self.df.columns:

            details.append(
                {
                    "Column": column,
                    "Data Type": str(self.df[column].dtype)
                }
            )

        return details