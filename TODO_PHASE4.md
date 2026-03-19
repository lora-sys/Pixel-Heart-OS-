# Phase 4 开发待办事项

## 当前状态: 进行中 (10%)

## 立即需要修复的问题

### 1. 安装缺失依赖 (优先级: 最高)

**问题**: LangGraph 和 ChromaDB 依赖未安装

**解决方案**:
```bash
cd backend
source .venv/bin/activate
pip install langgraph chromadb
```

**验证**:
```bash
pip list | grep -E "langgraph|chromadb"
```

---

### 2. 修复 LangGraph 类型错误 (优先级: 高)

**文件**: `backend/graphs/simulation_graph.py`

**问题**:
1. 节点函数返回类型不匹配 (需要完整 SimulationState)
2. TypedDict 字段未正确设置为 Optional

**解决方案**:
- 使用 `NotRequired` 或 `total=False` for partial updates
- 或者修改节点函数返回完整的 state

**示例修复**:
```python
class SimulationState(TypedDict, total=False):
    """State for the simulation workflow."""
    heroine_soul: Dict[str, Any]
    current_scene: Optional[Dict[str, Any]]
    active_npcs: List[Dict[str, Any]]
    # ... 其他字段
```

或者节点函数返回完整 state:
```python
async def retrieve_context(state: SimulationState) -> SimulationState:
    return {
        "heroine_soul": state.get("heroine_soul", {}),
        "current_scene": state.get("current_scene"),
        "active_npcs": state.get("active_npcs", []),
        "player_action": state.get("player_action", ""),
        "conversation_history": state.get("conversation_history", []),
        "retrieved_memories": [],  # 更新这个
        "npc_responses": state.get("npc_responses", []),
        "updated_relationships": state.get("updated_relationships", {}),
        "bead_data": state.get("bead_data", {}),
        "new_bead_id": state.get("new_bead_id"),
    }
```

---

### 3. 集成 ChromaDB 到 DI 容器 (优先级: 高)

**文件**: `backend/core/container.py`

**修改内容**:
```python
def get_vector_store(self) -> VectorStoreService:
    """Get VectorStoreService singleton."""
    if "vector_store" not in self._singletons:
        from vector_store.chroma_client import VectorStoreService
        self._singletons["vector_store"] = VectorStoreService()
    return self._singletons["vector_store"]
```

---

## Phase 4 详细待办事项

### Wave 1: ChromaDB 集成 (预计 2 小时)

- [ ] 安装 langgraph 和 chromadb 依赖
- [ ] 修复 chroma_client.py 导入错误
- [ ] 集成到 DI 容器 (get_vector_store)
- [ ] 编写端到端测试
- [ ] 测试语义搜索功能

**成功标准**:
- ChromaClient 可以连接到 ChromaDB
- 可以创建和查询集合
- 语义搜索返回正确结果

---

### Wave 2: LangGraph 工作流 (预计 3 小时)

- [ ] 安装 langgraph 依赖
- [ ] 修复 simulation_graph.py 类型错误
- [ ] 完善节点函数实现
- [ ] 集成到 SimulationService
- [ ] 编写端到端测试
- [ ] 测试工作流执行

**成功标准**:
- 工作流可以正常编译
- 节点函数按顺序执行
- 检查点功能正常工作
- SimulationService 可以调用工作流

---

### Wave 3: LLM 提示模板 (预计 1 小时)

- [ ] 创建 `heroine_parsing.txt` 提示模板
- [ ] 创建 `npc_generation.txt` 提示模板
- [ ] 创建 `dialogue_generation.txt` 提示模板
- [ ] 创建 `scene_generation.txt` 提示模板
- [ ] 在 LLMService 中使用提示模板

**成功标准**:
- 提示模板文件存在
- LLMService 可以加载和使用模板
- Mock 模式返回合理结果

---

### Wave 4: 前端组件 (预计 3 小时)

- [ ] 创建 `NPCCard.svelte` 组件
- [ ] 创建 `SceneCard.svelte` 组件
- [ ] 创建 `DiffViewer.svelte` 组件
- [ ] 创建 `Navigation.svelte` 组件
- [ ] 创建 `TerminalInput.svelte` 组件
- [ ] 更新现有页面使用新组件

**成功标准**:
- 组件可以独立渲染
- 组件可以接收 props
- 组件样式符合像素艺术风格

---

### Wave 5: Phaser 可视化 (预计 2 小时)

- [ ] 更新 `PhaserGame.svelte`
- [ ] 实现关系星云可视化
- [ ] 实现时间线条
- [ ] 添加交互功能 (点击选择 bead)

**成功标准**:
- Phaser 游戏可以正常加载
- 关系星云显示 NPC 节点和关系边
- 时间线条显示 bead 历史
- 点击交互正常工作

---

### Wave 6: 端到端测试和集成 (预计 2 小时)

- [ ] 测试女主角创建流程
- [ ] 测试宇宙生成
- [ ] 测试模拟交互
- [ ] 测试时间线可视化
- [ ] 修复发现的 bug

**成功标准**:
- 所有端点返回正确结果
- 前端可以正常调用 API
- 数据流完整无误

---

### Wave 7: Git 提交和文档 (预计 1 小时)

- [ ] 运行代码格式化和 linting
- [ ] 运行所有测试
- [ ] 提交代码
- [ ] 推送到远程仓库
- [ ] 更新项目文档

**成功标准**:
- 所有测试通过
- 代码符合项目规范
- 文档是最新的

---

## 时间估计

| 波次 | 任务 | 时间估计 |
|------|------|----------|
| 1 | ChromaDB 集成 | 2 小时 |
| 2 | LangGraph 工作流 | 3 小时 |
| 3 | LLM 提示模板 | 1 小时 |
| 4 | 前端组件 | 3 小时 |
| 5 | Phaser 可视化 | 2 小时 |
| 6 | 端到端测试 | 2 小时 |
| 7 | Git 提交 | 1 小时 |
| **总计** | | **14 小时** |

---

## 验证清单

### 功能验证

- [ ] ChromaDB 连接正常
- [ ] 语义搜索返回合理结果
- [ ] LangGraph 工作流执行成功
- [ ] SimulationService 集成正常
- [ ] 前端组件渲染正常
- [ ] Phaser 可视化显示正确
- [ ] 端到端数据流完整

### 代码质量

- [ ] 所有导入正常工作
- [ ] 类型检查通过
- [ ] 代码格式化符合规范
- [ ] 没有未使用的变量
- [ ] 错误处理完善

### 测试覆盖

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试通过
- [ ] 回归测试通过

---

## 下一步行动

立即执行:
1. 安装依赖: `pip install langgraph chromadb`
2. 修复类型错误
3. 测试 ChromaDB 集成

然后按波次顺序执行其他任务。
