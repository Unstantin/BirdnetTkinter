from Screens import Screens


class Data:
    root = None
    token = None
    CURRENT_SCREEN = Screens.AUTH
    BASE_URL = "http://127.0.0.1:3000/api/"
    interface = None

    observations = None
    profile_info = None
    current_observation = None
    current_identifications = None
    taxons = None
    taxons_names = dict()
