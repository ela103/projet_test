import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ============================================================
# Configuration générale
# ============================================================

USERS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

PASSWORD = "secret_sauce"

# Créer un dossier global screenshots
GLOBAL_DIR = "screenshots_by_user"
os.makedirs(GLOBAL_DIR, exist_ok=True)


# ============================================================
# Fonction générique d'affichage des résultats
# ============================================================

def result(tc_id, ok, message, user):
    status = "PASS" if ok else "FAIL"
    print(f"[{user}] {tc_id} : {status} – {message}")


# ============================================================
# Toutes les fonctions de test (réutilisées pour chaque user)
# ============================================================

def check_name_sort(driver, user, order="asc", screenshot_dir=""):
    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names = [p.text for p in products]
    sorted_names = sorted(names) if order == "asc" else sorted(names, reverse=True)

    passed = (names == sorted_names)
    result("TC-01" if order=="asc" else "TC-02",
           passed,
           f"Tri Name {order} correct",
           user)

    driver.save_screenshot(f"{screenshot_dir}/Name_{order}.png")
    return passed


def check_price_sort(driver, user, order="asc", screenshot_dir=""):
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices_float = [float(p.text.replace("$", "")) for p in prices]
    sorted_prices = sorted(prices_float) if order == "asc" else sorted(prices_float, reverse=True)

    passed = (prices_float == sorted_prices)
    result("TC-03" if order=="asc" else "TC-04",
           passed,
           f"Tri Price {order} correct",
           user)

    driver.save_screenshot(f"{screenshot_dir}/Price_{order}.png")
    return passed


def check_about_link(driver, user, screenshot_dir):
     # TC-05: Vérifie que le lien "About" du menu fonctionne
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        ).click()

        time.sleep(1)
        driver.find_element(By.ID, "about_sidebar_link").click()
        time.sleep(2)

        passed = ("saucelabs.com" in driver.current_url)
        result("TC-05", passed, "Lien About OK", user)

        driver.save_screenshot(f"{screenshot_dir}/About.png")
        driver.back()
        time.sleep(1)
        return passed

    except:
        result("TC-05", False, "Lien About cassé", user)
        driver.save_screenshot(f"{screenshot_dir}/About_FAIL.png")
        return False


def test_add_product_then_reset(driver, user, screenshot_dir):
    try:
        # TC-06 : Ajouter produit
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        time.sleep(1)
        passed_add = "Remove" in driver.find_element(By.ID, "remove-sauce-labs-backpack").text
        result("TC-06", passed_add, "Produit ajouté", user)

        # TC-07 : compteur
        cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        passed_count = (cart_count == "1")
        result("TC-07", passed_count, "Compteur correct", user)

        # TC-08 : Reset
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
        ).click()
        time.sleep(1)
        driver.find_element(By.ID, "reset_sidebar_link").click()
        time.sleep(1)

        cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        passed_reset = (len(cart_badge) == 0)
        result("TC-08", passed_reset, "Reset OK", user)

        driver.save_screenshot(f"{screenshot_dir}/Reset.png")
        return passed_add and passed_count and passed_reset

    except:
        result("TC-06/07/08", False, "Erreur dans ajout ou reset", user)
        driver.save_screenshot(f"{screenshot_dir}/Add_Reset_FAIL.png")
        return False


def test_search_bar_absence(driver, user, screenshot_dir):
     # TC-09:Verifier la  barre de recherche
    try:
        driver.find_element(By.CSS_SELECTOR, "input[type='search'], #search, .search, .search-input")
        result("TC-09", False, "Barre recherche existe (FAIL attendu)", user)
        return False
    except:
        result("TC-09", True, "Pas de barre de recherche", user)
        driver.save_screenshot(f"{screenshot_dir}/SearchBar_OK.png")
        return True


def test_logout(driver, user, screenshot_dir):
    # TC-10: Vérifie la déconnexion
    try:
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        driver.find_element(By.ID, "logout_sidebar_link").click()
        time.sleep(2)

        passed = ("saucedemo.com" in driver.current_url)
        result("TC-10", passed, "Logout OK", user)
        driver.save_screenshot(f"{screenshot_dir}/Logout.png")
        return passed

    except:
        result("TC-10", False, "Logout FAIL", user)
        driver.save_screenshot(f"{screenshot_dir}/Logout_FAIL.png")
        return False


# ============================================================
# EXÉCUTION DES TESTS POUR CHAQUE UTILISATEUR
# ============================================================

for user in USERS:

    print("\n========================================")
    print(f" DÉBUT DES TESTS POUR USER : {user}")
    print("========================================\n")

    # Dossier screenshots spécifique à l'utilisateur
    user_dir = os.path.join(GLOBAL_DIR, user)
    os.makedirs(user_dir, exist_ok=True)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com")

    # Login
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    # Cas particulier : locked_out_user → login refuse
    if "locked_out" in user and "inventory" not in driver.current_url:
        result("LOGIN", False, "Utilisateur bloqué (normal)", user)
        driver.save_screenshot(f"{user_dir}/LockedOut.png")
        driver.quit()
        continue

    # Si la connexion échoue → passer au suivant
    if "inventory" not in driver.current_url:
        result("LOGIN", False, "Échec connexion", user)
        driver.save_screenshot(f"{user_dir}/Login_FAIL.png")
        driver.quit()
        continue

    # Tests TC-01 à TC-10
    try:
        # Tri
        Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Name (A to Z)")
        time.sleep(1)
        check_name_sort(driver, user, "asc", user_dir)

        Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Name (Z to A)")
        time.sleep(1)
        check_name_sort(driver, user, "desc", user_dir)

        Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Price (low to high)")
        time.sleep(1)
        check_price_sort(driver, user, "asc", user_dir)

        Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_visible_text("Price (high to low)")
        time.sleep(1)
        check_price_sort(driver, user, "desc", user_dir)

        # Lien About
        check_about_link(driver, user, user_dir)

        # Ajout + reset
        test_add_product_then_reset(driver, user, user_dir)

        # Barre recherche
        test_search_bar_absence(driver, user, user_dir)

        # Logout
        test_logout(driver, user, user_dir)

    except Exception as e:
        print(f"[{user}] ERREUR GÉNÉRALE :", e)

    driver.quit()

print("\n======= FIN DE TOUS LES TESTS =======")
