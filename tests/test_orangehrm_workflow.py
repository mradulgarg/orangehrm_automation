from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

employees = [
    {"first": "KK", "last": "Sharma"},
    {"first": "Abhi", "last": "Verma"},
    {"first": "Niu", "last": "Singh"}
]

test_log = []  
step = 1

def log(category, desc, status):
    global step
    test_log.append((category, f"Step {step}", desc, status))
    step += 1

try:
    # Login Section
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(8)
    log("Login", "Open Orange HRM Login Page", "✅ Pass")

    driver.find_element(By.NAME, 'username').send_keys("Admin")
    driver.find_element(By.NAME, 'password').send_keys("admin123")
    driver.find_element(By.CLASS_NAME, 'oxd-button').click()
    time.sleep(5)
    log("Login", "Login with valid credentials", "✅ Pass")

    # Navigate to PIM
    driver.find_element(By.XPATH, "//a[@href='/web/index.php/pim/viewPimModule']").click()
    time.sleep(3)
    log("PIM Navigation", "Navigate to PIM Module", "✅ Pass")

    # Add Employees
    for emp in employees:
        driver.find_element(By.LINK_TEXT, "Add Employee").click()
        time.sleep(2)

        driver.find_element(By.NAME, "firstName").send_keys(emp["first"])
        driver.find_element(By.NAME, "lastName").send_keys(emp["last"])
        time.sleep(1)

        driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
        time.sleep(2)
        log("Add Employees", f"Add employee: {emp['first']} {emp['last']}", "✅ Pass")

        driver.find_element(By.LINK_TEXT, "Employee List").click()
        time.sleep(3)

    # Verify Employees
    for emp in employees:
        search_input = driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']")
        search_input.click()
        search_input.send_keys(Keys.COMMAND ,"a")
        search_input.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        search_input.send_keys(emp["first"])
        time.sleep(5)

        driver.find_element(By.XPATH, "//button[normalize-space()='Search']").click()
        time.sleep(5)
        # Fetch all employee rows
        rows = driver.find_elements(By.XPATH, "//div[@class='oxd-table-card']")
        found = False
        for row in rows:
            try:
                first_name = row.find_element(By.XPATH, ".//div[@class='oxd-table-cell oxd-padding-cell'][3]").text.strip()
                last_name = row.find_element(By.XPATH, ".//div[@class='oxd-table-cell oxd-padding-cell'][4]").text.strip()
                
                if first_name == emp["first"] and last_name == emp["last"]:
                    print(f"✅ Name Verified: {first_name} {last_name}")
                    log("Verify Employees", f"Verify employee: {emp['first']} {emp['last']}", "✅ Pass")
                    found = True
                    break
            except Exception as e:
                continue

        if not found:
            print(f"❌ Name Not Found: {emp['first']} {emp['last']}")
            log("Verify Employees", f"Verify employee: {emp['first']} {emp['last']}", "❌ Fail")

        
        time.sleep(3)


    # Logout
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-name").click()
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Logout").click()
    log("Logout", "Logout from Dashboard", "✅ Pass")

except Exception as e:
    log("Error", "Unexpected error: " + str(e), "❌ Fail")

finally:
    # Group by category
    categories = {}
    for entry in test_log:
        categories.setdefault(entry[0], []).append(entry)

    # Write table-style report
    with open("test_results.txt", "w") as file:
        file.write("QA Automation Test Results - Orange HRM\n")
        file.write("=" * 70 + "\n")

        for cat, steps in categories.items():
            file.write(f"\n📁 {cat}\n")
            file.write("-" * 70 + "\n")
            file.write(f"{'Step':<10} | {'Description':<50} | {'Status':<6}\n")
            file.write("-" * 70 + "\n")
            for _, step_no, desc, status in steps:
                file.write(f"{step_no:<10} | {desc:<50} | {status:<6}\n")
        file.write("\n" + "=" * 70 + "\n")

    driver.quit()
