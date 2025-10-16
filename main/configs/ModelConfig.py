# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# 测试用例文件路径
CASE_FILE_PATH = os.path.join(PROJECT_ROOT, "main", "files", "case", "test_cases.xlsx")
# 测试用例文件Sheet（默认为Sheet1）
SHEET_NAME = "Sheet1"
# 大语言模型的API_key
LAGUAGE_API_KEY = ''
# 大语言模型ID
LAGUAGE_MODEL_ID = ''
# 视觉模型地址
VIEW_MODEL_API_KEY_ADDRESS = ''
# 视觉模型
VIEW_MODEL = ''
# 视觉模型API_key
VIEW_MODEL_API_KEY = ''
# 初始页面图片保存路径
INIT_PAGE_IMAGE_PATH = os.path.join(PROJECT_ROOT, "main", "files", "image", "init_page.png")
# 最终UI自动化代码保存路径
AI_TEST_CODE_FILE_PATH = os.path.join(PROJECT_ROOT, "main", "files", "code", "ai_test_code.py")
# 测试用例结束生成的截图保存路径
ASSERT_IMAGE = os.path.join(PROJECT_ROOT, "main", "files", "images")
# 测试用例执行的开始条数
START_NUMBER = 1