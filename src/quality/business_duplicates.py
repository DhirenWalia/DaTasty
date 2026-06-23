import json


class BusinessDuplicateChecker:

    def __init__(self, df, rules_path):

        self.df = df

        import os

        print("business_duplicates.py")
        print("cwd =", os.getcwd())
        print("rules_path =", rules_path)
        print("exists =", os.path.exists(rules_path))

        with open(rules_path, "r") as file:
            self.rules = json.load(file)

    def analyze(self):

        results = []

        total_rows = len(self.df)


        for column, rules in self.rules.items():

            if column not in self.df.columns:
                continue


            if not rules.get("business_key", False):
                continue


            duplicate_mask = (
                self.df[column]
                .duplicated(keep=False)
            )


            duplicate_count = int(
                duplicate_mask.sum()
            )


            duplicate_percentage = round(
                duplicate_count / total_rows * 100,
                2
            )


            severity = self.assign_severity(
                duplicate_percentage
            )


            results.append({

                "Business Key": column,

                "Duplicate Records":
                    duplicate_count,

                "Duplicate Percentage":
                    duplicate_percentage,

                "Severity":
                    severity

            })

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