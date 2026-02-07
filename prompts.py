def get_initial_prompt(df_head, df_info):
    """
    初始化提示词：引导模型进行“观察-清洗-验证”的思维链 (CoT)
    """
    return f"""
# 角色定义
你是一位资深 Python 数据分析师。你的任务是编写代码分析内存中的 DataFrame (`df`)。

# 数据全景 (Data Context)
- 列类型概览:
{df_info}

- 样本数据预览:
{df_head}

# 数据清洗思维指南 (Thinking Process)
观察发现 'Sales' 和 'Rating' 列虽然是数值含义，但当前被识别为 Object/String 类型（可能包含 '$', '%', ',' 等符号）。
**请不要直接开始计算，而是遵循以下“防御性编程”流程：**

1. **观察 (Observe)**：
   - 检查目标列是否为 Object 类型。如果是数字类型则直接跳过。

2. **清洗 (Clean Strategy)**：
   - 针对货币列 ('Sales')：编写逻辑去除 '$' 和 ','，保留数字和小数点。
   - 针对百分比列 ('Rating')：编写逻辑去除 '%'，转为浮点数后除以 100。
   - **关键技巧**：推荐使用 `pd.to_numeric(..., errors='coerce')` 进行最终转换，以处理潜在的脏数据（如空字符串）。

3. **验证 (Verify)**：
   - 转换后，建议打印 `df['Sales'].head()` 确认清洗成功，避免全变成了 NaN 或 0。

# 代码编写约束
1. **环境**：直接使用 `df`，**严禁**使用 `read_csv` 重新读取文件（这会丢失之前的处理）。
2. **输出**：仅输出 Python 代码块。
3. **交互**：所有分析结果必须用 `print()` 展示。
"""

def get_error_correction_prompt(error_msg):
    """
    纠错提示词：引导模型分析 Traceback
    """
    return f"""
# 运行时异常分析
代码执行遇到了问题，错误信息如下：

{error_msg}

# 修正指南
请按照以下步骤排查：
1. **类型错误？** 是否对 String 类型的列进行了 Sum/Mean 计算？如果是，请加入数据清洗代码。
2. **清洗失败？** 是否使用了错误的正则导致数据变成了 NaN（例如全为 0）？如果是，请尝试更稳健的清洗逻辑（如先打印看看数据长什么样）。

请输出修正后的完整 Python 代码。
"""

def get_explanation_prompt(user_query, execution_output):
    """
    解释提示词：强调业务结论
    """
    return f"""
# 用户需求
"{user_query}"

# 分析结果
{execution_output}

# 回答策略
请作为业务专家，用简洁的中文解读上述数据。
- 重点关注趋势、异常值或对比结果。
- 如果结果数据异常（如全为 0），请诚实地提示用户可能存在数据质量问题。
- 即使结果集为空（Empty DataFrame），也要打印出原始的聚合数据，以便用户核实。
"""