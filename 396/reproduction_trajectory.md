# Reproduction Trajectory — Bug 396: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/730](https://github.com/huggingface/peft/issues/730)
- **Repository:** huggingface/peft @ `30fd5a4c88db369e87eab27ebf01c0b28bed02dc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny BertForSequenceClassification model from config so no network download is needed.
2. Wrap it with get_peft_model() using AdaLoraConfig with task_type='SEQ_CLS', target_modules=['query', 'value'], and lora_dropout=0.
3. Observe the TypeError when AdaLoraLayer.update_layer() stores a plain function in nn.ModuleDict.

## Observed behavior

- Running get_peft_model() on a tiny BertForSequenceClassification with AdaLoraConfig(lora_dropout=0) raises TypeError: peft.tuners.adalora.AdaLoraLayer.update_layer.<locals>.lora_dropout_layer is not a Module subclass. The failing code is in codebase/src/peft/tuners/adalora.py:342-352.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
