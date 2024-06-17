class ReportGenerator:
    def __init__(self, olama_model):
        """
        Initialize the ReportGenerator class.

        This class is responsible for running statistical tests on the classification results and generating
        a report using the OLAMA model based on the statistical results.

        Args:
            olama_model: OLAMA model object for generating reports.
        """
        pass

    def run_statistical_tests(self, classification_results):
        """
        Run statistical tests on the classification results.

        This function performs statistical tests (e.g., p-tests) on the classification results to evaluate
        the accuracy and significance of the treatment. It compares the case and control groups.

        Args:
            classification_results (pandas.DataFrame): DataFrame containing the classification results
                and case/control information.

        Returns:
            dict: Dictionary containing the results of the statistical tests.
        """
        pass

    def generate_report(self, statistical_results):
        """
        Generate a report based on the statistical results.

        This function uses the OLAMA model (e.g., LAMA-3-8B instruct) to generate a Markdown report
        based on the statistical results. The report includes aggregate metrics and the results of the
        p-tests. If low p-values are observed, the report explains why the treatment has statistical
        significance. If the treatment has no statistical significance, the report explains why it
        doesn't work.

        Args:
            statistical_results (dict): Dictionary containing the results of the statistical tests.

        Returns:
            str: Generated report in Markdown format.
        """
        return "These findings show that ..."
