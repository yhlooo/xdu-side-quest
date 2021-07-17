import logging

# 设置根日志
root_logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[%(asctime)s %(levelname)-7s][%(name)-13s] %(message)s'))
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)
