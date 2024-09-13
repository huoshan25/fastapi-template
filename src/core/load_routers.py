import importlib
import os
import sys
import traceback

from fastapi import FastAPI

MODULES_DIR = "src.modules"


def register_routes(app: FastAPI):
    modules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modules")
    print('♻️ 开始扫描路由')

    if not os.path.exists(modules_path):
        raise FileNotFoundError(f"❌ 未找到路径: {modules_path}")

    for module_name in os.listdir(modules_path):
        module_path = os.path.join(modules_path, module_name)

        if os.path.isdir(module_path) and not module_name.startswith("__"):
            for file_name in os.listdir(module_path):
                if file_name.endswith("_controller.py"):
                    module_file = file_name[:-3]  # 去掉 ".py" 后缀
                    full_module_name = f"{MODULES_DIR}.{module_name}.{module_file}"
                    try:
                        controller_module = importlib.import_module(full_module_name)
                        # 检查控制器类是否有 router 属性
                        for attr_name in dir(controller_module):
                            attr_value = getattr(controller_module, attr_name)
                            if isinstance(attr_value, type):  # 检查是否为类
                                instance = attr_value()
                                if hasattr(instance, "router"):
                                    app.include_router(instance.router)
                                    print(f"{module_name}.{module_file} ✅.")
                                    break  # 找到一个 router 就退出循环
                    except Exception as e:
                        error_info = get_error_info(sys.exc_info()[2], full_module_name)
                        print(f"注册模块 '{module_name}.{module_file}' 时发生错误 ❌ {type(e).__name__}:")
                        if error_info:
                            print(f"  文件: {error_info['filename']}")
                            print(f"  行号: {error_info['lineno']}")
                        else:
                            print(f"  模块: {full_module_name}")
                        print(f"  错误信息: {str(e)}")
                        print(f"  堆栈跟踪:\n{traceback.format_exc()}")


def get_error_info(tb, full_module_name):
    while tb:
        frame = tb.tb_frame
        if frame.f_globals.get('__name__') == full_module_name:
            return {
                'filename': frame.f_code.co_filename,
                'lineno': tb.tb_lineno
            }
        tb = tb.tb_next
    return None