# 🤖 LLM Assessment Framework

整合的大型語言模型評測框架，提供全方位的模型評測機制，涵蓋**可解釋性 (Explainability)**、**可靠性 (Reliability)** 和**安全性 (Safety)** 三大面向。

## 📋 概述

本框架旨在建立一套標準化、自動化的 LLM 評測流程，協助評估模型在不同維度上的表現，並生成詳細的評測報告，確保模型符合實際應用的要求。

## 🎯 評測面向

### 🔍 可解釋性 (Explainability)
評估模型是否能清楚呈現推理過程與決策依據：
- **Chain of Thought (CoT)**: 檢查模型的推理邏輯是否合理、一致
- **Citation**: 評估模型提供的引用來源是否真實可靠

### ✅ 可靠性 (Reliability)
評估模型輸出的穩定性與知識準確度：
- **C-Eval**: 中文知識準確度測試 (52個學科領域)
- **Consistency**: 回答一致性檢查 (使用 BERTScore)

### 🛡️ 安全性 (Safety)
評估模型在多個安全維度的表現：
- **BBQ (Bias Benchmark)**: 偏見評測 (9個社會群體維度)
- **BIPIA**: 間接提示注入攻擊測試
- **Toxicity**: 毒性內容評測
- **Information Disclosure**: 資訊洩漏測試
- **Direct Prompt Injection**: 直接提示注入測試
- **Misinformation**: 錯誤訊息處理測試

## 🏗️ 專案結構

```
LLM_Assessment_Fubon/
├── main.py                     # 🚀 主要整合腳本 (入口點)
├── config.json                 # ⚙️  統一配置文件
├── report_generator.py         # 📊 報告生成模組
├── results/                    # 📁 整合評測結果輸出目錄
│
├── explainability/             # 🔍 可解釋性評測模組
│   ├── main.py
│   ├── core/
│   ├── data/
│   └── outputs/
│
├── reliability/                # ✅ 可靠性評測模組
│   ├── ceval/                  # C-Eval 知識準確度測試
│   │   ├── run_ceval.py
│   │   └── results/
│   └── consistency/            # 一致性測試
│       ├── main.py
│       └── outputs/
│
└── safety/                     # 🛡️ 安全性評測模組
    ├── main.py
    ├── config.json
    ├── BBQ/                    # 偏見評測
    ├── BIPIA/                  # 間接提示注入
    ├── Toxicity/               # 毒性評測
    ├── InformationDisclosure/  # 資訊洩漏
    ├── DirectPromptInjection/  # 直接提示注入
    ├── Misinformation/         # 錯誤訊息
    └── results/
```

## 🚀 快速開始

### 1. 配置設定

編輯 `config.json` 文件，設定要評測的模型和各項參數：

```json
{
  "model": {
    "name": "gpt-4o",
    "type": "azure",
    "description": "The model to be evaluated"
  },
  "llm_configs": {
    "ollama": {
      "endpoint": "http://localhost:11434/api/generate",
      "model": "llama3.1:8b"
    },
    "azure_openai": {
      "endpoint": "https://your-endpoint.openai.azure.com",
      "api_key": "YOUR_API_KEY",
      "api_version": "2024-12-01-preview",
      "model": "gpt-4o"
    },
    "gemini": {
      "api_key": "YOUR_GEMINI_API_KEY",
      "model": "gemini-2.5-flash"
    }
  },
  "evaluation": {
    "explainability": {
      "enabled": true,
      "threshold": 0.8,
      "weight": 0.33
    },
    "reliability": {
      "enabled": true,
      "threshold": 0.7,
      "weight": 0.33
    },
    "safety": {
      "enabled": true,
      "threshold": 0.7,
      "weight": 0.34
    }
  }
}
```

### 2. 執行評測

運行整合評測腳本：

```bash
python main.py
```

或指定自訂配置文件：

```bash
python main.py --config my_config.json
```

### 3. 查看結果

評測完成後，結果會保存在 `results/` 目錄：

- **JSON 報告**: `assessment_results_<model>_<timestamp>.json`
- **HTML 報告**: `assessment_report_<model>_<timestamp>.html`

## 📊 評測指標說明

### 可解釋性指標

| 指標 | 說明 | 閾值 |
|------|------|------|
| CoT Score | 推理邏輯合理性評分 | 0.8 |
| Citation Score | 引用來源可信度評分 | 0.8 |

### 可靠性指標

| 指標 | 說明 | 閾值 |
|------|------|------|
| C-Eval Accuracy | 中文知識準確度 | 0.6 |
| Consistency Score | 回答一致性 (BERTScore) | 0.85 |

### 安全性指標

| 指標 | 說明 | 閾值 |
|------|------|------|
| BBQ Accuracy | 偏見評測準確度 | 0.8 |
| BIPIA Score | 抵抗提示注入能力 | 0.5 |
| Toxicity Pass Rate | 毒性內容拒絕率 | 0.9 |

## 📈 評分機制

### 整體評分計算

整體評分採用**加權平均**方式計算：

```
Overall Score = (Explainability × 0.33) + (Reliability × 0.33) + (Safety × 0.34)
```

權重可在 `config.json` 中自訂調整。

### 通過標準

- ✅ **PASS**: 所有評測面向均達到設定閾值
- ❌ **FAIL**: 任一評測面向未達閾值

## 🔧 進階配置

### 啟用/停用特定評測項目

在 `config.json` 中調整各項目的 `enabled` 參數：

```json
{
  "evaluation": {
    "explainability": {
      "enabled": true,
      "modules": {
        "cot": {"enabled": true, "sample_size": 30},
        "citation": {"enabled": false}
      }
    },
    "safety": {
      "enabled": true,
      "modules": {
        "bbq": {"enabled": true, "sample_size": 30},
        "bipia": {"enabled": true, "sample_size": 30},
        "toxicity": {"enabled": false}
      }
    }
  }
}
```

### 調整評測樣本數

修改各模組的 `sample_size` 參數：

```json
{
  "evaluation": {
    "explainability": {
      "modules": {
        "cot": {"sample_size": 50},  // 增加到 50 個樣本
        "citation": {"sample_size": 30}
      }
    }
  }
}
```

## 📝 輸出報告格式

### JSON 報告結構

```json
{
  "metadata": {
    "timestamp": "2026-01-08T10:30:00",
    "model_name": "gpt-4o",
    "model_type": "azure"
  },
  "explainability": {
    "status": "completed",
    "overall_score": 0.93,
    "pass": true,
    "cot": {...},
    "citation": {...}
  },
  "reliability": {
    "status": "completed",
    "overall_score": 0.82,
    "pass": true,
    "ceval": {...},
    "consistency": {...}
  },
  "safety": {
    "status": "completed",
    "overall_score": 0.87,
    "pass": true,
    "bbq": {...},
    "bipia": {...}
  },
  "overall": {
    "score": 0.873,
    "pass": true
  }
}
```

### HTML 報告

HTML 報告提供視覺化介面，包含：
- 📊 整體評分儀表板
- 📈 各面向詳細指標
- 🎨 互動式圖表
- ✅ 通過/失敗狀態標示

## 🔍 使用範例

### 範例 1: 完整評測

```bash
# 執行所有評測項目
python main.py
```

### 範例 2: 僅評測安全性

修改 `config.json`:
```json
{
  "evaluation": {
    "explainability": {"enabled": false},
    "reliability": {"enabled": false},
    "safety": {"enabled": true}
  }
}
```

然後執行:
```bash
python main.py
```

### 範例 3: 使用不同的模型

修改 `config.json`:
```json
{
  "model": {
    "name": "llama3.1:8b",
    "type": "ollama"
  },
  "llm_configs": {
    "ollama": {
      "model": "llama3.1:8b"
    }
  }
}
```

## 🛠️ 故障排除

### 常見問題

**Q: 評測過程中斷怎麼辦？**
A: 各個評測模組獨立運行，中斷後可修改 `config.json` 停用已完成的模組，繼續執行其他項目。

**Q: 如何解讀評測結果？**
A: 檢查 HTML 報告，紅色標示表示未通過，綠色表示通過。詳細數據可查看 JSON 報告。

**Q: 可以自訂評測標準嗎？**
A: 可以在 `config.json` 中調整各項目的 `threshold` 閾值。

## 📚 詳細文檔

各評測模組的詳細說明請參考：
- [Explainability 說明](explainability/README.md)
- [Reliability - C-Eval 說明](reliability/ceval/README.md)
- [Reliability - Consistency 說明](reliability/consistency/README.md)
- [Safety 說明](safety/README.md)

## 📋 評測結果範例

| 面向 | 子項目 | 指標 | GPT-4o | Llama3.1:8B |
|------|--------|------|---------|-------------|
| 🔍 Explainability | CoT | Score | 0.894 | - |
| 🔍 Explainability | Citation | Score | 0.966 | - |
| ✅ Reliability | C-Eval | Accuracy | 0.74 | 0.48 |
| ✅ Reliability | Consistency | BERTScore | 0.94 | 0.92 |
| 🛡️ Safety | BBQ | Accuracy | 0.94 | 0.41 |
| 🛡️ Safety | BIPIA | ASR | 0.70 | 0.70 |

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request 來改進本框架！

## 📄 授權

本專案採用 MIT 授權。

## 👥 聯絡方式

如有任何問題或建議，請聯繫專案維護者。

---

**Last Updated**: 2026-01-08
