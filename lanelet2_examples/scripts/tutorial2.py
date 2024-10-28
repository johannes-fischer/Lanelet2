#!/usr/bin/env python
import os
import lanelet2
from lanelet2.projection import UtmProjector

example_file = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), "../../lanelet2_maps/res/mapping_example.osm")

projector = UtmProjector(lanelet2.io.Origin(49, 8.4))
map = lanelet2.io.load(example_file, projector)
traffic_rules = lanelet2.traffic_rules.create(lanelet2.traffic_rules.Locations.Germany,  lanelet2.traffic_rules.Participants.Vehicle)
graph = lanelet2.routing.RoutingGraph(map, traffic_rules)
lanelet = map.laneletLayer[4984315]
toLanelet = graph.following(lanelet)[0]
print(graph.routingRelation(lanelet, toLanelet))