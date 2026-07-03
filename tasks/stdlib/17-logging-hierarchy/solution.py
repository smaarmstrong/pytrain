import logging


def audit(user, action):
    logging.getLogger("app.audit").info("%s did %s", user, action)


def warn_quota(user, pct):
    logger = logging.getLogger("app.quota")
    if pct >= 90:
        logger.warning("%s at %s%%", user, pct)
    else:
        logger.debug("%s at %s%%", user, pct)


def setup(stream):
    logger = logging.getLogger("app")
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
