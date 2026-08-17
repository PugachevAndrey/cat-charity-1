# HTTP статусы
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404

# Сообщения об ошибках
ERROR_PROJECT_NAME_EXISTS = "Проект с таким именем уже существует"
ERROR_PROJECT_NOT_FOUND = "Проект не найден"
ERROR_PROJECT_CLOSED = "Закрытый проект нельзя редактировать"
ERROR_DONATION_NOT_FOUND = "Пожертвование не найдено"
ERROR_PROJECT_HAS_INVESTMENTS = (
    "Нельзя удалить проект, в который уже инвестировали"
)
ERROR_FULL_AMOUNT_LESS_THAN_INVESTED = (
    "Нельзя установить требуемую сумму "
    "меньше уже внесённой"
)