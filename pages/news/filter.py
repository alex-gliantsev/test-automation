from config import BASE_URL_SITE
from playwright.sync_api import expect
from urllib.parse import parse_qs, urlparse

class FilterModal:
   def __init__(self, page):
      self.page = page
      
   def go_to_filter_settings(self):
      self.page.goto(BASE_URL_SITE)
      self.page.get_by_label("Filter settings").click()
      expect(self.page.locator("app-news-filter")).to_be_visible()
      
   # Category filter
   def select_categories(self, *categories):
      self.page.locator("div.filter-settings__categories").get_by_text("Reset all").click()
      for category in categories:
        if isinstance(category, tuple):
            # If category is a tuple (category_name, index), select the nth occurrence
            category_name, index = category
            self.page.get_by_role("dialog").get_by_text(category_name, exact=True).nth(index).click()
        else:
            # If category is a string, select first occurrence
            self.page.get_by_role("dialog").get_by_text(category, exact=True).first.click()
            
   # Territory filter
   def select_territories(self, *territories):
      self.page.locator("div.filter-settings__territory").get_by_text("Reset all").click()
      for territory in territories:
         self.page.get_by_role("dialog").get_by_text(territory, exact=True).click()
   
   # Filter apply
   def apply_filter(self):
      with self.page.expect_request('**/api/v2/broadcasts/*') as request_info:
         self.page.click('button:has-text("APPLY FILTER")')
      
      request = request_info.value
      query_parameters = urlparse(request.url).query

      # Extract the values of the group and region parameters and comma-separate the values
      # check if there are parameters in the request so that the method can be applied to filters in any combination
      self.group_values = []
      self.region_values = []
      
      if 'group' in parse_qs(query_parameters):
         group_values = parse_qs(query_parameters)['group']
         self.group_values = [value for param in group_values for value in param.split(",")]
      
      if 'region' in parse_qs(query_parameters):
         region_values = parse_qs(query_parameters)['region']
         self.region_values = [value for param in region_values for value in param.split(",")]

      expect(self.page.locator('.news-list__main .news-single__wrap-head').first).to_be_visible()