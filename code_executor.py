import io
import sys
import traceback
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CodeExecutor:
    def __init__(self, initial_df):
        self.globals = {
            "pd": pd,
            "plt": plt,
            "sns": sns,
            "df": initial_df
        }
    
    def execute(self, code):
        """
        执行代码并捕获输出
        返回: (success: bool, output: str)
        """
        # 捕获标准输出
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        success = True
        result = ""
        
        try:
            exec(code, self.globals)
            
            # 获取 print 的内容
            result = redirected_output.getvalue()
            if not result.strip():
                result = "[代码执行成功，但没有 print 输出结果]"
                
        except Exception:
            success = False
            # 获取详细的报错堆栈
            result = traceback.format_exc()
            
        finally:
            # 恢复标准输出
            sys.stdout = old_stdout
            
        return success, result