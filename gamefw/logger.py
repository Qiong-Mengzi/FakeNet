import logging

ROOT_LOGGER = logging.getLogger("gamefw")
ROOT_LOGGER.setLevel(logging.DEBUG)

fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(message)s]", "%H:%M:%S")
fh = logging.FileHandler("./latest.log", "w", encoding="utf-8")

fh.setFormatter(fmt)
fh.setLevel(logging.INFO)
ROOT_LOGGER.addHandler(fh)

logging.info("[======== FakeNet GameFW Logging Start ========]")
