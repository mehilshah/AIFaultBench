# Reproduction Trajectory — Bug 016: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11042](https://github.com/tensorflow/models/issues/11042)
- **Repository:** tensorflow/models @ `abb7ed6a4628118042876c17ba48c559e0fb5025`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read bug_report.txt and compared it with the checked-in resnet gpu.yaml.
2. Inspected classifier_trainer.py, distribute_utils.py, and dataset_factory.py for multi-worker setup and input sharding.
3. Ran bash run_repro.sh to capture the evidence in repro_stdout.log and repro_stderr.log.
4. Determined that the reported multi-node GPU throughput issue cannot be validated in this folder because there is no 2-node GPU cluster here.

## Observed behavior

- The checked-in codebase/official/legacy/image_classification/configs/examples/resnet/imagenet/gpu.yaml uses distribution_strategy: 'mirrored' and num_gpus: 1, which does not match the report's multi_worker_mirrored setup.
- classifier_trainer.py still calls distribute_utils.configure_cluster(params.runtime.worker_hosts, params.runtime.task_index) before selecting the distribution strategy.
- official/common/distribute_utils.py contains an explicit multi_worker_mirrored branch that returns tf.distribute.experimental.MultiWorkerMirroredStrategy.
- dataset_factory.py shards non-TFDS datasets across input pipelines when input_context.num_input_pipelines > 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The standardized folder does not provide the hardware or cluster topology required to measure multi-node GPU throughput, and the repo's checked-in resnet gpu.yaml is single-worker mirrored rather than the multi_worker_mirrored configuration described in the report.
