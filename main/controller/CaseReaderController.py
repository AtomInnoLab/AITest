import pandas

from main.configs.ModelConfig import CASE_FILE_PATH, SHEET_NAME

# 读取测试用例方法
def read_test_cases(CASE_FILE_PATH, SHEET_NAME):
    # 读取Excel表格中指定的sheet
    readFile = pandas.read_excel(CASE_FILE_PATH, sheet_name=SHEET_NAME)
    # 提取文件中列名为“测试用例标题”和“预期结果”两列内容，将其转化为列表
    test_case_titles = readFile["测试用例标题"].tolist()
    expected_results = readFile["预期结果"].tolist()
    # 将两个列表合并为一个字典Map
    test_case_map = dict(zip(test_case_titles, expected_results))
    # 返回字典
    return test_case_map
