import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from tests.test_data import TestData, ErrorMessages


class TestBurgerSetBuns:
    """Тесты для метода set_buns."""
    
    def test_set_buns_success(self, burger, mock_bun):
        """Проверка успешной установки булочки."""
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun
    
    def test_set_buns_replaces_existing_bun(self, burger, mock_bun):
        """Проверка замены существующей булочки на новую."""
        old_bun = Mock(spec=Bun)
        burger.set_buns(old_bun)
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun
        assert burger.bun != old_bun


class TestBurgerAddIngredient:
    """Тесты для метода add_ingredient."""
    
    def test_add_ingredient_to_empty_burger(self, burger, mock_ingredient_sauce):
        """Проверка добавления ингредиента в пустой бургер."""
        burger.add_ingredient(mock_ingredient_sauce)
        
        assert mock_ingredient_sauce in burger.ingredients
    
    def test_add_ingredient_increases_list_length(self, burger, mock_ingredient_sauce):
        """Проверка увеличения длины списка ингредиентов."""
        initial_length = len(burger.ingredients)
        burger.add_ingredient(mock_ingredient_sauce)
        
        assert len(burger.ingredients) == initial_length + 1
    
    def test_add_multiple_ingredients_preserves_order(
        self, burger, mock_ingredient_sauce, mock_ingredient_filling
    ):
        """Проверка сохранения порядка при добавлении нескольких ингредиентов."""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        
        assert burger.ingredients[0] == mock_ingredient_sauce
        assert burger.ingredients[1] == mock_ingredient_filling


class TestBurgerRemoveIngredient:
    """Тесты для метода remove_ingredient."""
    
    def test_remove_ingredient_by_valid_index(self, burger_with_ingredients):
        """Проверка удаления ингредиента по корректному индексу."""
        ingredient_to_remove = burger_with_ingredients.ingredients[0]
        burger_with_ingredients.remove_ingredient(0)
        
        assert ingredient_to_remove not in burger_with_ingredients.ingredients
    
    def test_remove_ingredient_decreases_list_length(self, burger_with_ingredients):
        """Проверка уменьшения длины списка после удаления."""
        initial_length = len(burger_with_ingredients.ingredients)
        burger_with_ingredients.remove_ingredient(0)
        
        assert len(burger_with_ingredients.ingredients) == initial_length - 1
    
    def test_remove_ingredient_preserves_remaining_ingredients(
        self, burger, mock_ingredient_sauce, mock_ingredient_filling
    ):
        """Проверка сохранения оставшихся ингредиентов после удаления."""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        burger.remove_ingredient(0)
        
        assert mock_ingredient_filling in burger.ingredients
    
    def test_remove_ingredient_with_negative_index_raises_error(self, burger_with_ingredients):
        """Проверка обработки отрицательного индекса (негативный тест)."""

        burger_with_ingredients.remove_ingredient(-1)
        
        assert len(burger_with_ingredients.ingredients) == 1
    
    def test_remove_ingredient_with_invalid_index_raises_error(self, burger):
        """Проверка выброса исключения при невалидном индексе."""
        with pytest.raises(IndexError):
            burger.remove_ingredient(999)


class TestBurgerMoveIngredient:
    """Тесты для метода move_ingredient."""
    
    def test_move_ingredient_changes_position(self, burger_with_ingredients):
        """Проверка изменения позиции ингредиента."""
        first_ingredient = burger_with_ingredients.ingredients[0]
        second_ingredient = burger_with_ingredients.ingredients[1]
        
        burger_with_ingredients.move_ingredient(0, 1)
        
        assert burger_with_ingredients.ingredients[0] == second_ingredient
        assert burger_with_ingredients.ingredients[1] == first_ingredient
    
    def test_move_ingredient_to_same_position(self, burger_with_ingredients):
        """Проверка перемещения ингредиента на ту же позицию."""
        original_order = burger_with_ingredients.ingredients.copy()
        burger_with_ingredients.move_ingredient(0, 0)
        
        assert burger_with_ingredients.ingredients == original_order
    
    def test_move_ingredient_preserves_list_length(self, burger_with_ingredients):
        """Проверка сохранения длины списка при перемещении."""
        initial_length = len(burger_with_ingredients.ingredients)
        burger_with_ingredients.move_ingredient(0, 1)
        
        assert len(burger_with_ingredients.ingredients) == initial_length
    
    @pytest.mark.parametrize(
        "from_index, to_index",
        [
            (0, 2),  # Перемещение вперед
            (2, 0),  # Перемещение назад
            (1, 1),  # На ту же позицию
        ],
        ids=["move_forward", "move_backward", "same_position"]
    )
    def test_move_ingredient_various_positions(self, burger, from_index, to_index):
        """Параметризованный тест перемещения ингредиентов."""
        # Создаем 3 разных ингредиента
        ingredients = [Mock(spec=Ingredient) for _ in range(3)]
        for ing in ingredients:
            burger.add_ingredient(ing)
        
        moved_ingredient = burger.ingredients[from_index]
        burger.move_ingredient(from_index, to_index)
        
        assert burger.ingredients[to_index] == moved_ingredient
    
    def test_move_ingredient_with_invalid_from_index_raises_error(self, burger_with_ingredients):
        """Проверка выброса исключения при невалидном исходном индексе."""
        with pytest.raises(IndexError):
            burger_with_ingredients.move_ingredient(999, 0)
    
    def test_move_ingredient_with_invalid_to_index_raises_error(self, burger_with_ingredients):
        """Проверка выброса исключения при невалидном целевом индексе."""
        burger_with_ingredients.move_ingredient(0, 999)

        assert len(burger_with_ingredients.ingredients) == 2


class TestBurgerGetPrice:
    """Тесты для метода get_price."""
    
    def test_get_price_with_bun_only(self, burger_with_bun):
        """Проверка расчета цены бургера только с булочкой."""
        expected_price = TestData.BUN_PRICE * 2
        
        assert burger_with_bun.get_price() == expected_price
    
    def test_get_price_with_bun_and_ingredients(self, burger_with_ingredients):
        """Проверка расчета цены бургера с булочкой и ингредиентами."""
        expected_price = (
            TestData.BUN_PRICE * 2 +
            TestData.INGREDIENT_SAUCE_PRICE +
            TestData.INGREDIENT_FILLING_PRICE
        )
        
        assert burger_with_ingredients.get_price() == expected_price
    
    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_total",
        [
            (100, [], 200),  # Только булочки
            (100, [50], 250),  # Булочки + 1 ингредиент
            (100, [50, 150], 400),  # Булочки + 2 ингредиента
            (100, [50, 150, 200], 600),  # Булочки + 3 ингредиента
            (0, [100, 200], 300),  # Бесплатные булочки
        ],
        ids=[
            "only_buns",
            "buns_and_one_ingredient",
            "buns_and_two_ingredients",
            "buns_and_three_ingredients",
            "free_buns"
        ]
    )
    def test_get_price_parametrized(self, burger, bun_price, ingredient_prices, expected_total):
        """Параметризованный тест расчета цены с разными комбинациями."""
        # Настройка булочки
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        # Добавление ингредиентов
        for price in ingredient_prices:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        
        assert burger.get_price() == expected_total
    
    def test_get_price_calls_bun_get_price_twice(self, burger, mock_bun):
        """Проверка двукратного вызова метода get_price для булочки."""
        burger.set_buns(mock_bun)
        burger.get_price()
        
        assert mock_bun.get_price.call_count == 1
    
    def test_get_price_calls_ingredient_get_price_for_each(
        self, burger, mock_bun, mock_ingredient_sauce, mock_ingredient_filling
    ):
        """Проверка вызова get_price для каждого ингредиента."""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        
        burger.get_price()
        
        mock_ingredient_sauce.get_price.assert_called_once()
        mock_ingredient_filling.get_price.assert_called_once()


class TestBurgerGetReceipt:
    """Тесты для метода get_receipt."""
    
    def test_get_receipt_with_bun_only(self, burger_with_bun):
        """Проверка генерации чека для бургера только с булочкой."""
        expected_receipt = (
            f"(==== {TestData.BUN_NAME} ====)\n"
            f"(==== {TestData.BUN_NAME} ====)\n\n"
            f"Price: {TestData.BUN_PRICE * 2}"
        )
        
        assert burger_with_bun.get_receipt() == expected_receipt
    
    def test_get_receipt_with_bun_and_ingredients(self, burger_with_ingredients):
        """Проверка генерации чека для полного бургера."""
        expected_receipt = (
            f"(==== {TestData.BUN_NAME} ====)\n"
            f"= {TestData.INGREDIENT_SAUCE_TYPE.lower()} {TestData.INGREDIENT_SAUCE_NAME} =\n"
            f"= {TestData.INGREDIENT_FILLING_TYPE.lower()} {TestData.INGREDIENT_FILLING_NAME} =\n"
            f"(==== {TestData.BUN_NAME} ====)\n\n"
            f"Price: {TestData.EXPECTED_PRICE_WITH_BUN_AND_TWO_INGREDIENTS}"
        )
        
        assert burger_with_ingredients.get_receipt() == expected_receipt
    
    def test_get_receipt_contains_bun_name_twice(self, burger_with_bun):
        """Проверка наличия имени булочки дважды в чеке."""
        receipt = burger_with_bun.get_receipt()
        
        assert receipt.count(TestData.BUN_NAME) == 2
    
    def test_get_receipt_ingredient_type_is_lowercase(self, burger_with_ingredients):
        """Проверка, что тип ингредиента в нижнем регистре."""
        receipt = burger_with_ingredients.get_receipt()
        
        assert TestData.INGREDIENT_SAUCE_TYPE.lower() in receipt
        assert TestData.INGREDIENT_FILLING_TYPE.lower() in receipt
    
    def test_get_receipt_contains_price_at_end(self, burger_with_ingredients):
        """Проверка наличия цены в конце чека."""
        receipt = burger_with_ingredients.get_receipt()
        
        assert receipt.endswith(f"Price: {TestData.EXPECTED_PRICE_WITH_BUN_AND_TWO_INGREDIENTS}")
    
    def test_get_receipt_calls_bun_get_name(self, burger, mock_bun):
        """Проверка вызова метода get_name для булочки."""
        burger.set_buns(mock_bun)
        burger.get_receipt()
        
        assert mock_bun.get_name.call_count >= 2
    
    def test_get_receipt_calls_ingredient_methods(
        self, burger, mock_bun, mock_ingredient_sauce
    ):
        """Проверка вызова методов ингредиента при генерации чека."""
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient_sauce)
        
        burger.get_receipt()
        
        mock_ingredient_sauce.get_type.assert_called()
        mock_ingredient_sauce.get_name.assert_called()
    
    def test_get_receipt_format_structure(self, burger_with_ingredients):
        """Проверка структуры формата чека."""
        receipt = burger_with_ingredients.get_receipt()
        lines = receipt.split('\n')
        
        # Проверяем структуру: верхняя булочка, ингредиенты, нижняя булочка, пустая строка, цена
        assert lines[0].startswith("(====")
        assert lines[-1].startswith("Price:")
        assert lines[-2] == ""  # Пустая строка перед ценой


class TestBurgerEdgeCases:
    """Тесты для граничных случаев и особых сценариев."""
    
    def test_burger_initialization_creates_empty_lists(self):
        """Проверка инициализации бургера с пустыми списками."""
        burger = Burger()
        
        assert burger.bun is None
        assert burger.ingredients == []
        assert isinstance(burger.ingredients, list)
    
    def test_burger_with_many_ingredients(self, burger, mock_bun):
        """Проверка работы с большим количеством ингредиентов."""
        burger.set_buns(mock_bun)
        
        # Добавляем 10 ингредиентов
        for i in range(10):
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_price.return_value = 10 * (i + 1)
            mock_ingredient.get_name.return_value = f"ingredient_{i}"
            mock_ingredient.get_type.return_value = "FILLING"
            burger.add_ingredient(mock_ingredient)
        
        assert len(burger.ingredients) == 10
        assert burger.get_price() == (TestData.BUN_PRICE * 2) + sum(10 * (i + 1) for i in range(10))
    
    def test_burger_remove_all_ingredients(self, burger_with_ingredients):
        """Проверка удаления всех ингредиентов."""
        initial_count = len(burger_with_ingredients.ingredients)
        
        for _ in range(initial_count):
            burger_with_ingredients.remove_ingredient(0)
        
        assert len(burger_with_ingredients.ingredients) == 0
    
    def test_burger_move_ingredient_in_single_item_list(self, burger, mock_ingredient_sauce):
        """Проверка перемещения единственного ингредиента."""
        burger.add_ingredient(mock_ingredient_sauce)
        burger.move_ingredient(0, 0)
        
        assert burger.ingredients[0] == mock_ingredient_sauce


class TestBurgerIntegration:
    """Интеграционные тесты для проверки взаимодействия методов."""
    
    def test_full_burger_workflow(self, burger, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
        """Проверка полного сценария работы с бургером."""
        # Шаг 1: Устанавливаем булочку
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
        
        # Шаг 2: Добавляем ингредиенты
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)
        assert len(burger.ingredients) == 2
        
        # Шаг 3: Перемещаем ингредиент
        burger.move_ingredient(0, 1)
        assert burger.ingredients[0] == mock_ingredient_filling
        
        # Шаг 4: Удаляем ингредиент
        burger.remove_ingredient(1)
        assert len(burger.ingredients) == 1
        
        # Шаг 5: Проверяем цену
        expected_price = TestData.BUN_PRICE * 2 + TestData.INGREDIENT_FILLING_PRICE
        assert burger.get_price() == expected_price
        
        # Шаг 6: Генерируем чек
        receipt = burger.get_receipt()
        assert TestData.BUN_NAME in receipt
        assert str(expected_price) in receipt
