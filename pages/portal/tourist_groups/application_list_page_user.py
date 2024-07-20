from playwright.sync_api import expect

class TGApplicationListPageUser:
   def __init__(self, page):
      self.page = page
     
   # Open applications list 
   def open_applications_list(self):
      self.page.get_by_label("Site header").get_by_role("link", name="Tourist groups").click()
      self.page.get_by_role("button", name="Routes history").click()
      expect(self.page.locator("h1")).to_be_visible()
   
   # Open application by route number 
   def open_application_by_route_number(self, route_number):
      self.page.locator(f"//tbody/tr[.//*[contains(text(), '{route_number}')]]").click()
      expect(self.page.locator(".tg-application-form-header-pagename")).to_be_visible()