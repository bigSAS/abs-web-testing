from abs.pages import Page
from abs.actions import Actions
from abs.elements import FluentFinder, Locator, Using
from abs.conditions import XpathExists
import yaml
import logging
from selenium import webdriver
from abs import expected_conditions as EC
from time import sleep
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]\t[%(levelname)s]\t[%(name)s]\t%(message)s"
)

logging.getLogger('abs-actions').setLevel(logging.INFO)
logging.getLogger('abs-finder').setLevel(logging.DEBUG)

# todo: formatting logs


class SasKodzi(Page):
    """ Sample POP Page """
    url = 'https://sas-kodzi.pl'
    
    # locators
    BLOG_BUTTON = Locator(Using.XPATH, '//a[@href="/blog"]')
    POST_BUTTON = Locator(Using.XPATH, "//section[@class='blog-post' and contains(., '{post_title}')]//a[contains(., 'Czytaj dalej')]")

    def goto_posts(self) -> None:
        self.actions.click(self.BLOG_BUTTON.get_by(), timeout=3)
        self.actions.wait_for(XpathExists('//body'))

    def open_post(self, post_title: str) -> None:
        self.actions.click(self.POST_BUTTON.get_by(post_title=post_title), condition=EC.visibility_of_element_located)
        self.actions.wait_for(XpathExists('//body'), timeout=50)


@dataclass
class Config:
    wd_path: str
    find_element_timeout: int
    wait_for_condition_timeout: int
    wait_between: int


def get_config() -> Config:
    with open('example.config.yaml', 'r', encoding='utf-8') as c:
        data = yaml.load(c, Loader=yaml.FullLoader)
        return Config(**data)

if __name__ == '__main__':
    config = get_config()
    driver = webdriver.Chrome(executable_path=config.wd_path)
    driver.maximize_window()
    finder = FluentFinder(webdriver=driver, default_timeout=config.find_element_timeout)
    actions = Actions(
        finder=finder,
        wait_for_condition_timeout=config.wait_for_condition_timeout,
        wait_between=config.wait_between
    )

    sas_kodzi_page = SasKodzi(actions)
    sas_kodzi_page.open()
    sas_kodzi_page.goto_posts()
    sas_kodzi_page.open_post('Python od zera pt2 - proste typy danych')

    driver.quit()
