import os


def get_resource_directory() -> str:
    """
    Returns the path of the resources directory so that solutions can read their inputs
    :return:
    """
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir_path, '../../resources')


def get_resource(resource_name: str) -> str:
    """
    Given some file name, this function will return the full path of that resource
    :param resource_name:
    :return:
    """
    return os.path.join(get_resource_directory(), resource_name)
