#!/usr/bin/env python
"""API Testing Script - Test all endpoints"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class APITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.hotel_id = None
        self.billing_id = None
        self.menu_id = None
    
    def print_test(self, title):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
        print(f"TEST: {title}")
        print(f"{'='*60}{Colors.END}")
    
    def print_request(self, method, endpoint, data=None):
        print(f"\n{Colors.BLUE}📤 REQUEST:{Colors.END}")
        print(f"   Method: {Colors.BOLD}{method}{Colors.END}")
        print(f"   URL: {self.base_url}{endpoint}")
        if data:
            print(f"   Body: {Colors.CYAN}{json.dumps(data, indent=2)}{Colors.END}")
    
    def print_response(self, response):
        print(f"\n{Colors.GREEN}📥 RESPONSE:{Colors.END}")
        print(f"   Status: {Colors.BOLD}{response.status_code}{Colors.END}")
        try:
            data = response.json()
            print(f"   Body: {Colors.CYAN}{json.dumps(data, indent=2)}{Colors.END}")
            return data
        except:
            print(f"   Body: {response.text}")
            return None
    
    def print_success(self, message):
        print(f"\n{Colors.GREEN}✅ {message}{Colors.END}")
    
    def print_error(self, message):
        print(f"\n{Colors.RED}❌ {message}{Colors.END}")
    
    def print_info(self, message):
        print(f"\n{Colors.YELLOW}ℹ️  {message}{Colors.END}")
    
    # AUTH ENDPOINTS
    def test_register(self):
        self.print_test("User Registration")
        endpoint = "/auth/register"
        data = {
            "username": f"testuser_{datetime.now().timestamp()}",
            "password": "TestPass@123",
            "phone_number": "+919876543210",
            "email": "testuser@example.com"
        }
        self.print_request("POST", endpoint, data)
        response = requests.post(f"{self.base_url}{endpoint}", json=data)
        result = self.print_response(response)
        
        if response.status_code == 201:
            self.print_success("User registered successfully!")
            self.user_id = result['user']['id']
            return True
        else:
            self.print_error(f"Registration failed: {result['error']}")
            return False
    
    def test_send_otp(self):
        self.print_test("Send OTP")
        endpoint = "/auth/send-otp"
        data = {"phone_number": "+919876543210"}
        self.print_request("POST", endpoint, data)
        response = requests.post(f"{self.base_url}{endpoint}", json=data)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("OTP sent successfully!")
            self.print_info(f"OTP ID: {result['otp_id']}")
            return result
        else:
            self.print_error(f"Failed to send OTP: {result['error']}")
            return None
    
    def test_verify_otp(self, otp_code="123456"):
        self.print_test("Verify OTP")
        endpoint = "/auth/verify-otp"
        data = {
            "phone_number": "+919876543210",
            "otp_code": otp_code
        }
        self.print_request("POST", endpoint, data)
        response = requests.post(f"{self.base_url}{endpoint}", json=data)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("OTP verified successfully!")
            return True
        else:
            self.print_error(f"OTP verification failed: {result['error']}")
            return False
    
    def test_login(self):
        self.print_test("User Login")
        endpoint = "/auth/login"
        data = {
            "username": "hotelowner",
            "password": "password123"
        }
        self.print_request("POST", endpoint, data)
        response = requests.post(f"{self.base_url}{endpoint}", json=data)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Login successful!")
            self.token = result['token']
            self.user_id = result['user']['id']
            self.print_info(f"Token: {self.token[:50]}...")
            return True
        else:
            self.print_error(f"Login failed: {result['error']}")
            return False
    
    # HOTEL ENDPOINTS
    def test_create_hotel(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("Create Hotel")
        endpoint = "/hotel/create"
        data = {
            "name": f"Test Hotel {datetime.now().timestamp()}",
            "description": "A test hotel for API testing",
            "phone_number": "+91-11-12345678",
            "email": "hotel@test.com",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "Test State",
            "zipcode": "123456",
            "country": "India",
            "total_rooms": 50,
            "check_in_time": "14:00",
            "check_out_time": "11:00",
            "currency": "INR"
        }
        self.print_request("POST", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 201:
            self.print_success("Hotel created successfully!")
            self.hotel_id = result['hotel']['id']
            return True
        else:
            self.print_error(f"Hotel creation failed: {result['error']}")
            return False
    
    def test_get_hotel(self):
        if not self.token or not self.hotel_id:
            self.print_error("No hotel ID available. Create hotel first!")
            return False
        
        self.print_test("Get Hotel Details")
        endpoint = f"/hotel/{self.hotel_id}"
        self.print_request("GET", endpoint)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Hotel details retrieved successfully!")
            return True
        else:
            self.print_error(f"Failed to get hotel: {result['error']}")
            return False
    
    def test_update_hotel(self):
        if not self.token or not self.hotel_id:
            self.print_error("No hotel ID available. Create hotel first!")
            return False
        
        self.print_test("Update Hotel")
        endpoint = f"/hotel/{self.hotel_id}"
        data = {
            "total_rooms": 100,
            "description": "Updated hotel description"
        }
        self.print_request("PUT", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.put(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Hotel updated successfully!")
            return True
        else:
            self.print_error(f"Hotel update failed: {result['error']}")
            return False
    
    # MENU ENDPOINTS
    def test_create_menu(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("Create Menu Item")
        endpoint = "/menu/create"
        data = {
            "name": "Paneer Butter Masala",
            "description": "Creamy curry with cottage cheese",
            "category": "Main Course",
            "price": 350.00,
            "availability": True,
            "preparation_time": 25,
            "is_vegetarian": True,
            "is_vegan": False
        }
        self.print_request("POST", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 201:
            self.print_success("Menu item created successfully!")
            self.menu_id = result['menu']['id']
            return True
        else:
            self.print_error(f"Menu creation failed: {result['error']}")
            return False
    
    def test_list_menus(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("List Menu Items")
        endpoint = "/menu/list"
        self.print_request("GET", endpoint)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success(f"Retrieved {len(result['menus'])} menu items!")
            return True
        else:
            self.print_error(f"Failed to list menus: {result['error']}")
            return False
    
    def test_update_menu(self):
        if not self.token or not self.menu_id:
            self.print_error("No menu ID available. Create menu first!")
            return False
        
        self.print_test("Update Menu Item")
        endpoint = f"/menu/{self.menu_id}"
        data = {
            "price": 400.00,
            "availability": False
        }
        self.print_request("PUT", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.put(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Menu item updated successfully!")
            return True
        else:
            self.print_error(f"Menu update failed: {result['error']}")
            return False
    
    # BILLING ENDPOINTS
    def test_create_billing(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("Create Billing Record")
        endpoint = "/billing/create"
        check_in = datetime.now()
        check_out = check_in + timedelta(days=3)
        data = {
            "guest_name": "John Doe",
            "guest_email": "john@example.com",
            "guest_phone": "+91-9999999999",
            "check_in_date": check_in.isoformat(),
            "check_out_date": check_out.isoformat(),
            "room_number": "301",
            "total_amount": 15000.00
        }
        self.print_request("POST", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 201:
            self.print_success("Billing record created successfully!")
            self.billing_id = result['billing']['id']
            return True
        else:
            self.print_error(f"Billing creation failed: {result['error']}")
            return False
    
    def test_list_billings(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("List Billing Records")
        endpoint = "/billing/list"
        self.print_request("GET", endpoint)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success(f"Retrieved {len(result['billings'])} billing records!")
            return True
        else:
            self.print_error(f"Failed to list billings: {result['error']}")
            return False
    
    def test_add_invoice(self):
        if not self.token or not self.billing_id:
            self.print_error("No billing ID available. Create billing first!")
            return False
        
        self.print_test("Add Invoice to Billing")
        endpoint = f"/billing/{self.billing_id}/add-invoice"
        data = {
            "invoice_number": f"INV-{datetime.now().timestamp()}",
            "item_description": "Room Charges - 3 nights",
            "quantity": 3,
            "unit_price": 5000.00
        }
        self.print_request("POST", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 201:
            self.print_success("Invoice added successfully!")
            return True
        else:
            self.print_error(f"Invoice addition failed: {result['error']}")
            return False
    
    def test_record_payment(self):
        if not self.token or not self.billing_id:
            self.print_error("No billing ID available. Create billing first!")
            return False
        
        self.print_test("Record Payment")
        endpoint = f"/billing/{self.billing_id}/payment"
        data = {"amount": 7500.00}
        self.print_request("POST", endpoint, data)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Payment recorded successfully!")
            return True
        else:
            self.print_error(f"Payment recording failed: {result['error']}")
            return False
    
    # REPORTS ENDPOINTS
    def test_revenue_report(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("Revenue Report")
        endpoint = "/reports/revenue?days=30"
        self.print_request("GET", endpoint)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Revenue report retrieved successfully!")
            return True
        else:
            self.print_error(f"Failed to get revenue report: {result['error']}")
            return False
    
    def test_menu_report(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("Menu Report")
        endpoint = "/reports/menu-popular"
        self.print_request("GET", endpoint)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Menu report retrieved successfully!")
            return True
        else:
            self.print_error(f"Failed to get menu report: {result['error']}")
            return False
    
    def test_occupancy_report(self):
        if not self.token:
            self.print_error("No token available. Login first!")
            return False
        
        self.print_test("Occupancy Report")
        endpoint = "/reports/occupancy"
        self.print_request("GET", endpoint)
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
        result = self.print_response(response)
        
        if response.status_code == 200:
            self.print_success("Occupancy report retrieved successfully!")
            return True
        else:
            self.print_error(f"Failed to get occupancy report: {result['error']}")
            return False
    
    def run_all_tests(self):
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║         HOTEL MANAGEMENT APP - API TEST SUITE            ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        print(f"\n{Colors.BOLD}🔐 AUTHENTICATION TESTS{Colors.END}")
        self.test_login()
        
        print(f"\n{Colors.BOLD}🏨 HOTEL TESTS{Colors.END}")
        self.test_create_hotel()
        self.test_get_hotel()
        self.test_update_hotel()
        
        print(f"\n{Colors.BOLD}🍽️  MENU TESTS{Colors.END}")
        self.test_create_menu()
        self.test_list_menus()
        self.test_update_menu()
        
        print(f"\n{Colors.BOLD}💳 BILLING TESTS{Colors.END}")
        self.test_create_billing()
        self.test_list_billings()
        self.test_add_invoice()
        self.test_record_payment()
        
        print(f"\n{Colors.BOLD}📊 REPORTS TESTS{Colors.END}")
        self.test_revenue_report()
        self.test_menu_report()
        self.test_occupancy_report()
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                    ALL TESTS COMPLETED!                   ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")

if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()
