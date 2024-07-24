from playwright.sync_api import expect
import random
from datetime import datetime, timedelta
from config import USER_CREDENTIALS, BASE_URL_SITE

class TGApplicationPageUser:
   def __init__(self, page):
      self.page = page

   # Data preparing for filling in the application form
   def prepare_application_data(self):
      
      # Assign values to the date and time fields and convert them to the required format
      current_date = datetime.now()
      self.current_date_string = current_date.strftime("%Y-%m-%d")
      current_datetime_string = current_date.strftime("%Y-%m-%dT%H:%M")
      return_datetime = current_date + timedelta(days=10)
      return_datetime_string = return_datetime.strftime("%Y-%m-%dT%H:%M")
      reserve_date = return_datetime + timedelta(days=1)
      reserve_date_string = reserve_date.strftime("%Y-%m-%d")
      connection_session = current_date + timedelta(days=5)
      connection_session_string = connection_session.strftime("%Y-%m-%dT%H:%M")
      
      # Full name to verify display in the list of applications
      self.full_name = f"{USER_CREDENTIALS['surname']} {USER_CREDENTIALS['name']} {USER_CREDENTIALS['patronymic']}"
      
      # Set values for filling in the fields of the application
      application_data = {
         "current_date": current_datetime_string,
         "return_date": return_datetime_string,
         "reserve_date": reserve_date_string,
         "connection_session": connection_session_string,
         "route_number": self.route_number,
         "application_status": self.application_status,
         "application_source": self.application_source,
         "adress_search": "krasnoyarsk mira 94",
         "adress": "Krasnoyarskiy kray, g. Krasnoyarsk, pr. mira, z. 94",
         "birthdate": "2000-01-01",
         "apartment_number": str(random.randint(1, 199)),
         "email": "tguser@test.ru",
         "contact_person": "Contact person. Phone +7 999-999 99 99",
         "group_member": "Ivanov Ivan Ivanovich",
         "place_search": ["krasnoyarsk", "khakassia"], # values to search for waypoints and regions
         "rout_point": ["Krasnoyarskiy kray", "Republic of Khakassia"],
         "full_name": self.full_name
      }
      return application_data
     
   # Create application
   def create_application_by_user(self, application_data):
      self.page.get_by_role("link", name="Tourist groups").click()
      self.page.get_by_role("button", name="Register group").click()
      expect(self.page.locator(".tg-application-form")).to_be_visible()

      # Organisation information block
      self.page.locator("app-company").get_by_placeholder("Enter the organisation name").fill("Tourist organisation")
      self.page.locator("//app-company//p[normalize-space(text())='Contact phone']/following-sibling::input[@type='text']").fill(USER_CREDENTIALS['phone_number'])
      self.page.locator("app-company").get_by_placeholder("Enter the address").fill(application_data["adress_search"])
      self.page.get_by_text(application_data["adress"], exact=True).click()
      
      # Block of information about the tour group leader
      self.page.locator("app-leader").get_by_placeholder("Enter surname").fill(USER_CREDENTIALS['surname'])
      self.page.locator("app-leader").get_by_placeholder("Enter name").fill(USER_CREDENTIALS['name'])
      self.page.locator("app-leader").get_by_placeholder("Enter patronymic").fill(USER_CREDENTIALS['patronymic'])
      self.page.locator("app-leader input[type=\"date\"]").fill(application_data["birthdate"])
      self.page.locator("app-leader").get_by_placeholder("Enter address").fill(application_data["adress_search"])
      self.page.get_by_text(application_data["adress"], exact=True).click()
      self.page.locator("app-leader").get_by_placeholder("Enter apartment number").fill(application_data["apartment_number"])
      self.page.locator("//app-leader//p[normalize-space(text())='Mobile phone']/following-sibling::input[@type='text']").fill(USER_CREDENTIALS['phone_number'])
      self.page.locator("//app-leader//p[normalize-space(text())='Home phone']/following-sibling::input[@type='text']").fill(USER_CREDENTIALS['phone_number'])
      self.page.locator("//app-leader//p[normalize-space(text())='Work phone']/following-sibling::input[@type='text']").fill(USER_CREDENTIALS['phone_number'])
      self.page.locator("app-leader").get_by_placeholder("example@mail.ru").fill(application_data["email"])
      self.page.locator("app-leader").get_by_placeholder("Name, phone").fill(application_data["contact_person"])
      
      # Group size block
      self.page.locator(".tg-application-form-subform").get_by_placeholder("Enter group size").fill("2")
      self.page.wait_for_selector("app-tourist-group-members")
      self.page.locator("app-tourist-group-members").get_by_placeholder("Enter full name").fill(application_data["group_member"])
      self.page.locator("app-tourist-group-members input[type=\"date\"]").fill(application_data["birthdate"])
      self.page.locator("//app-tourist-group-members//p[normalize-space(text())='Phone']/following-sibling::input[@type='text']").fill(USER_CREDENTIALS['phone_number'])
      
      # Route information block
      self.page.locator("app-route app-search-input:has-text('Starting point') input").fill(application_data["place_search"][0])
      self.page.get_by_text(application_data["rout_point"][0], exact=True).click()
      self.page.locator("app-route app-search-input:has-text('End point') input").fill(application_data["place_search"][1])
      self.page.get_by_text(application_data["rout_point"][1], exact=True).click()
      self.page.locator("app-route").get_by_placeholder("Enter distance").fill("100")
      self.page.locator("app-route input[type=\"datetime-local\"]").first.fill(application_data["current_date"])
      self.page.locator("app-route input[type=\"datetime-local\"]").nth(1).fill(application_data["return_date"])
      self.page.locator("app-route input[type=\"date\"]").fill(application_data["reserve_date"])

      # Block of timeframes and methods of communication
      self.page.locator("app-communications input[type=\"datetime-local\"]").fill(application_data["connection_session"])
      self.page.locator("app-communications").get_by_placeholder("Enter method").fill("Mobile")
      self.page.get_by_role("button", name="Add session").click()
      self.page.locator("app-communications input[type=\"datetime-local\"]").nth(1).fill(application_data["connection_session"])
      self.page.locator("app-communications").get_by_placeholder("Enter method").nth(1).fill("Mobile")
      
      # With sending the request, track the response from the server
      with self.page.expect_response(lambda response: "api/tourist_groups" in response.url and response.status in [200, 201]) as response_info:
         self.page.get_by_role("button", name="Submit application").click()
         
      # From the response, save the route number for further interaction with the application
      response = response_info.value
      response_body = response.json()
      self.route_number = response_body.get('route_number')
      assert self.route_number is not None, "Failed to retrieve the route number from the response"
      
      expect(self.page.locator(".tg-app-created-info")).to_be_visible()