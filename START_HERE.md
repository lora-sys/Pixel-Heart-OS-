# 🚀 START HERE - Docker 一键启动

## 最快路径 ( Mock 模式，无需 API Key)

```bash
# 1. 确保在项目根目录
cd /home/lora/repos/Pixel-Heart-OS-

# 2. 创建环境配置（Mock 模式，无 API key）
cp .env.example .env
# 编辑 .env，确保有：LLM_PROVIDER=mock 和 USE_MOCK_LLM=True

# 3. Docker 一键启动
docker-compose up -d

# 4. 访问
# 前端：http://localhost
# 后端 API 文档：http://localhost:8000/docs
```

**Mock 模式说明**：
- ✅ 无需 API key
- ✅ 能看到完整 UI 和所有页面
- ✅ Beads 时间线、分支功能都可用
- ❌ NPC 对话是预设的简单回复（不是真实 AI）
- ✅ 适合测试 UI、数据流、Beads 系统

---

## 🎯 使用 StepFun API (真实 LLM)

当你准备好 StepFun API key 后：

```bash
# 1. 修改 .env
LLM_PROVIDER=stepfun
USE_MOCK_LLM=False
STEPFUN_API_KEY=sk-你的密钥

# 2. 重启 Docker
docker-compose restart
```

即可享受真实 AI 驱动的 NPC 对话和生成！

---

## 📦 项目结构 (已创建)

```
Pixel-Heart-OS/
├── backend/              # FastAPI (Python)
│   ├── api/v1/          # REST API 端点
│   ├── beads/engine.py  # ✨ Beads DAG 引擎
│   ├── llm/service.py   # ✨ LLM 服务（支持 Anthropic/StepFun/Mock）
│   ├── config.py        # 配置管理
│   └── main.py          # FastAPI 入口
├── frontend/             # Svelte 5 + Phaser 3
│   ├── src/lib/         # 全局状态、API 客户端、EventBus
│   ├── src/routes/      # 4 个页面（create, universe, simulate, timeline）
│   └── package.json     # Bun 依赖
├── data/                 # 数据存储（容器内持久化）
├── docker-compose.yml   # 容器编排
└── .env                  # 你的环境配置（需创建）
```

---

## ✅ 已完成的修复 (Code Review 后)

1. ✅ **Beads DAG 引擎** - 完整实现（SHA-1、分支、合并、diff）
2. ✅ **LLM 多提供商** - Anthropic + StepFun + Mock 模式
3. ✅ **路径配置** - data_dir 绝对路径修复
4. ✅ **API 路由** - main.py 包含 v1_router
5. ✅ **导入路径** - simulation.py 正确导入 schemas
6. ✅ **bead_engine 初始化** - startup event 中初始化
7. ✅ **Simulation 状态** - build_simulation_state 函数完整
8. ✅ **Docker 环境变量** - 支持所有 LLM 配置
9. ✅ **像素风格** - 100% 还原 index.html 设计
10. ✅ **Mock 模式** - 无 API key 也能体验完整流程

---

## 🎮 体验流程

1. **Create** (`/create`) - 输入 heroine 描述 → 解析 soul 结构
2. **Universe** (`/universe`) - 自动生成 3 个 NPC + 场景
3. **Simulate** (`/simulate`) - 与 NPC 对话（Mock 模式返回预设）
4. **Timeline** (`/timeline`) - 查看 Beads DAG，创建分支

---

## 🐛 问题排查

```bash
# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 检查容器状态
docker-compose ps

# 重启
docker-compose restart

# 完全重建
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

详细问题排查见 `TROUBLESHOOTING.md`

---

## 🎨 像素风格验证

- ✅ 扫描线效果 (scanlines)
- ✅ 霓虹配色 (accent-1~5)
- ✅ 4px 块状边框 (blocky borders)
- ✅ 复古字体 (Press Start 2P, Share Tech Mono)
- ✅ 倒角阴影 (4px 4px 0 #000)

视觉设计 100% 贴合 `index.html` 原型！

---

## 📚 相关文档

- `README.md` - 项目介绍
- `QUICKSTART.md` - 开发模式快速启动（非 Docker）
- `DOCKER_DEPLOY.md` - 详细 Docker 部署指南
- `CLAUDE.md` - 代码库指南
- `PROJECT_SUMMARY.md` - 完整实现总结
- `Pixel Heart OS_ AI-Readable Requirements Document v2.0.md` - 原始需求

---

**Ready?** `docker-compose up -d` and enjoy! 🚀
