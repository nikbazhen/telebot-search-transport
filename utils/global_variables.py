class GlobalVariables:
    """Класс заменяющий функцию global, хранящий в себе разные типы переменных, кроме булевых"""
    glob_dict_station = None
    switch_start_and_stop = None
    count = None
    page = None
    current_page = 1
    stations = None
    answer_transport = None
    custom_filt = None
    date_for_db = None
    resul_for_db = None
    start_for_db = None
    stop_for_db = None
    transport_for_db = None
    date_search_for_db = None
    search_parameter_for_db = None
    latitude = None
    longitude = None
    id_chat_for_errors = None
