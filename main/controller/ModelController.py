import os
import time
import logging
import base64
import pyautogui
import requests
import importlib

from dashscope import Application
from main.controller.CaseReaderController import read_test_cases
from openai import OpenAI
from http import HTTPStatus

from main.files.code import ai_test_code
from main.files.criteria import AssertResult
from main.configs.LoggingConfig import logger
from main.configs.ModelConfig import LAGUAGE_API_KEY, LAGUAGE_MODEL_ID, VIEW_MODEL, VIEW_MODEL_API_KEY, VIEW_MODEL_API_KEY_ADDRESS, INIT_PAGE_IMAGE_PATH, AI_TEST_CODE_FILE_PATH, ASSERT_IMAGE, START_NUMBER

# AI测试执行器类
class AITestExecutor():

    # 执行大语言模型的第一次追问逻辑，将测试用例传给大语言模型
    def output_code_by_model_step1(input_cases):
        # 输出日志
        logger.info("开始根据测试用例文件生成相应的UI自动化代码")
        # 以下是Prompt，用的是通义千问-turbo模型
        """
        # 角色
        你是一名专业的测试工程师，擅长将用户提供的测试用例数据转化为UI自动化代码。在两轮对话中，你需要首先理解用户编写的测试用例，并生成相应的UI自动化代码（使用pyautogui库）。在第二轮对话中，根据用户返回的坐标信息，完善之前生成的代码。
        
        ## 技能
        ### 技能 1: 理解测试用例
        - 接收并理解用户提供的测试用例数据，格式为 `{'测试用例标题': '期待结果'}`，多个测试用例间以逗号分隔。
        
        ### 技能 2: 生成UI自动化代码
        - 根据理解的测试用例，编写相应的UI自动化代码。
        - 生成UI自动化代码的执行顺序按返回给你的字典的下标顺序相反。
        - 使用位置定位方式，预留出需要填写的位置变量名称（例如：`{element_position}`）。
        - 生成的代码应结构清晰、易于维护，包含必要的注释。
        - 第二轮对话中一定要去理解我传给你的坐标字典，去理解拿到相应坐标，最好别出现没拿到坐标的情况。
        - 帮我生成的最终UI自动化代码外层加一个def AITestCode():包裹起来，同时一定要导入生成代码需要的包。
        
        ### 技能 3: 代码优化与调试
        - 确保生成的代码能够正确运行，并达到预期的测试效果。
        - 提供代码的详细注释，解释关键逻辑部分，以便用户理解和修改。
        - 生成的最终代码每一步都设置等待时间为2秒，即`time.sleep(2)`。
        - 在使用每一个`pyautogui.write()`方法时，添加`interval=0.1`参数，以保证输入内容不会过快导致丢失。
        
        ## 限制
        - 只针对UI自动化代码的生成进行工作，不涉及其他类型的测试或开发任务。
        - 定位方式必须使用位置定位，并预留出需要填写的位置变量名称。
        - 生成的代码应结构清晰、易于维护，并包含必要的注释。
        - 保持代码的可读性和可维护性，避免过度复杂化。
        - 不引入个人观点或偏见，确保代码客观准确。
        - 严格按照测试用例标题的说法进行生成代码，不要根据上下文去联系，去篡改内容，例如在测试用例标题中指令让你做什么就生成什么样的命令。让你回车你就别自主判断去做点击。
        - 生成的代码开头不需要```python，结尾不需要```，以免影响代码的运行。
        """
        # 第一次调用大语言模型生成没有元素坐标的UI自动化代码
        response = Application.call(
            api_key = LAGUAGE_API_KEY,
            app_id = LAGUAGE_MODEL_ID,
            prompt = input_cases
        )
        
        # 当调用模型返回的响应状态码不为200时，则输出相应响应内容
        if response.status_code != HTTPStatus.OK:
            # 输出日志
            logger.error(f"调用大语言模型失败，request_id={response.request_id}，status_code={response.status_code}，message={response.message}")
            # 输出日志
            logger.error(f"请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        else:
            # 输出日志
            logger.info("根据用例生成未带元素坐标的初始UI自动化代码成功...")
            # 输出日志
            logger.info("准备全屏截图，请在8s内打开需要开始测试的相应界面")
            # 休眠8秒
            time.sleep(8)
            # 输出日志
            logger.info("正在接入视觉模型解析元素位置坐标...")
            # 返回响应
            return response

    # 执行大语言模型的第二次追问逻辑，将视觉模型生成的元素坐标传给大语言模型
    def output_code_by_model_step2(response, element_position):
        # 第二次调用大语言模型生成带元素坐标的UI自动化代码
        responseNext = Application.call(
            api_key = LAGUAGE_API_KEY,
            app_id = LAGUAGE_MODEL_ID,
            prompt = element_position,
            session_id = response.output.session_id
        )
        # 当调用模型返回的响应状态码不为200时，则输出相应响应内容
        if response.status_code != HTTPStatus.OK:
            # 输出日志
            logger.error(f"调用大语言模型失败，request_id={response.request_id}，status_code={response.status_code}，message={response.message}")
            # 输出日志
            logger.error(f"请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        else:
            # 输出日志
            logger.info("UI自动化代码生成完毕！")
            # 返回响应
            return responseNext.output.text

    # 调用视觉模型对截图进行元素的定位分析
    def output_element_position_by_image(image_path):
        # 编码图片
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        # 调用通义千问2.5-VL-32B-Instruct视觉模型
        message = [
            {"role": "system", "content": "你是一个专业的视觉助手。"},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    {"type": "text",
                     "text": "请解析图片中的各个元素给我，我需要抽取文字和输入框等元素位置，最好是获取到该元素的中心点位置，比如是按钮的话获取到按钮的中心位置，并把他们的元素定位以Python语法的集合给我。你要尽可能的获取到所有元素的集合，例如输入框等非文字元素的定位，最好把坐标以如下格式传回来。例如：'百度一下' : '元素位置坐标：(x, y)'，我的屏幕分辨率是2880*1920。"},
                ]
            }
        ]
        # 创建请求体
        payload = {
            "model": VIEW_MODEL,
            "message": message,
            "max_tokne": 8192,
        }
        # 创建请求头
        headers = {
            "Authorization": "Bearer " + VIEW_MODEL_API_KEY,
            "Content-Type": "application/json",
        }
        # 发送POST请求
        response = requests.post(VIEW_MODEL_API_KEY_ADDRESS, json=payload, headers=headers)
        # 返回结果
        return response.json()["choices"][0]["message"]["content"]
    
    # 将最终生成的UI自动化代码写入文件
    def output_code_as_file(response):
        # 打印日志
        logger.info("正在将UI自动化代码写入文件...")
        # 写入文件
        with open(AI_TEST_CODE_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(final_response)
        # 打印日志
        logger.info("文件写入完毕！")

    def start():
        # 指定用例从第几条开始，默认为1
        start_number = START_NUMBER
        # 索引下标
        start_index = start_number - 1
        # 接收所有测试用例
        test_cases = read_test_cases(CASE_FILE_PATH)
        # 创建一个名称为expected_result的列表
        expected_result = []
        # 循环遍历测试用例
        for index, (title, expected) in list(enumerate(test_cases.items()))[start_index:]:
            # 打印日志
            logger.info(f"开始执行第{index + 1}条用例：{title}")
            # 创建当前测试用例的字典，使分开来的title和expected合并为title：expected的字典
            current_case = {title: expected}
            # 调用大语言模型第一步
            response = AITestExecutor.output_code_by_model_step1(current_case)
            # 执行全屏截图
            initial_screenshot = pyautogui.screenshot()
            # 保存全屏截图到指定路径
            initial_screenshot.save(INIT_PAGE_IMAGE_PATH)
            # 调用视觉模型第二步
            element_position = AITestExecutor.output_element_position_by_image()
            # 调用大语言模型的第二步
            final_response = AITestExecutor.output_code_by_model_step2(response, element_position)
            # 将最终生成的UI自动化代码写入到文件中
            AITestExecutor.output_code_as_file(final_response)
            try:
                # 先重新加载模块，重新导入ai_test_code文件，使其重新加载到内存中
                importlib.reload(ai_test_code)
                # 导入ai_test_code文件
                from ai_test.files.ai_test_code import AITestCode
                # 调用ai_test_code文件中的AITestCode方法，跳过第一次没有AITestCode
                if hasattr(ai_test_code, "AITestCode") and (ai_test_code.AITestCode):
                    ai_test_code.AITestCode()
                else:
                    raise AttributeError("AITestCode 未定义")
            except ImportError:
                # 打印日志
                logger.error("ai_test_code 模块导入失败，使用默认实现")
            # 打印日志
            logger.info(f"第{index + 1}条测试用例执行完毕！")
            # 生成截图的完整路径
            full_path = os.path.join(ASSERT_IMAGE, f"test_case_{index + 1}.png")
            # 等待3s，确保资源加载完成，防止过快
            time.sleep(3)
            # 创建截图对象
            result_screenshot = pyautogui.screenshot()
            # 保存截图
            result_screenshot.save(full_path)
            # 将期待结果传给expected_result字典
            expected_result[index] = expected
        # 打印日志
        logger.info("所有测试用例执行完毕！")
        # 进行结果断言
        AssertResult.criteria_result(expected_result)

# 入口
if __name__ == '__main__':
    # 获取开始时间的时间戳
    start_time = time.time()
    # 启动测试
    AITestExecutor.start()
    # 获取结束时间的时间戳
    end_time = time.time()
    # 打印日志
    logger.info(f"AITest执行完毕，耗时：{end_time - start_time}秒")
