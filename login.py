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
        time.sleep(0.2)
    except:
        pass

# --- RESET PAGE LOGIN ---
def reset_page():
    driver.get("https://www.saucedemo.com/")
    wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    wait.until(EC.visibility_of_element_located((By.ID, "password")))
    wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    close_error()

# --- RÉCUPÉRER L'ERREUR (robuste, pas de wait.until) ---
def get_error():
    time.sleep(0.5)  # laisser le message apparaître
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        msg = elem.text.strip()
        print("DEBUG : message d'erreur trouvé ->", msg)
        return msg
    except:
        print("DEBUG : aucun message d'erreur trouvé")
        return ""

# ================================
#     TESTS LOGIN
# ================================

# LGN-01 : Login valide
reset_page()
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
wait.until(EC.url_contains("inventory.html"))
print("LGN-01 PASS")

# LGN-02 : mauvais mot de passe
reset_page()
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("wrong_password")
driver.find_element(By.ID, "login-button").click()
error = get_error()
print("LGN-02 message d'erreur :", error)
assert "Epic sadface" in error
print("LGN-02 PASS")

# LGN-03 : username vide
reset_page()
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
error = get_error()
print("LGN-03 message d'erreur :", error)
assert "Username is required" in error
print("LGN-03 PASS")

# LGN-04 : password vide
reset_page()
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "login-button").click()
error = get_error()
print("LGN-04 message d'erreur :", error)
assert "Password is required" in error
print("LGN-04 PASS")




# LGN-05 : utilisateur verrouillé
reset_page()
driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
error = get_error()
print("LGN-05 message d'erreur :", error)
assert "locked out" in error.lower()
print("LGN-05 PASS")


# Fermeture
driver.quit()
