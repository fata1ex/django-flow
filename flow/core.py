# coding: utf-8

from flow.models import FlowConfiguration


class BaseElement(object):
    flow = None
    element_class = None
    template_name = 'flow/object_item.html'

    def __init__(self, flow, count):
        super(BaseElement, self).__init__()
        self.flow = flow
        self.count = int(count)

    def objects(self):
        raise NotImplementedError

    @classmethod
    def element_class_list(cls):
        return list(cls.__subclasses__())

    @property
    def flow_template_name(self):
        return self.template_name


class Flow(object):
    _configuration = None

    template_name = 'flow/object_list.html'
    template_empty_block = 'flow/empty_block.html'

    def __init__(self):
        super(Flow, self).__init__()

        self.element_list = []
        self.populate_flow()

    def add(self, element):
        self.element_list.append(element)

    @classmethod
    def element_class_list(cls):
        return BaseElement.element_class_list()

    @property
    def configuration(self):
        if not self._configuration:
            self._configuration = FlowConfiguration.get_configuration()

        return self._configuration

    def populate_flow(self):
        element_class_map = {
            element.element_class.__name__: element
            for element in self.__class__.element_class_list()
        }

        for element_name, element_count in self.configuration['element_list'].iteritems():
            element = element_class_map.get(element_name)
            if element:
                self.add(element(self, int(element_count)))

    def _get_object_iterator(self):
        for element in self.element_list:
            for obj in element.objects()[:element.count]:
                obj.flow_template_name = element.template_name
                yield obj

    def objects(self):
        return self._get_object_iterator()

    def object_list(self):
        return list(self._get_object_iterator())
