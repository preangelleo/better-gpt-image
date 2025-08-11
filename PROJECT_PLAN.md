# Better GPT Image - 项目计划

## 项目概述
创建一个增强版的 OpenAI GPT 图像生成工具，通过智能 Prompt 优化提供更好的图像生成效果。

### 核心价值
1. **智能 Prompt 优化** - 自动优化用户输入的 prompt，提高生成质量
2. **完整功能支持** - 支持 OpenAI 最新的所有图像生成功能
3. **用户友好** - 统一的 Replicate 界面，简化使用流程
4. **成本控制** - 用户使用自己的 API key，控制成本

## 技术架构

### 核心功能模块

#### 1. Prompt 优化器 (prompt_optimizer.py)
- **enhance_prompt()** - 主函数，优化用户输入的 prompt
- **analyze_intent()** - 分析用户意图
- **apply_style_presets()** - 应用风格预设
- **add_quality_modifiers()** - 添加质量修饰词
- **translate_and_enhance()** - 翻译和增强非英文 prompt

#### 2. 图像生成器 (image_generator.py)
- **generate_image()** - 基础图像生成
- **edit_image()** - 图像编辑（使用参考图）
- **edit_with_mask()** - 使用 mask 编辑图像
- **stream_generation()** - 流式生成支持
- **multi_turn_generation()** - 多轮对话生成

#### 3. 图像处理器 (image_processor.py)
- **prepare_input_image()** - 预处理输入图像
- **create_mask()** - 创建和处理 mask
- **handle_transparency()** - 处理透明背景
- **optimize_size()** - 优化图像尺寸

#### 4. 会话管理器 (session_manager.py)
- **manage_conversation()** - 管理多轮对话
- **track_history()** - 跟踪生成历史
- **handle_references()** - 处理图像引用

## API 功能支持

### 支持的 OpenAI 功能
- ✅ GPT-5 文本生成（用于 prompt 优化）
- ✅ GPT-Image-1 图像生成
- ✅ 多图参考生成
- ✅ Mask 编辑（inpainting）
- ✅ 高保真输入（input_fidelity）
- ✅ 透明背景
- ✅ 流式生成
- ✅ 多轮对话编辑
- ✅ 自定义尺寸和质量

### 参数配置
```python
{
    "api_key": str,           # OpenAI API key (必需)
    "prompt": str,            # 原始 prompt
    "model": str,             # "gpt-image-1" (默认)
    "optimize_prompt": bool,  # 是否优化 prompt
    "style_preset": str,      # 风格预设
    "reference_images": list, # 参考图像列表
    "mask": str,             # 编辑 mask
    "size": str,             # 图像尺寸
    "quality": str,          # 质量设置
    "background": str,       # 背景设置
    "input_fidelity": str,   # 输入保真度
    "stream": bool,          # 流式输出
    "partial_images": int    # 部分图像数量
}
```

## 开发计划

### 第一阶段：核心功能（今天）
1. ✅ 项目结构搭建
2. 🔄 Prompt 优化器实现
3. 🔄 基础图像生成
4. 🔄 本地测试

### 第二阶段：高级功能
5. 图像编辑功能
6. 多轮对话支持
7. 流式生成
8. 完整测试套件

### 第三阶段：部署
9. Cog 配置
10. Replicate 部署
11. 文档完善
12. 开源发布

## 目录结构
```
better-gpt-image/
├── src/
│   ├── __init__.py
│   ├── prompt_optimizer.py    # Prompt 优化核心
│   ├── image_generator.py     # 图像生成核心
│   ├── image_processor.py     # 图像处理工具
│   ├── session_manager.py     # 会话管理
│   └── utils.py               # 工具函数
├── tests/
│   ├── test_prompt.py
│   ├── test_generator.py
│   └── test_integration.py
├── examples/
│   ├── basic_generation.py
│   ├── image_editing.py
│   └── multi_turn.py
├── cog.yaml                   # Cog 配置
├── predict.py                 # Replicate 接口
├── requirements.txt
├── README.md
└── PROJECT_PLAN.md
```

## 差异化特点

1. **智能 Prompt 工程**
   - 自动分析和增强用户输入
   - 内置专业提示词库
   - 多语言支持

2. **预设模板**
   - 电影风格
   - 动漫风格
   - 写实摄影
   - 艺术绘画
   - 3D 渲染

3. **批量处理**
   - 支持批量生成
   - 变体生成
   - 风格迁移

4. **用户体验**
   - 清晰的错误提示
   - 进度反馈
   - 成本预估

## 成功指标
- 生成质量提升 30%+
- 用户满意度 90%+
- 开源社区活跃度
- Replicate 平台使用量