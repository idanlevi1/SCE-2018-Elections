import unittest
from selenium import webdriver
from app import db, app
from app.models import User,Party
from selenium.webdriver.common.keys import Keys
from flask_testing import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class IntegrationTests(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        db.init_app(app)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        db.session.commit()
        admon1 = User('tomer', 'admon', 1111)
        avoda1 = Party(u'העבודה','http://www.havoda.org.il/wp-content/themes/mega_theme_havoda/images/logo.png')
        likud1 = Party(u'הליכוד','https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Likud_Logo.svg/250px-Likud_Logo.svg.png')
        lavan1 = Party(u'פתק לבן','https://www.weberthai.com/fileadmin/user_upload/01_training-elements/02.4_others/02.5_color_cards/05_color_mosaic/images/1.jpg')
        db.session.add(admon1)
        db.session.add(avoda1)
        db.session.add(likud1)
        db.session.add(lavan1)
        db.session.commit()

        self.driver = webdriver.PhantomJS()
        self.driver.get(self.get_server_url())
        self.driver.maximize_window()
        delay = 3  # seconds
    @TESTING
    def test_login_user(self):
        firstName, lastName, id = "tomer", "admon", 1111
        elem = self.driver.find_element_by_css_selector('body > div > form > input.btn.btn-default')  # submit button
        firstNameInputElement = self.driver.find_element_by_id("first_name")
        firstNameInputElement.send_keys(firstName)
        lastNameInputElement = self.driver.find_element_by_id("last_name")
        lastNameInputElement.send_keys(lastName)
        idInputElement = self.driver.find_element_by_css_selector('#id')
        idInputElement.send_keys(id)
        idInputElement.send_keys(Keys.ENTER)
        #elem.click()  # submit button
        time.sleep(2)
        assert 'Home' in self.driver.title
    @TESTING
    def test_user_not_in_database(self):
        firstName, lastName, id = "aaa", "bbb", 900
        elem = self.driver.find_element_by_css_selector('body > div > form > input.btn.btn-default')  # submit button
        firstNameInputElement = self.driver.find_element_by_id("first_name")
        firstNameInputElement.send_keys(firstName)
        lastNameInputElement = self.driver.find_element_by_id("last_name")
        lastNameInputElement.send_keys(lastName)
        idInputElement = self.driver.find_element_by_css_selector('#id')
        idInputElement.send_keys(id)
        idInputElement.send_keys(Keys.ENTER)
        #elem.click()  # submit button
        time.sleep(2)
       # assert 'Home' not in self.driver.title
        assert self.driver.find_element_by_id("error").text == 'error: User not found!'

    def tearDown(self):
        self.driver.quit()
        with app.app_context():
        #    db.drop_all()
            db.session.remove()

if __name__ == "__main__":
    unittest.main()
