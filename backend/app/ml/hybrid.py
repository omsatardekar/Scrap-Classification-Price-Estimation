from app.core.config import LOCAL_CONF_THRESHOLD


def hybrid_predict(local, nyckel):
    """
    Hybrid inference strategy:
    - Trust local model if confidence is high
    - Otherwise fall back to assisted inference
    """

    local_label, local_conf = local
    ny_label, ny_conf = nyckel

    if local_conf >= LOCAL_CONF_THRESHOLD:
        return local_label, local_conf, " "

    return ny_label, ny_conf, " "
