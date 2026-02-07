import re
import pandas as pd
from llm_client import LLMClient
from code_executor import CodeExecutor
from prompts import get_initial_prompt, get_error_correction_prompt, get_explanation_prompt

def extract_code(text):
    """从 Markdown 中提取 Python 代码"""
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def main():
    print("=== 大模型 CSV 数据分析 Agent (Powered by Qwen) ===")
    
    # 1. 读取数据
    csv_path = "data/test.csv"
    try:
        df = pd.read_csv(csv_path)
        print(f"成功加载数据: {csv_path} | 行数: {len(df)}")
    except FileNotFoundError:
        print(f"错误: 找不到文件 {csv_path}，请确保文件在 data 目录下。")
        return

    # 2. 初始化模块
    llm = LLMClient()
    executor = CodeExecutor(df) # 把 df 传给执行器

    # 3. 构建初始 Prompt (包含数据摘要)
    df_head = df.head().to_markdown(index=False)
    df_info = str(df.dtypes)
    system_prompt = get_initial_prompt(df_head, df_info)
    llm.initialize_system(system_prompt)
    
    print("系统就绪。请开始提问 (输入 'exit' 退出)")
    
    # 4. 主循环 (多轮对话)
    while True:
        user_query = input("\n👤 用户: ")
        if user_query.lower() in ['exit', 'quit']:
            break
        
        print("🤖 Agent 思考中...")
        
        # --- 步骤 A: 生成代码 ---
        response = llm.get_response(f"用户需求: {user_query}")
        code = extract_code(response)
        
        print(f"\n--- 生成的代码 ---\n{code}\n------------------")
        
        # --- 步骤 B: 执行与纠错 ---
        max_retries = 3
        execution_success = False
        execution_output = ""
        
        for i in range(max_retries):
            # 执行代码
            success, output = executor.execute(code)
            
            if success:
                execution_success = True
                execution_output = output
                print(f"✅ 执行成功。输出结果:\n{output[:500]}..." if len(output)>500 else f"✅ 执行成功。输出结果:\n{output}")
                break
            else:
                print(f"❌ 执行报错 (尝试 {i+1}/{max_retries}):\n{output.splitlines()[-1]}") # 只打印最后一行报错
                
                # 触发纠错循环
                correction_prompt = get_error_correction_prompt(output)
                print("🔄 正在自我修正代码...")
                response = llm.get_response(correction_prompt, is_error_feedback=True)
                code = extract_code(response)
                print(f"--- 修正后的代码 ---\n{code}\n------------------")
        
        # --- 步骤 C: 解释结果 ---
        if execution_success:
            print("\n📝 正在生成回答...")
            final_prompt = get_explanation_prompt(user_query, execution_output)
            final_answer = llm.get_response(final_prompt)
            print(f"\n🤖 Agent 回答:\n{final_answer}")
        else:
            print("\n💀 任务失败: 代码经过多次修正仍无法运行。")

if __name__ == "__main__":
    main()