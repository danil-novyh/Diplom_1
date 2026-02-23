"""
Тестовые данные для проверки класса Burger.
Централизованное хранение всех констант и ожидаемых значений.
"""
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestData:
    """Класс с константами для тестирования."""
    
    # Данные для булочки
    BUN_NAME = "Краторная булка N-200i"
    BUN_PRICE = 100.0
    
    # Данные для ингредиента: соус
    INGREDIENT_SAUCE_TYPE = INGREDIENT_TYPE_SAUCE
    INGREDIENT_SAUCE_NAME = "Соус Spicy-X"
    INGREDIENT_SAUCE_PRICE = 50.0
    
    # Данные для ингредиента: начинка
    INGREDIENT_FILLING_TYPE = INGREDIENT_TYPE_FILLING
    INGREDIENT_FILLING_NAME = "Котлета из марсианской Магнолии"
    INGREDIENT_FILLING_PRICE = 150.0
    
    # Ожидаемые результаты
    EXPECTED_PRICE_WITH_BUN_AND_TWO_INGREDIENTS = 400.0  # (100*2) + 50 + 150
    EXPECTED_PRICE_WITH_BUN_ONLY = 200.0  # 100*2


class ErrorMessages:
    """Класс с сообщениями об ошибках для негативных тестов."""
    INDEX_OUT_OF_RANGE = "list index out of range"
    LIST_ASSIGNMENT_INDEX_OUT_OF_RANGE = "list assignment index out of range"
    