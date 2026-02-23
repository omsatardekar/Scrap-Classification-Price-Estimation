from app.utils.distance import calculate_distance


def assign_nearest(order, delivery_agents):
    """
    Assign the nearest available delivery agent
    based on geographic distance.
    """

    order_lat = order["location"]["latitude"]
    order_lng = order["location"]["longitude"]

    nearest_agent = None
    min_distance = float("inf")

    for agent in delivery_agents:
        location = agent.get("location")

        if not location:
            continue

        agent_lat = location.get("latitude")
        agent_lng = location.get("longitude")

        if agent_lat is None or agent_lng is None:
            continue

        distance = calculate_distance(
            order_lat,
            order_lng,
            agent_lat,
            agent_lng,
        )

        if distance < min_distance:
            min_distance = distance
            nearest_agent = agent

    if not nearest_agent:
        raise Exception("No valid delivery agent with location found")

    return nearest_agent
