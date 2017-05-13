# -*- coding: utf-8 -*-

import selenium.common
import selenium.webdriver

from nose.tools import assert_equal, assert_false, assert_true, raises

from .. import documents, repositories, download_strategies


class TestSerializableDecorator(object):

    def __init__(self):
        self.document = None
        self.repository = None

    def setup(self):
        string = """
<head>
  <div class="foo">Foo</div>
  <div class="bar">Bar</div>
</head>"""

        length = 32
        generate_id_strategy = repositories.random_alphanumeric_strings(
            length=length)
        repository = repositories.Default(
            generate_id_strategy=generate_id_strategy)

        self.document = documents.LXmlDocument.from_string(string)
        self.repository = download_strategies.SerializableDecorator(
            repository=repository,
            serializable=documents.LXmlDocument)

    def test_get_return_value_is_same_entity(self):
        input_entity = expected_entity = self.document
        entity_id = self.repository.add(entity=input_entity)
        output_entity = self.repository.get(entity_id=entity_id)
        assert_equal(output_entity.to_string(), expected_entity.to_string())

    @raises(repositories.EntityNotFound)
    def test_get_raises_entity_not_found(self):
        self.repository.get(entity_id=None)


class NopDownloadStrategy(download_strategies.Base):

    def do_download(self):
        pass


class TestBase(object):

    def __init__(self):
        self.web_driver = None
        self.strategy = None

    def setup(self):
        length = 32
        generate_id_strategy = repositories.random_alphanumeric_strings(
            length=length)
        repository = repositories.Default(
            generate_id_strategy=generate_id_strategy)

        self.web_driver = selenium.webdriver.Chrome()
        self.strategy = NopDownloadStrategy(web_driver=self.web_driver,
                                            page_timeout=None,
                                            repository=repository)

    @raises(download_strategies.HttpError)
    def test_download_server_error_raises_http_error(self):
        url = self.construct_url(path='server_error')
        self.strategy.download(url=url)

    @raises(download_strategies.DownloadFailed)
    def test_download_expired_room_raises_download_failed(self):
        url = self.construct_url(path='expired_room')
        self.strategy.download(url=url)

    def test_confirm_rendered_page_title_correct_content(self):
        self.set_web_driver_page(path='title_correct_content')
        self.strategy._confirm_rendered_page(timeout=None)

    @raises(selenium.common.exceptions.TimeoutException)
    def test_confirm_rendered_page_title_incorrect_content(self):
        self.set_web_driver_page(path='title_incorrect_content')
        self.strategy._confirm_rendered_page(timeout=None)

    def test_confirm_server_error_correct_css_selector(self):
        self.set_web_driver_page(path='server_error_correct_css_selector')
        encountered_server_error = self.strategy._confirm_server_error(
            timeout=None)
        assert_false(encountered_server_error)

    def test_confirm_server_error_correct_css_selector_and_content(self):
        self.set_web_driver_page(path='server_error_correct_css_selector_and_content')
        encountered_server_error = self.strategy._confirm_server_error(
            timeout=None)
        assert_true(encountered_server_error)

    def set_web_driver_page(self, path):
        url = self.construct_url(path=path)
        self.web_driver.get(url=url)

    @staticmethod
    def construct_url(path):
        url = 'http://127.0.0.1:9090/{}/'.format(path)
        return url

    def teardown(self):
        self.strategy.dispose()
