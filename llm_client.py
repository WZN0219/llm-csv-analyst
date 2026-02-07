import os
import dashscope
from dashscope import Generation
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        # 设置 API Key
        dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
        
        # 获取模型名称
        self.model = os.getenv("LLM_MODEL", "qwen-plus")
        
        # 对话历史记忆
        self.messages = [] 

    def initialize_system(self, system_prompt):
        """设置系统人设"""
        self.messages = [{"role": "system", "content": system_prompt}]

    def get_response(self, user_input, is_error_feedback=False):
        # 1. 维护对话历史
        if not is_error_feedback:
            self.messages.append({"role": "user", "content": user_input})
        else:
            # 纠错模式下，也作为新的一轮输入
            self.messages.append({"role": "user", "content": user_input})

        try:
            response = Generation.call(
                model=self.model,
                messages=self.messages,
                result_format='message',  # 返回格式为消息格式
                temperature=0.1,          # 低温
                top_p=0.7
            )

            # 3. 解析返回结果
            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0].message.content
                
                # 记录 AI 的回答到历史中
                self.messages.append({"role": "assistant", "content": content})
                return content
            else:
                # 处理 API 报错
                error_msg = f"API Error: {response.code} - {response.message}"
                print(error_msg)
                return f"# {error_msg}"

        except Exception as e:
            print(f"SDK 调用失败: {e}")
            return "# Error calling DashScope SDK"