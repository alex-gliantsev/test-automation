from config import BASE_URL_SITE, VIEWPORT_SIZE
from playwright.sync_api import expect

class PortalLoginPage:
  def __init__(self, page):
      self.page = page

  # User authentication
  def user_auth(self, phone_number):
    self.page.set_viewport_size(VIEWPORT_SIZE)
    self.page.goto(BASE_URL_SITE)
    self.page.get_by_role("button", name="Sign In").click()
    self.page.get_by_role("button", name="Sign In with Phone Number").click()
    self.page.locator("[formcontrolname='phone']").fill(phone_number)
    with self.page.expect_response(lambda response: f"api/is_registered?phone=8{phone_number}" in response.url) as response_info:
      self.page.click('button:has-text("Sign In")')
      
    # Stop test if user with such phone is not registered
    response = response_info.value
    if response.status == 404:
      assert False, "The user with such phone number is not registered"
      
    expect(self.page.locator('[href="/profile"]')).to_be_visible()
    
  # Unregistered user authentication attempt
  def unregistered_user_auth_attempt(self, phone_number):
    self.page.set_viewport_size(VIEWPORT_SIZE)
    self.page.goto(BASE_URL_SITE)
    self.page.get_by_role("button", name="Sign In").click()
    self.page.get_by_role("button", name="Sign In with Phone Number").click()
    self.page.locator("[formcontrolname='phone']").fill(phone_number)
    self.page.click('button:has-text("SIGN IN")')