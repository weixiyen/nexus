import logging

_logger = logging.getLogger('venom')
#_logger.setLevel(logging.DEBUG)

warn = _logger.warning
info = _logger.info
error = _logger.error
critical = _logger.critical
debug = _logger.debug