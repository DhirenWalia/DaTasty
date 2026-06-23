class DTSCalculator:

    def __init__(
        self,
        missing_report,
        duplicate_report,
        validity_report,
        consistency_report,
        accuracy_report
    ):

        self.missing = missing_report
        self.duplicate = duplicate_report
        self.validity = validity_report
        self.consistency = consistency_report
        self.accuracy = accuracy_report


        self.weights = {
            "Completeness": 0.25,
            "Uniqueness": 0.20,
            "Validity": 0.20,
            "Consistency": 0.20,
            "Accuracy": 0.15
        }


    def calculate_score(self):

        scores = {

            "Completeness":
                self.calculate_average(self.missing,
                                       "Missing Percentage"),


            "Uniqueness":
                100 - self.duplicate["Duplicate Percentage"],


            "Validity":
                self.calculate_average(self.validity,
                                       "Invalid Percentage"),


            "Consistency":
                self.calculate_average(self.consistency,
                                       "Percentage"),


            "Accuracy":
                self.calculate_average(self.accuracy,
                                       "Outlier Percentage")
        }


        weighted_score = 0


        for category, score in scores.items():

            weighted_score += (
                score * self.weights[category]
            )


        return {
            "Dimension Scores": scores,
            "DTS Score": round(weighted_score, 2),
            "Status": self.get_status(weighted_score)
        }


    def calculate_average(self, report, key):

        if not report:
            return 100


        average_issue = (
            sum(item[key] for item in report)
            / len(report)
        )


        return round(100 - average_issue, 2)


    def get_status(self, score):

        if score >= 90:
            return "AI Ready"

        elif score >= 75:
            return "Good"

        elif score >= 60:
            return "Needs Attention"

        else:
            return "Not AI Ready"