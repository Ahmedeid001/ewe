import time

from numpy import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions, Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from licensing.models import *
from licensing.methods import Key, Helpers

# Public key settings
RSAPubKey = "<RSAKeyValue><Modulus>qjCUvqnrVSzGQmXbx0EmXCdAIljouanKlmrJaVEllzl29qc0ULESIk5elWuxtUNY4Xp6+t++7jGJ4smjCdAPQ1oSTugTMI4q+2Y4WLueudEbaljWN1DgCtLAUYny1NVdQY7SNVwBG3y1PgmpEuaf5Vy/TIz6vTsroJPDux3ZoKivc9AB/kykFoN6ca7l7r2RVlcUMM+v7epBmuXmILuD0kEl/CMf+W8SORbBe0glIucKAecmlFg2Fpf9S8NDpX+E6WyQl3HwQLXj4y0iGwwC/S62K/SXrl72C9ODmrKFGY6ylA/0kszX+07aK1vM6lsWCrDYfgjkK3l99ivgwkHyXw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI5NjUwNjc3NSIsInJOZHY2YUtLOGNiL0ZiSzlibURPdGliY09iN0Z6ZHA2TjJ1ejkrMDkiXQ=="

# Path to the Edge WebDriver
driver_path = r"C:\Program Files\msedgedriver.exe"

# Edge browser options
edge_options = EdgeOptions()
edge_options.add_experimental_option("detach", True)
service = EdgeService(driver_path)



def read_serial_key(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()
    except Exception as e:
        print(f"Error reading key file: {e}")
        return None


def check_license(user_key):
    result = Key.activate(token=auth,
                          rsa_pub_key=RSAPubKey,
                          product_id=27851,
                          key=user_key,
                          machine_code=Helpers.GetMachineCode(v=2))

    if result[0] is None or not Helpers.IsOnRightMachine(result[0], v=2):
        print("License key not valid: {0}".format(result[1]))
        return False
    else:
        print("License key validated ✅!")
        return True


def read_credentials(file_path):
    accounts = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '|' in line:  # التأكد من وجود الفاصل '|'
                    email, password = line.split('|', 1)
                    accounts.append((email.strip(), password.strip()))
                else:
                    print(f"Warning: Invalid account format in line: {line}")
        return accounts
    except Exception as e:
        print(f"Error reading credentials file: {e}")
        return []
def login(driver, username, password):
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(username)

    password_input = driver.find_element(By.NAME, "pass")
    password_input.send_keys(password)

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    # Wait for the new page to load
    time.sleep(6)

    # Verify current URL to confirm successful login
    current_url = driver.current_url
    if "https://www.facebook.com/" in current_url and "login" not in current_url:
        print(f"Login successful for account {username} ✅🔥🔥.")
        return True
    else:
        print(f"☠️☠️Login failed for account {username} 🚫🚫.")
        return False


def initialize_driver():
    try:
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.set_page_load_timeout(6)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None


def create_facebook_page(driver):
    try:
        driver.get("https://www.facebook.com/me/")
        driver.get("https://www.facebook.com/pages/creation/?ref_type=launch_point")
        time.sleep(3)  # Wait for the page to reload
        body = driver.find_element(By.TAG_NAME, "body")  # العثور على عنصر الجسم
        ActionChains(driver).move_to_element(body).click().perform()  # النقر في الجسم

        # Generate a random username
        base_username = "Hello"
        random_number = random.randint(1, 1000)
        final_username = f"{base_username}{random_number}"

        # Wait for the username input field to be present and enter the generated username
        username_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, ':r')])[1]"))
        )
        username_input.send_keys(final_username)

        # Wait for the dynamic input field to be present and send the "Marketing Agency" text
        dynamic_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, ':r')])[2]"))
        )
        dynamic_input.send_keys("Marketing Agency")

        # Wait for the "Marketing Agency" element to be present and click it
        target_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xzsf02u'][normalize-space()='Marketing Agency']"))
        )
        target_element.click()

        # Click the "إنشاء الصفحة" button (Create Page button)
        create_page_button_xpath = "//span[normalize-space()='Create Page']"

        # Wait for the button to be present and scroll it into view
        create_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, create_page_button_xpath))
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", create_page_button)

        # Wait for the button to be clickable
        create_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, create_page_button_xpath))
        )

        # Use ActionChains to click the button
        actions = ActionChains(driver)
        actions.move_to_element(create_page_button).click().perform()

        print("page created successfully ✔️!")
        time.sleep(5)  # Wait for the page creation to complete
    except Exception as e:
        print(f"🚫🚫Error creating page: {e}")


def click_accept_button(driver):
    try:
        # Navigate to the specified page
        driver.get("https://www.facebook.com/")
        driver.get("https://www.facebook.com/certification/nondiscrimination/")
        time.sleep(1.5)  # Wait for the page to load fully

        # Check if the "I accept" button exists
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[@dir='auto']/span[contains(text(), 'I accept')]"))
            )

            # Scroll into view of the "I accept" button
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", accept_button)
            time.sleep(1)  # Wait briefly for scroll

            # Use JavaScript to click the button directly, bypassing potential obstructions
            driver.execute_script("arguments[0].click();", accept_button)
            print("Policies are accepted! ✅✔")
        except:
            print("Policies are already accepted.")

    except Exception as e:
        print(f"Error clicking accept button: {e}")

def click_acc(driver):
    try:

        driver.get("https://www.facebook.com/ads/manager/account_settings/")
        time.sleep(6)  # Wait for the page to load fully



    except Exception as e:
        print(f"Error button: {e}")

# دالة لتغيير العملة
def change_currency(driver):
    try:

        driver.get("https://business.facebook.com/billing_hub/accounts/details?asset_id=")
        time.sleep(7)  # الانتظار قليلاً لتحميل الصفحة

        edit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x8t9es0') and contains(text(), 'Edit')]"))
        )

        # التمرير إلى العنصر والنقر باستخدام JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
        driver.execute_script("arguments[0].click();", edit_button)

        # العثور على عنصر العملة
        currency_label = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@aria-label='Currency']"))
        )
        currency_label.click()  # فتح قائمة العملات

        # الانتظار لفتح قائمة العملات
        time.sleep(1)

        # اختيار العملة (الدولار الكندي كمثال)
        cad_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Canadian Dollar')]"))
        )
        cad_option.click()
        time.sleep(1)  # النقر على خيار العملة

        # Locate the Time Zone label to open the list of time zones
        timezone_label = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@aria-label='Time zone']"))
        )
        timezone_label.click()  # Open the timezone dropdown

        # Wait briefly to ensure the dropdown is open
        time.sleep(1)

        # Select "Darwin, Australia (GMT+09:30)" from the list
        darwin_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Darwin, Australia (GMT+09:30)')]"))
        )
        darwin_option.click()  # Click on the Darwin time zone option
        time.sleep(1)  # Pause briefly after clicking the time zone


        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@aria-label='Country/region']"))
        )

        # تغيير الدولة إلى الأردن
        country_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@aria-label='Country/region']"))
        )
        country_dropdown.click()

        # اختيار الدولة (الأردن)
        jordan_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Jordan']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", jordan_option)  # تمرير العنصر
        jordan_option.click()

        # الانتظار قليلاً حتى يتم تحديث القوائم
        time.sleep(1)
        # حفظ التغييرات
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Save']"))
        )
        save_button.click()

        print("Currency changed to Canadian Dollar successfully!")
    except Exception as e:
        print(f"Error changing currency: {e}")

def add_friends(driver, profile_urls):
    for profile_url in profile_urls:
        try:
            driver.get(profile_url)
            time.sleep(2)
            add_friend_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add friend')]"))
            )
            driver.execute_script("arguments[0].click();", add_friend_button)
            print(f"Friend request sent to: {profile_url}")
            time.sleep(3)
        except Exception as e:
            print(f"Error trying to add friend at {profile_url}: {e}")


def like_and_share_posts(driver, post_urls, max_likes=5):
    for post_url in post_urls:
        try:
            driver.get(post_url)
            time.sleep(1.5)

            # العثور على زر اللايكات وتحديد العدد الأقصى منها
            like_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Like' or @aria-label='أعجبني']"))
            )

            for i, button in enumerate(like_buttons):
                if i >= max_likes:
                    break
                try:
                    button.click()
                    print(f"Liked the post: {post_url}")
                    time.sleep(0.75)
                except Exception as e:
                    print(f"Error clicking Like button: {e}")

            # زر المشاركة
            share_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@aria-label='Send this to friends or post it on your profile.']")
            ))
            driver.execute_script("arguments[0].click();", share_button)
            print(f"Clicked Share button for post: {post_url}")

            # العثور على زر "Share Now"
            share_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Share now')]"))
            )
            driver.execute_script("arguments[0].click();", share_now_button)
            print(f"تم مشاركة المنشور: {post_url}")
            time.sleep(2)

        except Exception as e:
            print(f"Error trying to share post {post_url}: {e}")


def like_pages_and_join_groups(driver, pages, groups):
    for page in pages:
        try:
            driver.get(page)
            time.sleep(3)
            like_button = WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Like']//ancestor::div[contains(@role, 'none')]"))
            )
            driver.execute_script("arguments[0].click();", like_button)
            print(f"Liked page: {page}")
        except Exception as e:
            print(f"Error trying to like page {page}: {e}")

    for group in groups:
        try:
            driver.get(group)
            time.sleep(3)
            join_button = WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Join group']//ancestor::div[contains(@role, 'none')]"))
            )
            driver.execute_script("arguments[0].click();", join_button)
            print(f"Joined group: {group}")
        except Exception as e:
            print(f"Error trying to join group {group}: {e}")


# Main execution
def log_success(username):
    with open("success.txt", "a", encoding="utf-8") as success_file:
        success_file.write(f"All tasks completed for account {username} ✅✅!\n")


def log_failure(username):
    with open("failure.txt", "a", encoding="utf-8") as failure_file:
        failure_file.write(f"Failed tasks for account {username} 🚫🚫.\n")

# التعديل في الكود الرئيسي
if __name__ == "__main__":
    try:
        serial_file_path = "serial_key.txt"
        user_key = read_serial_key(serial_file_path)

        if user_key is None or not check_license(user_key):
            print("Can't work without a valid license key.")
        else:
            credentials_file_path = "cookies.txt"
            accounts_credentials = read_credentials(credentials_file_path)

            for username, password in accounts_credentials:
                driver = initialize_driver()

                if driver is None:
                    print(f"Could not initialize browser for account {username}. Moving to the next account.")
                    log_failure(username)
                    continue  # Move to the next account

                try:
                    # Attempt login and check success
                    if not login(driver, username, password):
                        print(f"Login failed for account {username}. Moving to the next account.")
                        log_failure(username)
                        driver.quit()  # Make sure to close the browser before moving to the next account
                        continue  # Move to the next account

                    # Perform tasks if login was successful
                    click_accept_button(driver)
                    click_acc(driver)
                    change_currency(driver)
                    profile_urls = [
                        "https://www.facebook.com/profile.php?id=61555934691990",
                        "https://www.facebook.com/profile.php?id=100012222130128",
                        "https://www.facebook.com/profile.php?id=100052784946068"
                    ]

                    post_urls = [
                        "https://www.facebook.com/AlAhlyYouth/posts/pfbid0KedK1emp2B46tEwzerDrZrVWg3eZk9AMEEEnLP5Jr6njwAnjTXpnb9FsQzj4DzJWl",
                        "https://www.facebook.com/Ex.fans/posts/pfbid02nKb2QTLLnRQWJtTRV6mhKd2b6zANFgkgcheqdQTnrKJepomNqFk3jP3oEcHRSTprl",
                        "https://www.facebook.com/quraany112/posts/pfbid0UVv7NNE4ZBEPma8SMeb4QmdQp7kvMcN7Ufi7cUWvetNo9Bz4rmP4rkRhudaxpiVDl",
                        "https://www.facebook.com/permalink.php?story_fbid=pfbid02ytgbjrBRcmou8FZyjPNx1wWv38NDYGo93dfW9uCKjZ2YQaP8fwsqCWzDLuxx16hrl&id=61563602456026"
                    ]

                    pages = [
                        "https://www.facebook.com/nmec.gov.eg",
                        "https://www.facebook.com/AlAhlyYouth",
                        "https://www.facebook.com/DreamparkEg",
                        "https://www.facebook.com/cu.edu.eg",
                        "https://www.facebook.com/ElTahrirEG"
                    ]

                    groups = [
                        "https://www.facebook.com/groups/132946953437450/",
                        "https://www.facebook.com/groups/171095983238060/",
                        "https://www.facebook.com/groups/1986335248280205/",
                        "https://www.facebook.com/groups/1381761178661357/"
                    ]

                    # تنفيذ المهام لكل حساب
                    add_friends(driver, profile_urls)
                    like_and_share_posts(driver, post_urls, max_likes=5)
                    like_pages_and_join_groups(driver, pages, groups)
                    create_facebook_page(driver)
                    click_accept_button(driver)


                    # تسجيل النجاح في الملف success.txt
                    log_success(username)

                    print(f"All tasks completed for account {username} ✅✅!")
                except Exception as e:
                    print(f"Unexpected error occurred while executing tasks for account {username}: {e}")
                    log_failure(username)
                finally:
                    driver.quit()  # Ensure the browser is closed after each attempt

            print("All tasks completed for all accounts! 🚫🚫")

    except Exception as main_exception:
        print(f"Error in main program: {main_exception}")
    finally:
        input("Press Enter to exit...")