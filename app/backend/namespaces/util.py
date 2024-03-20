def add_routes(namespace, routes):
    for route, resource in routes.items():
        namespace.add_resource(resource, route)
