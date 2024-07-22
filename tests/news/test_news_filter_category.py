from playwright.sync_api import Page
from pages.portal.news.filter import FilterModal
from pages.portal.news.news_page import NewsPage
import allure

@allure.title("Filter by 1 category without subcategories")
@allure.description("The test checks that the filter by category (without subcategories) is applied correctly.")
def test_filter_by_single_category_without_subcategories(page: Page):

   category_filter = "Health" # Set the category (without subcategories) by which the filtering will be performed.
   
   news_page = NewsPage(page)
   filter_modal = FilterModal(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_categories(category_filter)
   filter_modal.apply_filter()
   
   # Collect the names of news categories after applying the filter
   category_names = news_page.collect_category_names()
   
   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the selected category
   assert all(name.lower() == category_filter.lower() for name in category_names), f"{category_names} != {category_filter}" 
   
@allure.title("Filter by category with subcategory")
@allure.description("The test checks that the filter by category (with subcategory) is applied correctly")
def test_filter_by_category_including_subcategories(page: Page):

   category_filter = 'Emergency shutdowns'
   
   news_page = NewsPage(page)
   filter_modal = FilterModal(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_categories(category_filter)
   filter_modal.apply_filter()
   
   # Collect the names of news categories after applying the filter
   category_names = news_page.collect_category_names()
   
   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the selected category
   assert all(name.lower() == category_filter.lower() for name in category_names), f"{category_names} != {category_filter}" 
   
@allure.title("Filter by multiple categories without subcategories")
@allure.description("The test checks that the filter on multiple categories (without subcategories) is applied correctly")
def test_filter_by_multiple_categories_without_subcategories(page: Page):
   
   category_filter = ["Health", "Information"]
   
   news_page = NewsPage(page)
   filter_modal = FilterModal(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_categories(category_filter[0], category_filter[1])
   filter_modal.apply_filter()
   
   # Collect the names of news categories after applying the filter
   category_names = news_page.collect_category_names()
   
   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the selected categories
   assert all(name.lower() in (filter_name.lower() for filter_name in category_filter)
         for name in category_names), f"{category_names} != {category_filter}"
   
@allure.title("Filter by subcategory")
@allure.description("The test checks that the subcategory filter is applied correctly. When sending a request, the value of the ‘group’ parameter matches the categories")
def test_filter_by_subcategory(page: Page):

   # In case of checking the filter by another parent category, 
   # the order of the selected subcategory item should be changed (0 - subcategory in Emergency Shutdowns, 1 - in Scheduled Shutdowns), 
   # as there is currently no way to select a subcategory depending on the parent category
   parent_category = 'Emergency shutdowns' # Set a category that contains a subcategory (Expected category name in the news)
   category_filter = ('Electricity supply', 0) # Set the subcategory to filter by
   group_value = '536' # Set the expected value of the corresponding subcategory of the parameter ‘group’, which is reflected in the query
   
   news_page = NewsPage(page)
   filter_modal = FilterModal(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_categories(category_filter)
   filter_modal.apply_filter()
   
   # Write the value of the ‘group’ parameter that is sent in the query when the filter is applied
   actual_group_values = filter_modal.group_values
   # Collect the names of news categories after applying the filter
   category_names = news_page.collect_category_names()

   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the parent category
   assert all(name.lower() == parent_category.lower() for name in category_names), f"{category_names} != {parent_category}" 
   # Check that there is only one ‘group’ value in the query and that it matches the given group_value
   assert actual_group_values == [group_value]
   
@allure.title("Filter across multiple subcategories in different categories")
@allure.description("The test checks that the subcategory filter is applied correctly. When sending a request, the value of the ‘group’ parameter matches the categories")
def test_filter_by_several_subcategories(page: Page):

   parent_category = ['Emergency shutdowns', 'Scheduled shutdowns'] # Set categories that contain a subcategory (Expected category name in the news)
   category_filter = [('Electricity supply', 0), ('Electricity supply', 1)] # Specify the subcategories by which the filter will be applied (0 - subcategory in Emergency shutdowns, 1 - in Scheduled shutdowns)
   group_value = ['536', '537'] # Set the expected value of the corresponding subcategories of the parameter ‘group’, which is reflected in the query
   
   news_page = NewsPage(page)
   filter_modal = FilterModal(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_categories(category_filter[0], category_filter[1])
   filter_modal.apply_filter()
   
   # Write the value of the ‘group’ parameter that is sent in the query when the filter is applied
   actual_group_values = filter_modal.group_values
   # Collect the names of news categories after applying the filter
   category_names = news_page.collect_category_names()

   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the parent categories
   assert all(name.lower() in (filter_name.lower() for filter_name in parent_category) for name in category_names), f"{category_names} != {parent_category}" 
   # Check that the set of values of the ‘group’ parameter matches the expected list of values of all categories (by number and composition)
   assert sorted(actual_group_values) == sorted(group_value)