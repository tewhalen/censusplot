import overpy


def query_buildings(area, buildings):
    """Query OSM for buildings in the proper area, and get all their nodes.

    buildings = [(housenumber, prefix, street),]"""
    q = """
    [timeout:25];
    area[name="{}"];
    (
      {}
       )->.x1;
       (way.x1[building];>;);
    out body;
    """
    query_format = 'way["addr:housenumber"="{}"]["addr:street:name"="{}"]["addr:street:prefix"="{}"];'
    queries = []
    #print(buildings)
    for housenumber, prefix, street in buildings:
        queries.append(query_format.format(housenumber, street, prefix))
    #print(queries)
    api = overpy.Overpass()
    return api.query(q.format(area, "\n".join(queries)))

def query_streets(bbox):
    """query osm for ways in the bbox"""
    q = """
    [timeout:25][bbox:{},{},{},{}];
    (
    way[highway][!service];
    );

    out geom;
    """
    api = overpy.Overpass()
    return api.query(q.format(*bbox))

def main():
    nodes = query_buildings("Chicago",[(1917, "West","Berwyn"),
                            (1911,"West","Berwyn"),
                            (1907,"West","Berwyn"),
                            (1916,"West","Berwyn")])

    for w in nodes.ways:
        print(w.tags)
        for n in w.get_nodes():
            print((float(n.lat), float(n.lon)))

if __name__ == '__main__':
    main()
