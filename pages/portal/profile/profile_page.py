import random
from playwright.sync_api import expect
from config import BASE_URL_SITE

class ProfilePage:
   def __init__(self, page):
      self.page = page
      
   def go_to_profile_page(self):
      self.page.locator('[href="/profile"]').click()
      expect(self.page.locator('.profile__info')).to_be_visible()
   
   def profile_logout(self):
      self.page.get_by_role("button", name="Sign out").click()
      self.page.wait_for_url(f"{BASE_URL_SITE}/news", timeout=10000)
      self.page.wait_for_selector('.header__user')
      
   def delete_profile(self):
      self.page.get_by_role("button", name="Delete profile").click()
      auth_modal = self.page.locator(".auth-modal")
      auth_modal.get_by_role("button", name="SUBMIT").click()
      self.page.wait_for_url(f"{BASE_URL_SITE}/news", timeout=10000)
      
   # Prepare data for filling personal profile fields
   def prepare_personal_profile_data_to_edit(self):
    
      last_name_list = ["Ivanov-Black", "Petrov Junior", "Marmeladov", "Li", "Konstantinopolskiy"]
      first_name_list = ["Konstantin Evgeny", "Anton-Sergey", "Arnold", "Ed", "Yaroslav"]
      patronymic_list = ["Konstantinovich Junior", "Sergeevich-Junior", "Ed", "Arnoldovich", "Serafimovich"]
      
      last_name = random.choice(last_name_list)
      first_name = random.choice(first_name_list)
      patronymic = random.choice(patronymic_list)
      birth_year = str(random.randint(1902, 2024))
      
      personal_profile_data = {
          "last_name": last_name,
          "first_name": first_name,
          "patronymic": patronymic,
          "birth_year": birth_year
      }
      
      return personal_profile_data
   
   # Edit personal profile data fields
   def edit_personal_profile_data(self, personal_profile_data):
      self.page.locator('[aria-label="Edit"]').click()
      self.page.locator('[formcontrolname="last_name"]').fill(personal_profile_data['last_name'])
      self.page.locator('[formcontrolname="first_name"]').fill(personal_profile_data['first_name'])
      self.page.locator('[formcontrolname="patronymic_name"]').fill(personal_profile_data['patronymic'])
      self.page.locator('[formcontrolname="birth_year"]').fill(personal_profile_data['birth_year'])
      self.page.locator('[aria-label="Apply"]').click()
      expect(self.page.locator('[aria-label="Edit"]')).to_be_visible()
     
   # Prepare data for filling disability profile fields
   def prepare_disability_profile_data(self):
      disabilities_list = ["Hearing", "Mobility", "Speech", "Eyesight", "Other"]
      disability_type = random.choice(disabilities_list)
      contact_person = "Konstantinopolskiy Konstantin Konstantinovich"
      contact_person_phone = "9" + str(random.randint(100000000, 999999999))
      
      disailities_profile_data = {
          "disability_type": disability_type,
          "contact_person": contact_person,
          "contact_person_phone": contact_person_phone
      }
      
      return disailities_profile_data
   
   # Edit disability fields in the profile
   def edit_disability_profile_data(self, disailities_profile_data):
      self.page.locator('[aria-label="Edit"]').click()
      self.page.locator("label").filter(has_text="Disabilities").locator("app-custom-select").click()
      self.page.get_by_text("Yes", exact=True).click()
      self.page.locator("label").filter(has_text="Disability type").locator("app-custom-select").click()
      self.page.get_by_text(disailities_profile_data['disability_type']).click()
      self.page.locator('[formcontrolname="contactPersonName"]').fill(disailities_profile_data['contact_person'])
      self.page.locator('[formcontrolname="contactPersonPhone"]').fill(disailities_profile_data['contact_person_phone'])
      self.page.locator('[aria-label="Apply"]').click()
      expect(self.page.locator('[aria-label="Edit"]')).to_be_visible()
      
   # Removing disabilities
   def remove_disabilities(self):
      self.page.locator('[aria-label="Edit"]').click()
      self.page.locator("label").filter(has_text="Disabilities").locator("app-custom-select").click()
      self.page.get_by_text("No", exact=True).click()
      self.page.locator('[aria-label="Apply"]').click()
      expect(self.page.locator('[aria-label="Edit"]')).to_be_visible()
      
   # Prepare data for filling email field
   def prepare_email_profile_data(self):
      email = f"test{random.randint(100, 999)}@test.{random.choice(['ru', 'com'])}"
      return email
   
   # Edit email in the profile
   def edit_email_profile_data(self, email):
      self.page.locator('[aria-label="Edit"]').click()
      self.page.locator('[formcontrolname="email"]').fill(email)
      self.page.locator('[aria-label="Apply"]').click()
      expect(self.page.locator('[aria-label="Edit"]')).to_be_visible()

   # Delete email
   def delete_email(self):
      self.page.locator('[aria-label="Edit"]').click()
      self.page.locator('[formcontrolname="email"]').fill("")
      self.page.locator('[aria-label="Apply"]').click()
    
   # Add notification settings
   def add_notification(self, region, category):
      self.page.get_by_role("button", name="Add notification").click()
      self.page.locator(".auth-modal__list-item").get_by_text(region).click()
      self.page.get_by_role("button", name="Choose territory").click()
      self.page.get_by_text("All categories").click()
      self.page.get_by_text(category, exact=True).click()
      self.page.get_by_role("button", name="SAVE").click()
      self.page.wait_for_selector(".profile-notifications__list-selected")
  
   # Edit notification settings 
   def edit_notification(self, region, category):
      self.page.locator("li").filter(has_text=region).get_by_label("edit").click()
      self.page.get_by_text(category, exact=True).click()
      self.page.get_by_role("button", name="SAVE").click()
      self.page.wait_for_selector(".profile-notifications__list-selected")
    
   # Delete notifications
   def delete_notification(self, region):
      self.page.locator("li").filter(has_text=region).get_by_label("delete").click()
   
   # Edit phone number   
   def edit_phone_number(self, new_phone_number):
      self.page.get_by_label("Edit", exact=True).click()
      self.page.locator("[formcontrolname='phone']").fill(new_phone_number)
      with self.page.expect_response(lambda response: f"api/is_registered?phone=8{new_phone_number}" in response.url) as response_info:
         self.page.get_by_label("Apply").click()
      
      # Stop test if user with such phone is already registered
      response = response_info.value
      if response.status == 200:
         assert False, "The user with such phone number is already registered"

      expect(self.page.locator('[aria-label="Edit"]')).to_be_visible()