import os
import unittest

import itertools
import networkx as nx
from nose import with_setup
from nose.tools import assert_equals, raises

from ..topology import Topology


class LoadTopologyTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.topology = Topology()
        cls.graph = nx.Graph()

        cls.graph.add_node('router1', type='router')
        cls.graph.add_node('router2', type='router')
        cls.graph.add_node('broker1', type='broker')
        cls.graph.add_node('broker2', type='broker')
        cls.graph.add_node('broker3', type='broker')
        cls.graph.add_edge('router2', 'router1', value=10)
        cls.graph.add_edge('router2', 'broker2', value=5)
        cls.graph.add_edge('router2', 'broker3', value=6)
        cls.graph.add_edge('router1', 'broker1', value=7)


    @raises(SystemExit)
    def test_load_empty_graph(self):
        self.topology.load_graph_from_json('qpid_generator/tests/items/empty_graph_test.yml')


    # @TODO - allow all tests and consult outputs
    # def test_load_ref_graph(self):
    #     self.topology.load_graph_from_json('qpid_generator/tests/items/ref_graph_test.yml')
    #
    #     print self.topology.graph.edges()
    #     print self.graph.edges()
    #
    #     assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)


class SmallTopologyTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.topology = Topology()
        cls.graph = nx.Graph()

        cls.graph.add_node('router1', type='router')
        cls.graph.add_node('broker1', type='broker')
        cls.graph.add_node('broker2', type='broker')
        cls.graph.add_edge('router1', 'broker1', value=1)
        cls.graph.add_edge('router1', 'broker2', value=1)

        cls.routers = ['router1']
        cls.brokers = ['broker1', 'broker2']


    def teardown_edges(self):
        self.graph.add_edge('broker1', 'broker2', value=1)

    def test_load_graph(self):
        self.topology.load_graph_from_json('qpid_generator/tests/items/graph_test.yml')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

    def test_create_line(self):
        self.topology.create_graph(self.routers, self.brokers, 'line_graph')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

    def test_create_line_mixed(self):
        self.topology.create_graph(self.routers, self.brokers, 'line_mix_graph')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

    def test_create_bus(self):
        self.topology.create_graph(self.routers, self.brokers, 'bus_graph')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

        # def test_create_complete(self):
        #     self.topology.create_graph(self.routers, self.brokers, 'complete_graph')
        #     assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)


class BiggerTopologyTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.topology = Topology()
        cls.graph = nx.Graph()

        cls.routers = ['router1', 'router2']
        cls.brokers = ['broker1', 'broker2', 'broker3']

    def setUp(self):
        self.graph.add_node('router1', type='router')
        self.graph.add_node('router2', type='router')
        self.graph.add_node('broker1', type='broker')
        self.graph.add_node('broker2', type='broker')
        self.graph.add_node('broker3', type='broker')

    def tearDown(self):
        # for edge in self.graph.edges():
        self.graph.clear()

    def test_crete_line_mix(self):
        self.graph.add_edge('router1', 'broker1', value=1)
        self.graph.add_edge('router1', 'broker2', value=1)
        self.graph.add_edge('broker2', 'router2', value=1)
        self.graph.add_edge('router2', 'broker3', value=1)

        self.topology.create_graph(self.routers, self.brokers, 'line_mix_graph')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

    def test_create_bus(self):
        self.graph.add_edge('router1', 'broker1', value=1)
        self.graph.add_edge('router1', 'router2', value=1)
        self.graph.add_edge('router2', 'broker2', value=1)
        self.graph.add_edge('router1', 'broker3', value=1)

        self.topology.create_graph(self.routers, self.brokers, 'bus_graph')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

    def test_create_line(self):
        self.graph.add_edge('router1', 'router2', value=1)
        self.graph.add_edge('broker2', 'broker3', value=1)
        self.graph.add_edge('broker3', 'router2', value=1)
        self.graph.add_edge('router1', 'broker1', value=1)

        self.topology.create_graph(self.routers, self.brokers, 'line_graph')
        assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)

        # @with_setup(setup_complete, teardown_edges())
        # def test_crete_complete(self):
        #     self.topology.create_graph(self.routers, self.brokers, 'complete_graph')
        #     assert_equals(nx.is_isomorphic(self.graph, self.topology.graph), True)