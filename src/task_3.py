from .pseudocode import DataLoader, ModelRunner, ReportGenerator


def main():
    # Set up the necessary configurations and paths
    wsi_dir = "path/to/wsi/directory"
    patch_size = (512, 512)
    classification_results_path = "path/to/classification/results.csv"
    report_output_path = "output.md"

    # Initialize the required objects
    data_loader = DataLoader(wsi_dir)
    segmentation_model = None  # Initialize your segmentation model here
    classification_model = None  # Initialize your classification model here
    model_runner = ModelRunner(segmentation_model, classification_model)
    olama_model = None  # Initialize your OLAMA model here
    report_generator = ReportGenerator(olama_model)

    # Step 1: Load WSI images
    wsi_paths = data_loader.get_wsi_paths()

    for wsi_path in wsi_paths:
        # Step 2: Load each WSI image
        wsi = data_loader.load_wsi(wsi_path)

        # Step 3: Extract patches from the WSI image
        patches = data_loader.extract_patches(wsi, patch_size)

        # Step 4: Perform segmentation on all patches
        segmentations = model_runner.run_segmentation(patches)

        # Step 5: Perform classification on all detected segmentations
        classification_results = model_runner.run_classification(segmentations)

        # Step 6: Save the classification results to CSV
        data_loader.save_classification_results(classification_results, classification_results_path)

    # Step 7: Load the classification results from CSV and obtain case/control data
    classification_results_df = data_loader.load_classification_results(classification_results_path)

    # Step 8: Run statistical tests on the classification results
    statistical_results = report_generator.run_statistical_tests(classification_results_df)

    # Step 9: Generate the report based on the statistical results
    report = report_generator.generate_report(statistical_results)

    # Step 10: Save the generated report to a file
    with open(report_output_path, "w") as file:
        file.write(report)

    print("Pipeline execution completed.")
