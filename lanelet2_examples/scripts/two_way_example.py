#!/usr/bin/env python
import os
import lanelet2
from lanelet2.projection import UtmProjector

example_file = "src/lanelet2/lanelet2_maps/res/mapping_example.osm"
# example_file = "lanelet2_maps/res/mapping_example.osm"
example_file = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), "../../lanelet2_maps/res/mapping_example.osm")
projector = UtmProjector(lanelet2.io.Origin(49, 8.4))
lanelet_map = lanelet2.io.load(example_file, projector)

traffic_rules = lanelet2.traffic_rules.create(lanelet2.traffic_rules.Locations.Germany,
                                                   lanelet2.traffic_rules.Participants.Vehicle)
graph = lanelet2.routing.RoutingGraph(lanelet_map, traffic_rules)

graph.exportGraphML("routing_graph.graphml")
graph.exportGraphViz("routing_graph.graphviz")

debug_map = graph.getDebugLaneletMap()
lanelet2.io.write("debug_map.osm", debug_map, projector)


lanelet_in_roundabout = lanelet_map.laneletLayer[45334]
lanelet_before_roundabout = lanelet_map.laneletLayer[45356]
lanelet_on_road_before = lanelet_map.laneletLayer[45358]

assert(len(graph.following(lanelet_before_roundabout)) == 1)
assert(len(graph.following(lanelet_on_road_before)) == 1)
assert(len(graph.possiblePaths(lanelet_before_roundabout, 100, 0, True)) == 1)
assert(graph.getRoute(lanelet_before_roundabout, lanelet_in_roundabout)  == None)
assert(graph.getRoute(lanelet_on_road_before, lanelet_before_roundabout) == None)
assert(graph.getRoute(lanelet_before_roundabout, lanelet_on_road_before) != None) # route along lane
assert((lanelet_in_roundabout.id in [lanelet.id for lanelet in graph.reachableSet(lanelet_before_roundabout, 100, 0, True)]) == False)
