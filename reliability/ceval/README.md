# C-Eval

基於 `lm-evaluation-harness` 的評測腳本，使用 C-Eval 評測 LLM 的可靠性。

## Installation

Python version: 3.12

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Usage

```shell
python run_ceval.py \
    --split valid \
    --model_args pretrained=Qwen/Qwen2.5-0.5B-Instruct \
    --output_path outputs \
    --log_samples
```

### Arguments

- `--split`: `valid` or `test`. 選擇要使用 valid set 或 test set
- `--model_args`: huggingface model arguments
- `--log_samples`: 保留模型輸出
- `--output_path`: 輸出路徑
