import json
import os


class DashboardExporter:


    def __init__(
        self,
        profile,
        dts_report,
        missing_report,
        duplicate_report,
        validity_report,
        consistency_report,
        accuracy_report
    ):

        self.profile = profile

        self.dts_report = dts_report

        self.missing = missing_report

        self.duplicates = duplicate_report

        self.validity = validity_report

        self.consistency = consistency_report

        self.accuracy = accuracy_report


    def export(self):

        critical_count = 0


        reports = [
            self.missing,
            self.validity,
            self.consistency,
            self.accuracy
        ]


        for report in reports:

            for item in report:

                if item["Severity"] == "Critical":

                    critical_count += 1


        data = {

            "dataset": {

                "name":
                self.profile["Dataset Name"],

                "rows":
                self.profile["Total Rows"],

                "columns":
                self.profile["Total Columns"]

            },


            "dts": {

                "score":
                self.dts_report["DTS Score"],


                "status":
                self.dts_report["Status"],


                "dimensions":
                self.dts_report[
                    "Dimension Scores"
                ]

            },


            "issues": {

                "critical":
                critical_count

            }

        }


        os.makedirs(
            "output",
            exist_ok=True
        )


        with open(
            "output/dashboard_metrics.json",
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )


        print(
            "\nDashboard JSON exported successfully."
        )