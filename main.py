from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class Product:
    def __init__(self, url, lifetime, is_img_exist):
        self.url = url
        self.lifetime = int(lifetime)
        self.is_img_exist = is_img_exist


def get_products_urls(driver, url: str):
    """Забирает со страницы все ссылки на товары и сохраняет их в коллекцию."""
    driver.get(url=url)
    time.sleep(3)
    products = driver.find_elements(by=By.CLASS_NAME, value="product_anker")
    links_on_products = set()
    for product in products:
        links_on_products.add(product.get_attribute('href'))
    return links_on_products


def get_info_from_products_urls(driver, urls: set):
    """Собирает данные со страниц товаров и сохраняет их в объекте"""
    products = []
    for url in urls:
        driver.get(url)
        time.sleep(3)
        # беру последнюю строчку div-а с id tab-1 разбиваю ее по пробелам и забираю предпоследний элемент
        lifetime = driver.find_element(
            by=By.ID,
            value='tab-1',
        ).text.split('\n')[-1].split(' ')[-2]

        try:
            driver.find_element(by=By.CLASS_NAME, value='imgCont')
            is_img_exist = True
        except NoSuchElementException:
            is_img_exist = False

        products.append(Product(url=url, lifetime=lifetime, is_img_exist=is_img_exist))
    return products


def condition_check(products: list):
    """Проверяет объект продукта на соответсвие условиям, при соответсвии записывает в result.txt"""
    with open('result.txt', 'w') as file:
        for product in products:
            if product.lifetime < 10 or product.is_img_exist is False:
                file.write(f'{product.url}\n')


def main():
    driver = webdriver.Chrome()
    try:
        products_urls = get_products_urls(
            driver=driver,
            url="https://stilsoft.ru/products/kitsoz-synerget",
        )
        products = get_info_from_products_urls(driver=driver, urls=products_urls)
        condition_check(products)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
