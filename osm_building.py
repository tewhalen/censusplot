import overpy


def query_buildings(buildings):
    q = """
    [timeout:25];
    (
      {}
       );
       (._;>;);
    out body;
    """
    query_format = 'way["addr:housenumber"="{}"]["addr:street:name"="{}"]["addr:street:prefix"="{}"];'
    queries = []
    for number, direction, street in buildings:
        queries.append(query_format.format(number, street, direction))

    api = overpy.Overpass()
    return api.query(q.format("\n".join(queries)))


def main():
    nodes = query_buildings([(1917, "West","Berwyn"),
                            (1911,"West","Berwyn")]).ways[0].get_nodes()

    for n in nodes:
        print((float(n.lat), float(n.lon)))

if __name__ == '__main__':
    main()
