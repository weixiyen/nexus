def topsort(data):
    extra_items_in_deps = set()

    for value in data.values():
        if value is not None:
            extra_items_in_deps.add(value)

    extra_items_in_deps -= set(data.keys())

    data.update({item: set() for item in extra_items_in_deps})

    while True:
        ordered = {item for item, dep in data.items() if not dep}

        if not ordered:
            break

        for thing in ordered:
            yield thing

        data = {item: (({dep} - ordered) if dep else set()) for item, dep in data.items() if item not in ordered}