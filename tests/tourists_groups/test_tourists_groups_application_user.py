import pytest,allure
from playwright.sync_api import expect, Page
from config import USER_CREDENTIALS, OPERATOR_TG_CREDENTIALS
from pages.portal.profile.portal_login_page import PortalLoginPage
from pages.admin.admin_login_page import AdminLoginPage
from pages.portal.tourist_groups.application_page_user import TGApplicationPageUser
from pages.portal.tourist_groups.application_list_page_user import TGApplicationListPageUser
from pages.portal.tourist_groups.application_page_operator import TGApplicationPageOperator
from pages.portal.tourist_groups.application_list_page_operator import TGApplicationListPageOperator

@allure.title("Creation of an application for registration of a tourist group by a registered user")
@allure.description("The user creates an application for registration of a tourist group; the Operator goes to the application sent by the user and registers it")
def test_tourist_group_application_creation_by_user(page: Page, browser):

   user_login_page = PortalLoginPage(page)
   user_application_page = TGApplicationPageUser(page)
   user_applications_list_page = TGApplicationListPageUser(page)
   
   user_data = USER_CREDENTIALS
   operator_data = OPERATOR_TG_CREDENTIALS

   # Tourist group user authorization
   user_login_page.user_auth(user_data['phone_number'])

   # Data for filling in the application form
   application_data = user_application_page.prepare_application_data(user_data)
   # Creating an application
   user_application_page.create_application_by_user(application_data, user_data)
   # Save the route number
   route_number = user_application_page.route_number
   
   # Check that the page with the message about successful submission is opened after sending the application
   assert page.locator(".tg-app-created-info-pageMessage").text_content().strip() == "Your application has been successfully submitted, an operator will contact you shortly"
   
   # Go to the page with the history of tour group applications
   user_applications_list_page.open_applications_list()
   
   # Check that the created application is present in the list (by route number)
   assert page.is_visible(f"text='{route_number}'")

   # Under the profile of the operator go to the page of the application created by the user
   # Creating a new context
   operator_context = browser.new_context()
   operator_page = operator_context.new_page()
   operator_login_page = AdminLoginPage(operator_page)
   operator_application_page = TGApplicationPageOperator(operator_page)
   operator_application_list_page = TGApplicationListPageOperator(operator_page)
   
   # Authorization of tour group operator
   operator_login_page.login(operator_data['username'], operator_data['password'])
   expect(operator_page.locator(".header__user-name", has_text='Logout')).to_be_visible()
   expect(operator_page.locator("h1", has_text="Application list")).to_be_visible()
   
   # Checking the presence of the application created by the user
   assert operator_page.is_visible(f"text='{route_number}'")
   
   # Go to the page of the application created by the user
   operator_application_list_page.open_application_by_route_number(route_number)
   
   # Operator registers the application
   operator_application_page.application_registration()

   # Check that the application is registered
   expected_status = "Registered"
   expect(operator_page.locator(f"//p[contains(text(), 'Статус')]/following-sibling::div[contains(text(), '{expected_status}')]")).to_be_visible()