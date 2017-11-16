import overpy


def query_buildings(area, buildings):
    """Query OSM for buildings in the proper area, and get all their nodes.

    buildings = [(number, direction, street),]"""
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
    for number, direction, street in buildings:
        queries.append(query_format.format(number, street, direction))

    api = overpy.Overpass()
    return api.query(q.format(area, "\n".join(queries)))


def main():
    nodes = query_buildings("Chicago",[(1917, "West","Berwyn"),
                            (1911,"West","Berwyn")]).ways[0].get_nodes()

    for n in nodes:
        print((float(n.lat), float(n.lon)))

if __name__ == '__main__':
    main()
