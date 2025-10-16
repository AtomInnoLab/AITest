import sys
import logging

# 定义日志配置方法
def setup_logger(name="app"):
    # 创建一个全局唯一的logger实例
    logger = logging.getLogger(name)
    # 避免重复添加处理器
    if not logger.handlers:
        # 设置日志级别
        logger.setLevel(logging.DEBUG)
        # 创建控制台处理器：强制无缓冲
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        # 将处理器添加到logger
        logger.addHandler(console_handler)
    # 返回logger
    return logger
# 创建并导出默认logger
logger = setup_logger()