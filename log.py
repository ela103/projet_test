from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# --- CONFIG CHROME ---
options = Options()
options.add_argument("--remote-allow-origins=*")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# --- FERMER MESSAGE D'ERREUR ---
def close_error():
    try:
        btn = driver.find_element(By.CSS_SELECTOR, "[data-test='error-button']")
        btn.click()
        time.sleep(2)
    except:
        pass

# --- RESET PAGE LOGIN ---
def reset_page():
    driver.get("https://www.saucedemo.com/")
    wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    wait.until(EC.visibility_of_element_located((By.ID, "password")))
    wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    close_error()

# --- RÉCUPÉRER L'ERREUR ---
def get_error():
    time.sleep(2)
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        return elem.text.strip()
    except:
        return ""

# =========================================
#   TESTS POUR TOUS LES USERNAMES
# =========================================

# ================================
# TESTS LOGIN - 5 CAS POUR CHAQUE USERNAME
# ================================

usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

correct_password = "secret_sauce"
wrong_password = "wrong_password"

for user in usernames:
    print(f"\n========== TESTS POUR {user} ==========")

    # LGN-01 : login valide
    reset_page()
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(correct_password)
    driver.find_element(By.ID, "login-button").click()
    if "inventory.html" in driver.current_url:
        print(f"LGN-01 : {user} LOGIN RÉUSSI")
    else:
        print(f"LGN-01 : {user} LOGIN ÉCHOUÉ -> {get_error()}")

    # LGN-02 : mauvais mot de passe
    reset_page()
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(wrong_password)
    driver.find_element(By.ID, "login-button").click()
    print(f"LGN-02 : {user} -> {get_error()}")

    # LGN-03 : username vide
    reset_page()
    driver.find_element(By.ID, "password").send_keys(correct_password)
    driver.find_element(By.ID, "login-button").click()
    print(f"LGN-03 : {user} -> {get_error()}")

    # LGN-04 : password vide
    reset_page()
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "login-button").click()
    print(f"LGN-04 : {user} -> {get_error()}")

    # LGN-05 : utilisateur verrouillé (uniquement pour locked_out_user)
    reset_page()
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(correct_password)
    driver.find_element(By.ID, "login-button").click()
    if user == "locked_out_user":
        print(f"LGN-05 : {user} -> {get_error()}")
    else:
        print(f"LGN-05 : {user} (non verrouillé) -> {get_error()}")

driver.quit()
