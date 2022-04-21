from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
# Para pular algum teste, importar skip ou utilizar o self.fail() para fazer o teste falhar  # noqa


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipes_found_if_no_have_recipes(self):  # noqa
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 😭</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipe(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', response_content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if exists recipes
        self.assertIn(
            '<h1>No recipes found here 😭</h1>',
            response.content.decode('utf-8'),
        )
