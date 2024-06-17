from difflib import SequenceMatcher
from typing import List, Tuple
import pandas as pd
import os


def similarity_ratio(a: str, b: str) -> float:
    """
    Calculates the similarity ratio between two strings.

    Args:
        a (str): First string.
        b (str): Second string.

    Returns:
        float: Similarity ratio between the two strings.
    """
    return SequenceMatcher(None, a, b).ratio()


def find_similar_names(missing_names: List[str], reference_names: List[str], first: bool = False) -> List[Tuple[str, str]]:
    """
    Finds similar names between missing names and reference names.

    Args:
        missing_names (List[str]): List of missing names.
        reference_names (List[str]): List of reference names.
        first (bool): Flag to determine the order of the matched names in the output tuple. Default is False.

    Returns:
        List[Tuple[str, str]]: List of tuples containing matched names.
    """
    matches = []
    for missing_name in missing_names:
        similar_names = [ref_name for ref_name in reference_names if similarity_ratio(missing_name, ref_name) > 0.5]

        assert len(similar_names) == 1, f"Too many matches for {missing_name}: {similar_names}"

        matches.append((missing_name, similar_names[0]) if first else (similar_names[0], missing_name))
    return matches


def load_data(metadata_path: str, cell_data_path: str) -> pd.DataFrame:
    """
    Loads and merges metadata and cell data from CSV files.

    Args:
        metadata_path (str): Path to the metadata CSV file.
        cell_data_path (str): Path to the directory containing cell data CSV files.

    Returns:
        pd.DataFrame: Merged DataFrame containing cell data and metadata.
    """
    metadata = pd.read_csv(metadata_path)

    cell_data = []
    for file in os.listdir(cell_data_path):
        file_path = os.path.join(cell_data_path, file)
        df = pd.read_csv(file_path)
        df["name"] = file.strip(".csv")
        cell_data.append(df)

    cell_data = pd.concat(cell_data)

    cell_data_names = set(cell_data["name"])
    metadata_names = set(metadata["name"])

    missing_in_metadata = sorted(cell_data_names - metadata_names)
    missing_in_cell_data = sorted(metadata_names - cell_data_names)

    matches_cell_data = find_similar_names(missing_in_cell_data, cell_data_names, True)
    matches_metadata = find_similar_names(missing_in_metadata, metadata_names, False)

    matches = sorted(set(matches_metadata + matches_cell_data))

    assert len(matches_metadata) == len(matches_cell_data) == len(matches)

    mapping = dict(matches)
    metadata["name"] = metadata["name"].map(mapping).fillna(metadata["name"])

    data = pd.merge(cell_data, metadata, on="name")

    return data


def extract_feature_from_group(df: pd.DataFrame) -> pd.Series:
    """
    Extracts features from a group of data.

    Args:
        df (pd.DataFrame): DataFrame containing cell data for a group.

    Returns:
        pd.Series: Series containing extracted features.
    """
    total_cells = len(df)
    malignant_cells = (df["label"] == "malignant").sum()
    normal_cells = (df["label"] == "normal").sum()
    malignant_ratio = malignant_cells / total_cells
    return pd.Series(
        {"total_cells": total_cells, "malignant_cells": malignant_cells, "normal_cells": normal_cells, "malignant_ratio": malignant_ratio}
    )


def extract_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts features from the merged data.

    Args:
        data (pd.DataFrame): Merged DataFrame containing cell data and metadata.

    Returns:
        pd.DataFrame: DataFrame containing extracted features.
    """
    features = data.groupby(["patient_id", "arm", "treatment"], as_index=False).apply(extract_feature_from_group)
    features = features.sort_values(by="patient_id")
    return features


def prepare_pre_post_treatment_data(features: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares pre and post treatment data by merging and calculating change in malignant ratio.

    Args:
        features (pd.DataFrame): DataFrame containing extracted features.

    Returns:
        pd.DataFrame: DataFrame containing pre and post treatment data.
    """
    pre_treatment = features[features["treatment"] == "pre"]
    post_treatment = features[features["treatment"] == "post"]

    pre_post_data = pd.merge(pre_treatment, post_treatment, on=["patient_id", "arm"], suffixes=("_pre", "_post"))
    pre_post_data["change_in_malignant_ratio"] = pre_post_data["malignant_ratio_pre"] - pre_post_data["malignant_ratio_post"]
    pre_post_data = pre_post_data.sort_values(by="patient_id")

    return pre_post_data


def get_control_case_groups(pre_post_data: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Retrieves control and case groups from the pre and post treatment data.

    Args:
        pre_post_data (pd.DataFrame): DataFrame containing pre and post treatment data.

    Returns:
        Tuple[pd.Series, pd.Series]: Tuple containing case group and control group data.
    """
    case_group = pre_post_data[pre_post_data["arm"] == "case"]["change_in_malignant_ratio"]
    control_group = pre_post_data[pre_post_data["arm"] == "control"]["change_in_malignant_ratio"]

    return case_group, control_group
