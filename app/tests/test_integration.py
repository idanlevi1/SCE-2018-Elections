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

class IntegrationTests(LiveServerTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        db.init_app(app)
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        db.session.commit()
        admon1 = User('tomer', 'admon', 1111)
        idan1 = User('idan', 'levi', 3333)
        avoda1 = Party(u'העבודה','https://www.am-1.org.il/wp-content/uploads/2015/03/%D7%94%D7%A2%D7%91%D7%95%D7%93%D7%94.-%D7%A6%D7%99%D7%9C%D7%95%D7%9D-%D7%99%D7%97%D7%A6.jpg')
        likud1 = Party(u'הליכוד','https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Likud_Logo.svg/250px-Likud_Logo.svg.png')
        lavan1 = Party(u'פתק לבן','https://www.weberthai.com/fileadmin/user_upload/01_training-elements/02.4_others/02.5_color_cards/05_color_mosaic/images/1.jpg')
        db.session.add(admon1)
        db.session.add(idan1)
        db.session.add(avoda1)
        db.session.add(likud1)
        db.session.add(lavan1)
        db.session.commit()

     #   self.driver = webdriver.Chrome()
        self.driver = webdriver.PhantomJS()
        self.driver.get(self.get_server_url())
     #   self.driver.get('http://localhost:5000/')
        self.driver.maximize_window()
        delay = 3  # seconds...

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

    def test_full_choice(self):
        firstName, lastName, id = "idan", "levi", 3333
        elem = self.driver.find_element_by_css_selector('body > div > form > input.btn.btn-default')  # submit button
        firstNameInputElement = self.driver.find_element_by_id("first_name")
        firstNameInputElement.send_keys(firstName)
        lastNameInputElement = self.driver.find_element_by_id("last_name")
        lastNameInputElement.send_keys(lastName)
        idInputElement = self.driver.find_element_by_css_selector('#id')
        idInputElement.send_keys(id)
        idInputElement.send_keys(Keys.ENTER)
        time.sleep(2)
        #index page
        self.driver.find_element_by_css_selector('#someParty > label > div > div > img').click()
        self.driver.find_element_by_css_selector('body > div.container > form > div.submitbote > button').click()
        time.sleep(2)
        # confirm page
        self.driver.find_element_by_css_selector('body > div > form > div > button.btn.btn-lg.btn-success').click()
        # back to main page
        time.sleep(2)
        firstName, lastName, id = "idan", "levi", 3333
        elem = self.driver.find_element_by_css_selector('body > div > form > input.btn.btn-default')  # submit button
        firstNameInputElement = self.driver.find_element_by_id("first_name")
        firstNameInputElement.send_keys(firstName)
        lastNameInputElement = self.driver.find_element_by_id("last_name")
        lastNameInputElement.send_keys(lastName)
        idInputElement = self.driver.find_element_by_css_selector('#id')
        idInputElement.send_keys(id)
        idInputElement.send_keys(Keys.ENTER)
        time.sleep(2)
        assert 'Home' not in self.driver.title

    def tearDown(self):
        self.driver.quit()
        with app.app_context():
        #    db.drop_all()
            db.session.remove()

if __name__ == "__main__":
    unittest.main()