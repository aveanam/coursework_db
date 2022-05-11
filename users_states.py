from aiogram.dispatcher.filters.state import StatesGroup, State

# Для состояний
class users_states(StatesGroup):

    name = State()  # Состояние для получение данных из мед.карты
    new_pat = State()  # Состояние для внесения нового пациента

    # Создание нового пациента
    new_pat_name = State()
    new_pat_years = State()
    new_pat_cities = State()
    new_pat_phone = State()

    # Для получение врачей нужной специальности
    get_doc_spec = State()

    # Для записи к доктору
    get_new_visit_state = State()
    add_new_visit_w_id_pat = State()

    # Для получения расшифровки болезни
    get_info_M10 = State()

