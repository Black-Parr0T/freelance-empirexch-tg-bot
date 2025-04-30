import requests
from basic_func import generate_username, append_to_csv

headers_common = {
    "Host": "api.uvwin2024.co",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept": "application/json, text/plain, */*",
    "Sec-Ch-Ua": "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Sec-Ch-Ua-Mobile": "?0",
    "Origin": "https://www.empirexch.com",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.empirexch.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
}

async def send_reg_request(phone_number):
    session = requests.Session()
    try:
        res = session.get(
            f"https://api.uvwin2024.co/account/v2/users/phones/91{phone_number}/:exists",
            headers=headers_common,
        )

        if 'true' in res.text:
            print(f"Phone number {phone_number} already exists.")
            return {"error": "Phone number already exists"}
        
        response = session.post(
            f"https://api.uvwin2024.co/account/v2/otp/?mobileNumber=91{phone_number}",
            headers={**headers_common, "Content-Length": "0"},
            data=b""
        )

        if response.status_code != 204:
            print("Failed to send OTP.")
            return {"error": "Failed to send OTP"}
        return {"success": True}, session
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}
    
async def verify_otp(session, phone_number, otp, user_id=None):
    try:
        response = session.post(
            f"https://api.uvwin2024.co/account/v2/otp/validate?mobileNumber=91{phone_number}&otp={otp}",
            headers={**headers_common, "Content-Type": "application/json;charset=UTF-8"},
            json={}
        )
        if response.status_code != 204:
            print("Invalid OTP.")
            return {"error": "Invalid OTP"}
        
        res = register_user(session, phone_number, otp, user_id=user_id)
        
        if res.get('error'):
            print("Registration failed.")
            return {"error": "Registration failed"}
        print("OTP verified successfully.")
        return {"success": True}
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}
    

async def register_user(session, phone_number, otp, campaign_code=None,user_id=None):
    try:
        username = generate_username()
        signup_payload = {
                "fullName": username,
                "username": username,
                "password": 'Anand@123',
                "phoneNumber": f'91{phone_number}',
                "referralCode": None,
                "campaignCode": campaign_code,
                "otp": otp
            }
        
        response = session.post(
                "https://api.uvwin2024.co/account/v2/accounts/signup",
                headers={**headers_common, "Content-Type": "application/json;charset=UTF-8"},
                json=signup_payload
            )
        if response.status_code == 204:
            await append_to_csv('empirexch', data=[username, 'Anand@123', phone_number, campaign_code, user_id], header=['username', 'password', 'phone_number', 'campaign_code', 'user_id'])
            print("Signup successful!")
            return {"success": True}
        else:
            print("Signup failed.")
            print(response.text)
            return {"error": "Signup failed"}
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}