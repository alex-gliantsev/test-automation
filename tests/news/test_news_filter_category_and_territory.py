import allure
from pages.portal.news.filter import FilterModal
from pages.portal.news.news_page import NewsPage
from playwright.sync_api import Page

@allure.title("Filter by category with subcategories and territory with districts")
@allure.description("The test checks that the combined filter on category with subcategories and territory with regions is applied correctly. In the query, the value of the 'region' parameter corresponds to territories")
def test_filter_by_category_and_territory(page: Page):

   territory_filter = 'Krasnoyarsk'
   region_value = ['68','67','66','65','64','63','62','1']
   category_filter = 'Emergency shutdowns'
   
   filter_modal = FilterModal(page)
   news_page = NewsPage(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_territories(territory_filter)
   filter_modal.select_categories(category_filter)
   filter_modal.apply_filter()
   
   # Collect the names of news categories after applying the filter
   category_names = news_page.collect_category_names()

   # Write the value of the region parameter that was sent in the query when the filter was applied
   actual_region_values = filter_modal.region_values 
   
   # Check that the 'region' parameter contains the expected value
   assert sorted(actual_region_values) == sorted(region_value)
   
   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the selected category
   assert all(name.lower() == category_filter.lower() for name in category_names), f"{category_names} != {category_filter}" 
   
@allure.title("Filter by subcategory and district of the territory")
@allure.description("The test verifies that the combined filter by subcategory and separate region of the territory is applied correctly. In the query the values of parameters 'group' and 'region' correspond to categories and territories")
def test_filter_by_subcategory_and_district(page: Page):

   territory_filter = 'Central district of Krasnoyarsk'
   region_value = '68'
   all_territories = 'Several districts of the Krasnoyarsk region'
   parent_category = 'Emergency shutdowns'
   category_filter = ('Hot water supply', 0)
   group_value = '534'
   
   filter_modal = FilterModal(page)
   news_page = NewsPage(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_territories(territory_filter)
   filter_modal.select_categories(category_filter)
   filter_modal.apply_filter()
   
   # Collecting category and territory names after applying the filter
   category_names = news_page.collect_category_names()
   territory_names = news_page.collect_territory_names()

   # Write the value of parameters in the query when applying the filter
   actual_region_values = filter_modal.region_values
   actual_group_values = filter_modal.group_values
   
   # Check that the parameters contain the expected value
   assert actual_region_values == [region_value]
   assert actual_group_values == [group_value]
   
   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the parent category
   assert all(name.lower() == parent_category.lower() for name in category_names), f"{category_names} != {parent_category}" 
   
   # Check that the names of territories correspond to the selected region or news with the territory value 'Multiple territories' are displayed
   assert all(name == territory_filter or name == all_territories for name in territory_names), f"{territory_names} != {[territory_filter, all_territories]}" 
   
@allure.title("Filter by multiple categories and territories")
@allure.description("The test checks that the combined filter with several categories and territories is applied correctly. In the query, the values of parameters 'group' and 'region' correspond to categories and territorie")
def test_filter_by_several_categories_and_territories(page: Page):

   territory_filter = ['Achinsk', 'Bogotol']
   region_value = ['4', '50']
   all_territories = 'Several districts of the Krasnoyarsk region'
   parent_category = ['Emergency shutdowns', 'Scheduled shutdowns'] # Set categories that contain a subcategory (Expected category name in the news)
   category_filter = [('Hot water supply', 0), ('Hot water supply', 1)] # Specify the subcategories by which the filter will be applied (0 - subcategory in Emergency shutdowns, 1 - in Scheduled shutdowns)
   group_value = ['534', '535'] #Set the expected value of the corresponding subcategories of the parameter ‘group’, which is reflected in the query
   
   filter_modal = FilterModal(page)
   news_page = NewsPage(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_territories(territory_filter[0], territory_filter[1])
   filter_modal.select_categories(category_filter[0], category_filter[1])
   filter_modal.apply_filter()
   
   # Collecting category and territory names after applying the filter
   category_names = news_page.collect_category_names()
   territory_names = news_page.collect_territory_names()

   # Write the value of parameters in the query when applying the filter
   actual_region_values = filter_modal.region_values
   actual_group_values = filter_modal.group_values
   
   # Check that the parameters contain the expected value
   assert sorted(actual_region_values) == sorted(region_value)
   assert sorted(actual_group_values) == sorted(group_value)
   
   assert len(category_names) > 0, "The list is empty, no news with the given query found"
   # Check that the values of the category names of each news item correspond to the parent category
   assert all(name.lower() in (filter_name.lower() for filter_name in parent_category) 
      for name in category_names), f"{category_names} != {parent_category}" 
   
   # Check that the names of territories correspond to the selected region or news with the territory value 'Multiple territories' are displayed
   assert all(name.lower() in (filter_name.lower() for filter_name in territory_filter) or name.lower() == all_territories.lower()
      for name in territory_names), f"{territory_names} != {territory_filter}"