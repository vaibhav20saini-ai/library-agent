"""Simple multi-book collection planner."""

from algorithms import astar, path_cost


def plan_collection(graph, start, books, positions=None, time_limit=None):
    """
    Plan a route by repeatedly visiting the nearest remaining book shelf.
    Higher priority breaks ties between shelves at the same estimated cost.
    This is a student-friendly greedy heuristic, not a guaranteed global optimum.
    """
    remaining = list(books)
    current = start
    route = [start]
    collected = []
    total_cost = 0
    skipped = []
    details = []

    while remaining:
        candidates = []
        for book in remaining:
            path, _, _, cost = astar(graph, current, book["shelf"], positions)
            if path:
                candidates.append((cost, -int(book.get("priority", 1)), book, path))
        if not candidates:
            skipped.extend(remaining)
            break

        candidates.sort(key=lambda item: (item[0], item[1], item[2]["title"]))
        cost, _, book, path = candidates[0]

        # Estimate one minute per cost unit for a simple demonstration.
        estimated_total = total_cost + cost
        if time_limit is not None and estimated_total > time_limit:
            # Try another requested book that may fit within the remaining time.
            fitting = [item for item in candidates if total_cost + item[0] <= time_limit]
            if not fitting:
                skipped.extend(remaining)
                break
            cost, _, book, path = fitting[0]

        route.extend(path[1:])
        total_cost += cost
        collected.append(book)
        details.append({
            "book": book["title"],
            "shelf": book["shelf"],
            "segment_cost": cost,
            "route_segment": " → ".join(path),
            "priority": book.get("priority", 1),
        })
        current = book["shelf"]
        remaining.remove(book)

    return {
        "route": route,
        "collected": collected,
        "skipped": skipped,
        "total_cost": total_cost,
        "details": details,
    }
