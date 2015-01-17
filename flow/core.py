# coding: utf-8

from random import choice

from flow.models import FlowConfiguration


class FlowException(Exception):
    pass


class FlowConfigurationException(FlowException):
    pass


class FlowElement(object):
    flow = None
    element_class = None
    template_name = 'flow/object_item.html'

    sorting_key = ''

    def __init__(self, flow, page_limit=None):
        super(FlowElement, self).__init__()
        self.flow = flow
        self.page_limit = int(page_limit) if page_limit else None

        self.object_list = []

    def objects(self):
        return self.get_objects()

    def get_objects(self):
        raise NotImplementedError

    @classmethod
    def element_class_list(cls):
        return list(cls.__subclasses__())

    def weight(self, obj):
        if callable(self.sorting_key):
            return self.sorting_key(obj)

        if hasattr(obj, self.sorting_key):
            return getattr(obj, self.sorting_key)

        return None


class Flow(object):
    _configuration = None

    template_name = 'flow/object_list.html'
    template_empty_block = 'flow/empty_block.html'

    def __init__(self, page=None):
        super(Flow, self).__init__()

        self.element_list = []
        self.object_list = []

        try:
            self.page = int(page)
            if self.page < 0:
                raise ValueError

        except (ValueError, TypeError):
            self.page = None

        self.paginate_by = self.configuration.get('paginate_by')
        self.reverse = self.configuration.get('reverse', False)
        self.randomize_same_weight = self.configuration.get('randomize_same_weight', False)

        self.init_flow_elements()

        # self.cache_key = '{0}'.format('flow')

    def add_element(self, element):
        self.element_list.append(element)

    @classmethod
    def element_class_list(cls):
        return FlowElement.element_class_list()

    @property
    def configuration(self):
        # if not self._configuration:
        self._configuration = FlowConfiguration.get_configuration()

        return self._configuration

    def init_flow_elements(self):
        element_class_map = {
            element.element_class.__name__: element
            for element in self.__class__.element_class_list()
        }

        for element in self.configuration.get('elements', []):
            if isinstance(element, (str, unicode)):
                name, page_limit = element, None

            elif isinstance(element, dict):
                name, page_limit = element.items()[0]

            else:
                raise FlowConfigurationException

            element = element_class_map.get(name)
            if element:
                self.add_element(element(self, page_limit=page_limit))

    def objects(self):
        self.object_list = self._get_object_list()
        return self._get_paginated_object_list()

    def _get_object_list(self):
        for element in self.element_list:
            for obj in element.objects():
                obj.flow_element = element
                obj.flow_weight = element.weight(obj)

                self.object_list.append(obj)

        self._sort_object_list()
        return self.object_list

    def _sort_object_list(self):
        self.object_list.sort(cmp=self.cmp, reverse=self.reverse)

    def cmp(self, x, y):
        try:
            if x.flow_weight < y.flow_weight:
                return -1

            if x.flow_weight > y.flow_weight:
                return 1
        except TypeError:
            return 1 if bool(x.flow_weight) else -1

        if self.randomize_same_weight:
            return choice([-1, 0, 1])

        return 0

    def _get_paginated_object_list(self):
        if self.page and self.paginate_by:
            index_start = (self.page - 1) * self.paginate_by
            index_end = self.page * self.paginate_by

            return self.object_list[index_start:index_end]

        return self.object_list
