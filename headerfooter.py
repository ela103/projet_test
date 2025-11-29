print("TEST HEADER & FOOTER SAUCEDEMO")

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# --- Liste des utilisateurs à tester ---
USERS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

PASSWORD = "secret_sauce"

# --- Dossier des screenshots ---
SCREENSHOT_FOLDER = "HF_ALL_USERS"
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

# --- Vérifier si un élément existe ---
def element_existe(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except:
        return False

# --- Screenshot utilitaire ---
def screenshot(driver, username, testname):
    folder = f"{SCREENSHOT_FOLDER}/{username}"
    os.makedirs(folder, exist_ok=True)
    driver.save_screenshot(f"{folder}/{testname}.png")

# --- Test principal pour un utilisateur ---
def tester_user(username):

    
    print(f" TEST POUR USER : {username}")
    

    driver = webdriver.Chrome()
    driver.maximize_window()
    time.sleep(1)

    # TC1 — HEADER avant login
    print("\nTC1 : HEADER avant login")
    driver.get("https://www.saucedemo.com")
    time.sleep(2)

    print("Logo :", "PASS" if element_existe(driver, By.CLASS_NAME, "app_logo") else "FAIL")
    print("Titre :", "PASS" if element_existe(driver, By.CLASS_NAME, "login_logo") else "FAIL")
    print("Burger :", "PASS" if not element_existe(driver, By.ID, "react-burger-menu-btn") else "FAIL")
    print("Search :", "PASS" if not element_existe(driver, By.CLASS_NAME, "search_input") else "FAIL")

    screenshot(driver, username, "TC1_HEADER_BEFORE")

    # TC2 — FOOTER avant login
    print("\nTC2 : FOOTER avant login")
    print("Footer :", "PASS" if not element_existe(driver, By.CLASS_NAME, "footer") else "FAIL")
    print("Copyright :", "PASS" if not element_existe(driver, By.CLASS_NAME, "footer_copy") else "FAIL")

    screenshot(driver, username, "TC2_FOOTER_BEFORE")

    # TC3 — Logos sociaux absents avant login
    print("\nTC3 : Logos sociaux avant login")
    logos_avant = [
        ("Twitter", "a[href='https://twitter.com/saucelabs']"),
        ("Facebook", "a[href='https://www.facebook.com/saucelabs']"),
        ("LinkedIn", "a[href='https://www.linkedin.com/company/sauce-labs/']")
    ]

    for nom, selector in logos_avant:
        present = element_existe(driver, By.CSS_SELECTOR, selector)
        print(f"{nom} :", "FAIL" if present else "PASS")

    screenshot(driver, username, "TC3_SOCIAL_BEFORE")

    # TC4 — LOGIN
    print("\nTC4 : Tentative de login")

    try:
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Cas particulier : locked_out_user → LOGIN FAIL attendu
        if username == "locked_out_user":
            error = element_existe(driver, By.CSS_SELECTOR, "h3[data-test='error']")
            if error:
                print("PASS : locked_out_user NE PEUT PAS se connecter (comportement attendu)")
            else:
                print("FAIL : locked_out_user a pu se connecter !")
            screenshot(driver, username, "TC4_LOGIN")
            driver.quit()
            return

        print("PASS : Login réussi")
    except:
        print("FAIL : Login impossible")

    screenshot(driver, username, "TC4_LOGIN")

    # TC5 — HEADER après login
    print("\nTC5 : HEADER après login")

    print("Logo :", "PASS" if element_existe(driver, By.CLASS_NAME, "app_logo") else "FAIL")
    print("Burger :", "PASS" if element_existe(driver, By.ID, "react-burger-menu-btn") else "FAIL")
    print("Panier :", "PASS" if element_existe(driver, By.CLASS_NAME, "shopping_cart_link") else "FAIL")
    print("Search Bar :", "PASS" if not element_existe(driver, By.CLASS_NAME, "search_input") else "FAIL")

    screenshot(driver, username, "TC5_HEADER_AFTER")

    # TC6 — FOOTER après login
    print("\nTC6 : FOOTER après login")

    print("Footer :", "PASS" if element_existe(driver, By.CLASS_NAME, "footer") else "FAIL")
    print("Copyright :", "PASS" if element_existe(driver, By.CLASS_NAME, "footer_copy") else "FAIL")

    screenshot(driver, username, "TC6_FOOTER_AFTER")

    # TC7 — Logos sociaux après login
    print("\nTC7 : Logos sociaux après login")

    social_tests = [
        ("Twitter", "a[href='https://twitter.com/saucelabs']", "twitter.com"),
        ("Facebook", "a[href='https://www.facebook.com/saucelabs']", "facebook.com"),
        ("LinkedIn", "a[href='https://www.linkedin.com/company/sauce-labs/']", "linkedin.com")
    ]

    for nom, selector, attendu in social_tests:
        try:
            onglet = driver.current_window_handle
            driver.find_element(By.CSS_SELECTOR, selector).click()
            time.sleep(2)

            for h in driver.window_handles:
                if h != onglet:
                    driver.switch_to.window(h)
                    break

            url = driver.current_url
            if attendu in url:
                print(f"PASS : {nom} pointe vers {attendu}")
            else:
                print(f"FAIL : Mauvaise URL pour {nom} ({url})")

            screenshot(driver, username, f"TC7_{nom}")
            driver.close()
            driver.switch_to.window(onglet)

        except:
            print(f"FAIL : Impossible de tester {nom}")

    # TC8 — COPYRIGHT
    print("\nTC8 : Vérification copyright")

    try:
        txt = driver.find_element(By.CLASS_NAME, "footer_copy").text
        if "©" in txt:
            print("PASS : Copyright")
        else:
            print("FAIL : Texte incorrect")

        screenshot(driver, username, "TC8_COPYRIGHT")
    except:
        print("FAIL : Élément introuvable")

    driver.quit()


#Lancer les tests pour tous les utilisateurs
for user in USERS:
    tester_user(user)