class ModelRunner:
    def __init__(self, segmentation_model, classification_model):
        """
        Initialize the ModelRunner class.

        This class is responsible for running the segmentation and classification models on the patches
        and segmentations, respectively.

        Args:
            segmentation_model: Segmentation model object.
            classification_model: Classification model object.
        """
        pass

    def run_segmentation(self, patches):
        """
        Run segmentation on the patches.

        This function applies the segmentation model to each patch in the provided list of patches.
        It returns the segmentation results for each patch.

        Args:
            patches (list): List of patches to perform segmentation on.

        Returns:
            list: List of segmentation results.
        """
        pass

    def run_classification(self, segmentations):
        """
        Run classification on the segmentations.

        This function applies the classification model to each segmentation in the provided list of
        segmentations. It returns the classification results for each segmentation.

        Args:
            segmentations (list): List of segmentations to perform classification on.

        Returns:
            list: List of classification results.
        """
        pass
