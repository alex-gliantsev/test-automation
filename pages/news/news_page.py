
class NewsPage:
   def __init__(self, page):
      self.page = page
      
   def collect_category_names(self):
      category_names = self.page.locator('.news-list__main .categoryColorBg').all_text_contents()
      category_names = [name.strip() for name in category_names]
      return category_names
   
   def collect_territory_names(self):
      territory_names = self.page.locator('.news-list__main .news-single__region').all_text_contents()
      territory_names = [name.strip() for name in territory_names]
      return territory_names