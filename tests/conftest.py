import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from tests.test_data import TestData


@pytest.fixture
def burger():
    """Фикстура для создания пустого бургера."""
    return Burger()


@pytest.fixture
def mock_bun():
    """Фикстура для создания мок-объекта булочки."""
    bun = Mock(spec=Bun)
    bun.get_name.return_value = TestData.BUN_NAME
    bun.get_price.return_value = TestData.BUN_PRICE
    return bun


@pytest.fixture
def mock_ingredient_sauce():
    """Фикстура для создания мок-объекта ингредиента типа 'соус'."""
    ingredient = Mock(spec=Ingredient)
    ingredient.get_type.return_value = TestData.INGREDIENT_SAUCE_TYPE
    ingredient.get_name.return_value = TestData.INGREDIENT_SAUCE_NAME
    ingredient.get_price.return_value = TestData.INGREDIENT_SAUCE_PRICE
    return ingredient


@pytest.fixture
def mock_ingredient_filling():
    """Фикстура для создания мок-объекта ингредиента типа 'начинка'."""
    ingredient = Mock(spec=Ingredient)
    ingredient.get_type.return_value = TestData.INGREDIENT_FILLING_TYPE
    ingredient.get_name.return_value = TestData.INGREDIENT_FILLING_NAME
    ingredient.get_price.return_value = TestData.INGREDIENT_FILLING_PRICE
    return ingredient


@pytest.fixture
def burger_with_bun(burger, mock_bun):
    """Фикстура для создания бургера с установленной булочкой."""
    burger.set_buns(mock_bun)
    return burger


@pytest.fixture
def burger_with_ingredients(burger, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
    """Фикстура для создания полностью собранного бургера."""
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient_sauce)
    burger.add_ingredient(mock_ingredient_filling)
    return burger
    