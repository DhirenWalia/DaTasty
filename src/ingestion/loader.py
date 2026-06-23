import pandas as pd
from pathlib import Path


class DataLoader:

    def __init__(self):
        pass


    def load_data(self, source):
        """
        Main entry point for loading datasets.
        """

        source = Path(source)

        if source.suffix == ".csv":
            return self._load_csv(source)

        elif source.suffix in [".xlsx", ".xls"]:
            return self._load_excel(source)

        else:
            raise ValueError(
                "Unsupported file format. Use CSV or Excel."
            )


    def _load_csv(self, path):
        """
        Load CSV file.
        """

        try:
            df = pd.read_csv(path)

            print("CSV loaded successfully.")

            return df

        except Exception as e:
            raise Exception(
                f"Error loading CSV: {e}"
            )


    def _load_excel(self, path):
        """
        Load Excel file.
        """

        try:
            df = pd.read_excel(path)

            print("Excel loaded successfully.")

            return df

        except Exception as e:
            raise Exception(
                f"Error loading Excel: {e}"
            )
        
        