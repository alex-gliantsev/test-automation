import requests
from config import USER_CREDENTIALS_FOR_DELETE, BASE_URL_SITE

def register_user(phone_number):
    try:
        formatted_phone = format_phone_number(phone_number)
        data = {
            "last_name": USER_CREDENTIALS_FOR_DELETE['surname'],
            "first_name": USER_CREDENTIALS_FOR_DELETE['name'],
            "patronymic_name": USER_CREDENTIALS_FOR_DELETE['patronymic'],
            "birth_year": "1980",
            "email": "",
            "phone": formatted_phone,
            "disability_type": [],
        }
        response = requests.post(
            f'{BASE_URL_SITE}/api/registration',
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status() 
        token_response = response.json()
        if "token" in token_response:
            token = token_response["token"]
            return token
        else:
            raise ValueError("Token not found")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to register user: {e}")

def format_phone_number(phone: str):
    if len(phone) != 10:
        raise ValueError("Phone number must be 10 digits long")
    return f"+7 ({phone[0:3]}) {phone[3:6]} {phone[6:8]}-{phone[8:]}"