from playwright.sync_api import Page
from pages.portal.news.filter import FilterModal
from pages.portal.news.news_page import NewsPage
import allure

@allure.title("Filter by single territory")
@allure.description("The test checks that after applying a filter on one territory, news for the selected territory (+ news for the total territory) are displayed. The corresponding parameter value is sent in the request.")
def  test_filter_by_single_territory_without_children(page: Page):
   
   territory_filter = 'Achinsk' # Specify the territory for which the filter will be applied.
   all_territories = 'Several districts of the Krasnoyarsk region'
   region_value = '4' # Set the expected value of the corresponding territory of the parameter ‘region’, which is reflected in the query
   
   filter_modal = FilterModal(page)
   news_page = NewsPage(page)
   
   filter_modal.go_to_filter_settings()
   filter_modal.select_territories(territory_filter)
   filter_modal.apply_filter()
   
   # Collecting names of territories after applying the filter
   territory_names = news_page.collect_territory_names()
   # Write the value of the region parameter that was sent in the query when the filter was applied
   actual_region_values = filter_modal.region_values
   
   # Check that the names of territories correspond to the selected region or news with the territory value 'Multiple territories' are displayed
   assert all(name == territory_filter or name == all_territories for name in territory_names), f"{territory_names} != {[territory_filter, all_territories]}" 
   # Check that the 'region' parameter contains the expected value
   assert actual_region_values == [region_value]

@allure.title("Фильтр по нескольким территориям без дочерних территорий")
@allure.description("Тест проверяет, что после применения фильтра по нескольким территориям отображаются новости по выбранным территориям (+ общая территория). В запросе отправляется соответствующее значение параметра")
def  test_filter_by_several_territories_without_children(page: Page):

   territory_filter = ['Achinsk', 'Borodino'] # Specify the territories for which the filter will be applied
   all_territories = 'Several districts of the Krasnoyarsk region'
   region_value = ['4', '51'] # Set the expected value of the corresponding territory of the parameter ‘region’, which is reflected in the query

   filter_modal = FilterModal(page)
   news_page = NewsPage(page)

   filter_modal.go_to_filter_settings()
   filter_modal.select_territories(territory_filter[0], territory_filter[1])
   filter_modal.apply_filter()

   # Collecting names of territories after applying the filter
   territory_names = news_page.collect_territory_names()

   # Write the value of the region parameter that was sent in the query when the filter was applied
   actual_region_values = filter_modal.region_values 

   # Check that the names of territories correspond to the selected regions or news with the territory value ‘Multiple territories’ are displayed
   assert all(name.lower() in (filter_name.lower() for filter_name in territory_filter) or name.lower() == all_territories.lower()
      for name in territory_names), f"{territory_names} != {territory_filter}"
   # Check that the ‘region’ parameter contains the expected value
   assert sorted(actual_region_values) == sorted(region_value)