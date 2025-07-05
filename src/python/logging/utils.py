from logging import getLogger, basicConfig, INFO


logger = getLogger(__name__)

basicConfig(
    filename='log.log',
    filemode='w',
    level=INFO,
    format='{asctime} {name}:{lineno} [{levelname}]: {message}',
    style='{'
)
