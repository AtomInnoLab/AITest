from main.files import images

def criteria_result(expected_result):
    # 记录成功的用例数
    success = 0
    # 记录失败的用例数
    failure = 0
    # 遍历expected_result列表
    for i in range(len(expected_result)):
        # 调用视觉大模型API判断是否与期待结果一致
        """
        # TODO：加上调用的大模型去断言测试用例执行完毕相对应的截图
        """
        
    return success, failure
