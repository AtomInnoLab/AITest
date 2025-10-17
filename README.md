# 📁 项目结构
├── main/                # 应用目录<br/>
│   ├──configs/          # 变量配置与工具配置<br/>
│   ├──controller/       # 方法控制类<br/>
│   ├──files/            # 物料资源<br/>
│   │   ├──case/         # 测试用例<br/>
│   │   ├──code/         # 生成的自动化代码<br/>
│   │   ├──criteria/     # 断言脚本<br/>
│   │──tools/            # 部分辅助工具脚本<br/>

# 🔧 库安装
- pip install loggging requests pandas pyautogui OpenAI

# ⚠ 模型配置
使用不同模型，需要根据对应模型的调用方法进行替换。本项目中可替换模型的方法：<br/>
1、output_code_by_model_step1<br/>
2、output_code_by_model_step2<br/>
3、output_element_position_by_image<br/>
4、criteria_result
