import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def get_product_details(url):
    driver.get(url)
    time.sleep(3)

    try:
        product_name = driver.find_element(By.CSS_SELECTOR, "#productTitle").text.strip()
    except:
        product_name = None

    try:
        product_price = driver.find_element(By.CSS_SELECTOR, ".a-section.a-spacing-none.aok-align-center .a-price-whole").text
    except:
        product_price = None

    try:
        product_rating_element = driver.find_element(By.XPATH, "//*[@id='acrPopover']/span[1]/a/i[1]")
        product_rating = float(product_rating_element.get_attribute("innerText").split()[0])
    except:
        product_rating = None

    try:
        see_all_reviews_link = driver.find_element(By.XPATH, "//*[@id='reviews-medley-footer']/div[2]/a")
        product_reviews = None

        driver.execute_script("window.open(arguments[0], '_blank');", see_all_reviews_link.get_attribute("href"))
        
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(5)

        review_count_element = driver.find_element(By.CSS_SELECTOR, "div[data-hook='cr-filter-info-review-rating-count']")
        review_text = review_count_element.text

        review_parts = review_text.split(',')
        product_reviews = review_parts[1].strip().split()[0]

    except:
        product_reviews = None

    driver.switch_to.window(driver.window_handles[0])

    return {
        'Product Name': product_name,
        'Product Price': product_price,
        'Rating (out of 5)': product_rating,
        'Number of Reviews': product_reviews
    }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

num_pages = 20

data = []
for page in range(1, num_pages + 1):
    base_url = "https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1690046189&sprefix=ba%2Caps%2C283&ref=sr_pg_{}".format(page, page)

    driver.get(base_url)

    time.sleep(5)

    product_elements = driver.find_elements(By.XPATH, "//div[contains(@data-component-type, 's-search-result')]")

    product_urls = []
    for product_element in product_elements:
        try:
            product_url = product_element.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline").get_attribute("href")
            product_urls.append(product_url)
        except Exception as e:
            print(f"Error occurred while extracting product URL: {e}")

    for url in product_urls:
        product_data = get_product_details(url)
        data.append(product_data)

driver.quit()

df = pd.DataFrame(data)
df.to_csv('amazon_bags_data.csv', index=False)
