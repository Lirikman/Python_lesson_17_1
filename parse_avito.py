import undetected_chromedriver
import time


try:
    driver = undetected_chromedriver.Chrome()
    driver.get('https://www.avito.ru/all/vakansii?cd=1&q=python')
    time.sleep(10)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


