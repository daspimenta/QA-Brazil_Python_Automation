from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code
import time

class UrbanRoutesPage:
    # Seção De e Para
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Fluxo de chamada de táxi
    taxi_option = (By.XPATH, '//button[contains(text(),"Chamar")]')
    comfort_icon = (By.XPATH, '//img[@src="/static/media/kids.075fd8d4.svg"]')
    comfort_active = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')

    # Numero de Telefone
    number_text_locator = (By.CSS_SELECTOR, '.np-button')
    number_enter = (By.ID, 'phone')
    number_confirm = (By.CSS_SELECTOR, '.button.full')
    number_code = (By.ID, 'code')
    code_confirm = (By.XPATH, '//button[contains(text(),"Confirmar")]')
    number_finish = (By.CSS_SELECTOR, '.np-text')


    # Metodo de Pagamento
    add_metodo_pagamento = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card = (By.CSS_SELECTOR, '.pp-plus')
    number_card = (By.ID, 'number')
    code_card = (By.CSS_SELECTOR, 'input.card-input#code')
    add_finish_card = (By.XPATH, '//button[contains(text(),"Adicionar")]')
    close_button_card = (By.CSS_SELECTOR, '.payment-picker.open .close-button')
    confirm_card = (By.CSS_SELECTOR, '.pp-value-text')

    # Adicionar Comentario
    add_comment = (By.ID, 'comment')

    # Pedir cobertor e lenços

    switch_blanket = (By.CSS_SELECTOR, '.switch')
    switch_blanket_active = (By.CSS_SELECTOR,
                             '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw > div > input')


    # Pedir dois sorvetes

    add_icecream = (By.CSS_SELECTOR, '.counter-plus')
    qnt_icecream = (By.CSS_SELECTOR, '.counter-value')

    # Pedir um táxi

    call_taxi_button = (By.CSS_SELECTOR, '.smart-button')
    pop_up = (By.CSS_SELECTOR, '.order-header-title')

    # Construtor

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Métodos CORE POM

    def _find(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def _type(self, locator, text):
        element = self._find(locator)
        element.clear()
        element.send_keys(text)

    # Endereços

    def _get_text(self, locator):
        return self._find(locator).text

    def _get_value(self, locator):
        return self._find(locator).get_attribute('value')

    def enter_locations(self, from_text, to_text):
        self._type(self.from_field, from_text)
        self._type(self.to_field, to_text)

    def get_from_location(self):
        return self._get_value(self.from_field)

    def get_to_location(self):
        return self._get_value(self.to_field)

    # Chamar táxi
    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option).click()

    def click_comfort_icon(self):
        self.driver.find_element(*self.comfort_icon).click()

    def click_comfort_active(self):
        try:
            active_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.comfort_active))
            return "active" in active_button.get_attribute("class")
        except:
            return False

    def click_phone_field(self, phone):
        self.driver.find_element(*self.number_text_locator).click()
        self.driver.find_element(*self.number_enter).send_keys(phone)
        self.driver.find_element(*self.number_confirm).click()


        code = retrieve_phone_code(self.driver)
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.number_code)
        )
        code_input.clear()
        code_input.send_keys(code)
        self.driver.find_element(*self.code_confirm).click()


    def confirm_number(self):
        number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.number_finish))
        return number.text

    def click_add_card(self, card, code):
        self.driver.find_element(*self.add_metodo_pagamento).click()
        self.driver.find_element(*self.add_card).click()
        time.sleep(1)
        self.driver.find_element(*self.number_card).send_keys(card)
        time.sleep(1)
        self.driver.find_element(*self.code_card).send_keys(code)
        time.sleep(1)
        self.driver.find_element(*self.add_finish_card).click()
        self.driver.find_element(*self.close_button_card).click()

    def card_confirm(self):
        return self.driver.find_element(*self.confirm_card).text


    def comment_add(self, comment):
        self.driver.find_element(*self.add_comment).send_keys(comment)


    def comment_confirm(self):
        return self.driver.find_element(*self.add_comment).get_attribute('value')


    def blanket_hand_order(self):
        blanket = self.driver.find_element(*self.switch_blanket)
        blanket.click()

    def blanket_hand_active(self):
        blanket_active = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.switch_blanket_active)
        )
        return blanket_active.is_selected()

    def ice_cream_order(self):
        self.driver.find_element(*self.add_icecream).click()

    def ice_cream_verify(self):
        return self.driver.find_element(*self.qnt_icecream).text

    def taxi_call(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def validate_popup(self):
        popup_show = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.pop_up)
        )
        return popup_show.text




