from pathlib import Path


def get_path_to_data():
    """return path to data"""
    return Path("data/")


def get_raw_data_path():
    """return path to raw data"""
    return get_path_to_data() / "raw_data"


def get_tidy_data_path():
    """return path to tidy data"""
    return get_path_to_data() / "tidy_data"


def get_cleaned_data_path():
    """return path to cleaned data"""
    return get_path_to_data() / "cleaned_data"


def get_result_data_path():
    """return path to result data"""
    return get_path_to_data() / "result_data"
