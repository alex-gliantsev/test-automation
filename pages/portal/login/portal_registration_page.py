from playwright.sync_api import expect
from config import BASE_URL_SITE, VIEWPORT_SIZE
import random

class PortalRegistrationPage:
   def __init__(self, page):
      self.page = page

   # Prepare data for filling personal profile fields for registration
   def prepare_user_data_to_register(self):

      last_name_list = ["Ivanov-Black", "Petrov Junior", "Marmeladov", "Li", "Konstantinopolskiy"]
      first_name_list = ["Konstantin Evgeny", "Anton-Sergey", "Arnold", "Ed", "Yaroslav"]
      patronymic_list = ["Konstantinovich Junior", "Sergeevich-Junior", "Ed", "Arnoldovich", "Serafimovich"]
      
      phone_number = "9" + str(random.randint(100000000, 999999999))
      last_name = random.choice(last_name_list)
      first_name = random.choice(first_name_list)
      patronymic = random.choice(patronymic_list)
      birth_year = str(random.randint(1902, 2024))
      
      registration_data = {
         "phone_number": phone_number,
         "last_name": last_name,
         "first_name": first_name,
         "patronymic": patronymic,
         "birth_year": birth_year
      }
      
      return registration_data
   
   # Prepare data for filling disability profile fields for registration
   def prepare_disability_data_to_register(self):
      
      disabilyties = ["Hearing", "Mobility", "Speech", "Eyesight", "Other"]
      disability_type = random.choice(disabilyties)
      contact_person_phone = "9" + str(random.randint(100000000, 999999999))
      
      disability_data = {
          "disability_type": disability_type,
          "contact_person": "Konstantinopolskiy Konstantin Konstantinovich",
          "contact_person_phone": contact_person_phone
      }
      
      return disability_data
   
   # User registration
   def user_registration(self, registration_data, disability_data=None):
      self.page.set_viewport_size(VIEWPORT_SIZE)
      self.page.goto(BASE_URL_SITE)
      self.page.get_by_role("button", name="Sign in").click()
      self.page.get_by_role("button", name="SIGN UP").click()
      self.page.locator('[formcontrolname="last_name"]').fill(registration_data['last_name'])
      self.page.locator('[formcontrolname="first_name"]').fill(registration_data['first_name'])
      self.page.locator('[formcontrolname="patronymic_name"]').fill(registration_data['patronymic'])
      self.page.locator('[formcontrolname="birth_year"]').fill(registration_data['birth_year'])
      self.page.locator('[formcontrolname="phone"]').fill(registration_data['phone_number'])
      
      if disability_data:
         self.page.locator("label").filter(has_text="Disabilities").locator(".selectValue").click()
         self.page.get_by_text("Yes", exact=True).click()
         self.page.locator("label").filter(has_text="Disability type").locator(".selectValue").click()
         self.page.locator("li").filter(has_text=disability_data['disability_type']).locator("svg").click()
         self.page.get_by_label("Contact person").fill(disability_data['contact_person'])
         self.page.get_by_label("Contact person phone").fill(disability_data['contact_person_phone'])
         
      with self.page.expect_response(lambda response: f"api/is_registered?phone=8{registration_data['phone_number']}" in response.url) as response_info:
         self.page.get_by_role("button", name="SIGN UP").click()
         
      expect(self.page.locator('[href="/profile"]')).to_be_visible()
      
      # Stop test if user with such phone is already registered
      response = response_info.value
      if response.status == 200:
         assert False, "The user with such phone number is already registered"