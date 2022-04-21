from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
# Para pular algum teste, importar skip ou utilizar o self.fail() para fazer o teste falhar  # noqa


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=testing')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            reverse('recipes:search') + '?q=<test>'
        )
        self.assertIn(
            'Search for &quot;&lt;test&gt;&quot;',
            response.content.decode('utf-8'),
        )
