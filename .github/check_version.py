import requests
import pkg_resources


PKG_NAME = 'jskiner'
IMPORT_NAME = 'jskiner'


def get_all_versions() -> str:
    """
    Gets the latest pip version number from the pypi server.
    Returns: (str) the version of the latest pip module
    """
    req = requests.get(f"https://pypi.org/pypi/{PKG_NAME}/json")
    return list(req.json()["releases"].keys())


if __name__ == '__main__':
    my_version = pkg_resources.get_distribution('jskiner').version
    online_versions = get_all_versions()
    assert my_version not in online_versions, "This version already uploaded!"
