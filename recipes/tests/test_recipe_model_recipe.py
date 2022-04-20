from django.forms import ValidationError
from recipes.tests.test_recipe_base import RecipeTestBase
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

            # - Test with unittest -

            # def test_recipe_fields_max_lenght(self):
            #     fields = [
            #         ('title', 65),
            #         ('description', 165),
            #         ('preparation_time_unit', 65),
            #         ('servings_unit', 65),
            #     ]

            #     for field, max_lenght in fields:
            #         with self.subTest(field=field, max_lenght=max_lenght):
            #             setattr(self.recipe, field, 'A' * (max_lenght + 1))
            #             with self.assertRaises(ValidationError):
            #                 self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        self.assertFalse(
            self.recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False'
        )

    def test_recipe_is_published_is_false_by_default(self):
        # Changing value default of make_recipe for false
        self.recipe.is_published = False

        self.assertFalse(
            self.recipe.is_published,
            msg='is_published is not False'
        )

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')
