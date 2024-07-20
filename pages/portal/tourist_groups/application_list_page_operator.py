from playwright.sync_api import expect

class TGApplicationListPageOperator:
  
   def __init__(self, page):
      self.page = page
  
   # Открыть заявку по номеру маршрута
   def open_application_by_route_number(self, route_number):
      self.page.locator(f"//tbody/tr[.//*[contains(text(), '{route_number}')]]").click()
      expect(self.page.locator(".tg-application-form-header-pagename")).to_be_visible()