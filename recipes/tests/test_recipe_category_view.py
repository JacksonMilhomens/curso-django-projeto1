from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
# Para pular algum teste, importar skip ou utilizar o self.fail() para fazer o teste falhar  # noqa


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
            )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipe(self):
        needed_title = 'This is a category test'

        # Need a recipe for this test
        recipe = self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id})  # noqa
        )
        response_content = response.content.decode('utf-8')

        self.assertIn(needed_title, response_content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id})  # noqa
        )

        self.assertEqual(response.status_code, 404)
