from config import VIEWPORT_SIZE, BASE_URL_ADMIN

class AdminLoginPage:
   def __init__(self, page):
        self.page = page

   # User authentication (admin, operator)
   def login(self, username, password):
      self.page.set_viewport_size(VIEWPORT_SIZE)
      self.page.goto(BASE_URL_ADMIN)
      self.page.fill('input[name="username"]', username)
      self.page.fill('input[name="password"]', password)
      self.page.get_by_role("button", name="SIGN IN").click()