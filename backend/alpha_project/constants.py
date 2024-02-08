SEC_BEFORE_NEXT_REQUEST = 86400
URL = "https://new.red-hand.ru"
REGEX_TEL = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
MAX_NAME_CHARACTERS = 150
MAX_EMAIL_CHARACTERS = 254
MAX_DEPTH = 5
HARD_SKILLS = [
    "Структуры данных и алгоритмы",
    "Инфраструктура разработки",
    "Аналитическое мышление",
    "Высшая математика",
]
SOFT_SKILLS = [
    "Наставничество",
    "Работа в коллективе",
    "Коммуникабельность",
    "Аналитическое мышление",
    "Личная эффективность",
]
MAX_LENGTH_COMMENT = 200
MAX_LENGTH_STATUS = 20
MAX_LENGTH_TITLE = 256
HTML_TASK_STATUS_MESSAGE = (
    '<p>У вас изменился статус задачи {task_name}. <a href="'
    '{URL}/employee/idp/{idp_id}/tasks">ИПР с этой задачей</a>'
)
HTML_DIRECTOR_MESSAGE = (
    "<p>Сотрудник пометил задачу {task_name} как "
    'выполненную. <a href="{URL}/head/staff/{user_id}'
    '/{idp_id}/tasks">ИПР с задачей</a></p>'
)
HTML_NEW_TASK_MESSAGE = (
    '<p>У вас новая задача. <a href="{URL}/employee/idp/'
    '{idp_id}/tasks">ИПР с новой задачей</a>'
)
HTML_NEW_IDP_MESSAGE = (
    '<p>Вам назначено ИПР <a href="{URL}' '/employee/idp/{idp_id}/tasks">{title}</a>.'
)
