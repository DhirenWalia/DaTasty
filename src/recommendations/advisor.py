class RecommendationEngine:

    def __init__(
        self,
        missing_report,
        duplicate_report,
        validity_report,
        consistency_report,
        accuracy_report
    ):

        self.missing_report = missing_report
        self.duplicate_report = duplicate_report
        self.validity_report = validity_report
        self.consistency_report = consistency_report
        self.accuracy_report = accuracy_report


    def generate_recommendations(self):

        recommendations = []

        recommendations.extend(
            self.missing_recommendations()
        )

        recommendations.extend(
            self.duplicate_recommendations()
        )

        recommendations.extend(
            self.validity_recommendations()
        )

        recommendations.extend(
            self.consistency_recommendations()
        )

        recommendations.extend(
            self.accuracy_recommendations()
        )

        return recommendations


    def create_entry(
        self,
        issue,
        impact,
        recommendation,
        priority
    ):

        return {
            "Issue": issue,
            "Business Impact": impact,
            "Recommendation": recommendation,
            "Priority": priority
        }


    def missing_recommendations(self):

        results = []

        for item in self.missing_report:

            if item["Missing Percentage"] > 0:

                results.append(
                    self.create_entry(
                        issue=f"{item['Column']} has {item['Missing Percentage']}% missing values.",
                        
                        impact="Incomplete information may reduce the quality of analytics and AI predictions.",
                        
                        recommendation="Collect missing data or apply suitable imputation techniques.",
                        
                        priority=item["Severity"]
                    )
                )

        return results


    def duplicate_recommendations(self):

        results = []

        if self.duplicate_report["Duplicate Records"] > 0:

            results.append(
                self.create_entry(
                    issue=f"{self.duplicate_report['Duplicate Records']} duplicate records detected.",
                    
                    impact="Duplicate records can inflate business metrics and bias AI training datasets.",
                    
                    recommendation="Review duplicate entries and remove unnecessary repeated records.",
                    
                    priority=self.duplicate_report["Severity"]
                )
            )

        return results


    def validity_recommendations(self):

        results = []

        for item in self.validity_report:

            if item["Invalid Count"] > 0:

                results.append(
                    self.create_entry(
                        issue=f"{item['Column']} contains {item['Invalid Count']} invalid records.",
                        
                        impact="Incorrect values can lead to unreliable analysis and inaccurate decision making.",
                        
                        recommendation="Apply validation rules and correct invalid values.",
                        
                        priority=item["Severity"]
                    )
                )

        return results


    def consistency_recommendations(self):

        results = []

        for item in self.consistency_report:

            if item["Affected Records"] > 0:

                results.append(
                    self.create_entry(
                        issue=f"{item['Column']} contains inconsistent formatting.",
                        
                        impact="Inconsistent formatting may create duplicate categories and inaccurate reporting.",
                        
                        recommendation="Standardize text, date, and categorical formats.",
                        
                        priority=item["Severity"]
                    )
                )

        return results


    def accuracy_recommendations(self):

        results = []

        for item in self.accuracy_report:

            if item["Outlier Count"] > 0:

                results.append(
                    self.create_entry(
                        issue=f"{item['Column']} contains {item['Outlier Count']} unusual values.",
                        
                        impact="Extreme values may indicate entry errors and can distort statistical models.",
                        
                        recommendation="Investigate outliers and confirm whether they represent real business cases.",
                        
                        priority=item["Severity"]
                    )
                )

        return results