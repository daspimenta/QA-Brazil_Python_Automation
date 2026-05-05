import data
import helpers
import time

from pages import UrbanRoutesPage
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # não modifique, pois precisamos do registro adicional habilitado para recuperar o código de confirmação do telefone
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = Chrome()
        cls.driver.implicitly_wait(5)


        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_taxi_option()
        self.page.click_comfort_icon()


    def test_set_route(self):
        assert self.page.get_from_location() == data.ADDRESS_FROM
        assert self.page.get_to_location() == data.ADDRESS_TO
        time.sleep(10)

    def test_select_plan(self):
        assert self.page.click_comfort_active()
        time.sleep(10)

    def test_fill_phone_number(self):
        self.page.click_phone_field(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER in self.page.confirm_number()
        time.sleep(10)


    def test_fill_card(self):
        self.page.click_add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert "Cartão" in self.page.card_confirm()
        time.sleep(10)

    def test_comment_for_driver(self):
        self.page.comment_add(data.MESSAGE_FOR_DRIVER)
        assert data.MESSAGE_FOR_DRIVER in self.page.comment_confirm()
        time.sleep(10)

    def test_order_blanket_and_handkerchiefs(self):
        self.page.blanket_hand_order()
        assert self.page.blanket_hand_active() is True
        time.sleep(10)


    def test_order_2_ice_creams(self):
        for _ in range(2):
            self.page.ice_cream_order()
        assert int(self.page.ice_cream_verify()) == 2
        time.sleep(10)


    def test_car_search_model_appears(self):
        #Adicionar em S8
        pass
        print("função criada para buscar modelo do carro")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()