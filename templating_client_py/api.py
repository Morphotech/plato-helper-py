from functools import wraps
from http import HTTPStatus
from typing import NamedTuple, Sequence, List, Optional

import requests

from templating_client_py.request_collections import RequestDict


class TemplatingUnavailable(Exception):
    """
    Error to be raised when the API is unavailable.
    """
    ...


class TemplatingError(Exception):
    """
    Error to be raised when the API responds but not as expected.
    """
    ...


def catch_connection_error(f):
    """
    Simple decorator to catch when the connection for templating service fails and raises a TemplatingUnavailable.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionError as e:
            raise TemplatingUnavailable(e)

    return wrapper


class TemplateInfo(NamedTuple):
    """
    Template
    ---
    properties:
        template_id:
            type: string
            description: template id
        template_schema:
            type: object
            description: jsonschema for template
        type:
            type: string
            description: template MIME type
        metadata:
            type: object
            description: a collection on property values defined by the resource owner at the template conception
        tags:
            type: array
            items:
                type: string
    """
    template_id: str
    template_schema: dict
    type: str
    metadata: dict
    tags: List[str]


class TemplatingClient:
    """
    Templating client for the Vizidox templating microservice.

    Attributes:
        templating_host: The docker host for the templating microservice.
    """

    def __init__(
            self,
            templating_host: str
    ):
        self.templating_host = templating_host

    @catch_connection_error
    def templates(self, tags: List[str]) -> Sequence[TemplateInfo]:
        """
        Retrieves your templates from the API.
        :param tags: tags to filter the templates by
        :return: Sequence[TemplateInfo] on all the templates available
        """

        params = dict()

        if tags:
            params["tags"] = tags

        response = requests.get(f"{self.templating_host}/templates/",
                                params=params
                                )

        if response.status_code != HTTPStatus.OK:
            raise TemplatingError(response.status_code, response.text)

        templates = [TemplateInfo(**template_dict) for template_dict in response.json()]

        return templates

    @catch_connection_error
    def template(self, template_id: str) -> TemplateInfo:
        """
        Retrieves the template info with the given id.
        :param template_id: the template id
        :return: TemplateInfo on the template
        """
        response = requests.get(f"{self.templating_host}/templates/{template_id}")

        if response.status_code != HTTPStatus.OK:
            raise TemplatingError(response.status_code, response.text)

        template = TemplateInfo(**response.json())

        return template

    @catch_connection_error
    def compose(self, template_id: str,
                compose_data: dict,
                mime_type="application/pdf",
                page: Optional[int] = None,
                resize_height: Optional[int] = None,
                resize_width: Optional[int] = None
                ) -> bytes:
        """
        Makes a request for the template to be composed and returns the bytes for the file
        :param template_id: the template id
        :param compose_data: dict to compose template with
        :param mime_type: MIME type for the example
        :param page: The number of the page to be printed
        :param resize_width: The height for resizing the template
        :param resize_height: The width for resizing the template
        """
        headers = {**{"accept": mime_type}}
        query_params = RequestDict(page=page, height=resize_height, width=resize_width)
        response = requests.post(f"{self.templating_host}/template/{template_id}/compose",
                                 headers=headers,
                                 json=compose_data,
                                 params=query_params
                                 )

        if response.status_code != HTTPStatus.OK:
            raise TemplatingError(response.status_code, response.text)

        return response.content

    @catch_connection_error
    def template_example(self, template_id: str,
                         mime_type="application/pdf",
                         page: Optional[int] = None,
                         resize_height: Optional[int] = None,
                         resize_width: Optional[int] = None) -> bytes:
        """
        Makes a request for the template to be composed and returns the bytes for the file
        :param template_id: the template id
        :param mime_type: MIME type for the example
        :param page: The number of the page to be printed
        :param resize_width: The height for resizing the template
        :param resize_height: The width for resizing the template
        """
        headers = {**{"accept": mime_type}}
        query_params = RequestDict(page=page, height=resize_height, width=resize_width)

        response = requests.get(f"{self.templating_host}/template/{template_id}/example",
                                headers=headers,
                                params=query_params
                                )

        if response.status_code != HTTPStatus.OK:
            raise TemplatingError(response.status_code, response.text)

        return response.content

    def compose_to_file(self, template_id: str, compose_data: dict, composed_file_target: str, *args, **kwargs):
        """
        Makes a request for the template to be composed and writes the result to a file.
        :param template_id: the template id
        :param compose_data: dict to compose template with
        :param composed_file_target: path to file to be written. Caution: file is overwritten
        :param args: extra arguments to send to compose
        :param kwargs: extra keyword arguments to send to compose
        """
        composed_content = self.compose(template_id, compose_data, *args, **kwargs)

        with open(composed_file_target, mode='wb') as output:
            output.write(composed_content)
