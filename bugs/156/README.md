# Bug 156

This folder reproduces the EoMT fast image processor crash when a CUDA segmentation map reaches the slow NumPy-based mask conversion helper.

## Repro

1. Create the environment:
   `bash setup_env.sh`
2. Run the repro:
   `bash run_repro.sh`
3. Inspect:
   `repro_stdout.log`
   `repro_stderr.log`

## What Fails

The failing call path is:
`EomtImageProcessorFast.preprocess -> convert_segmentation_map_to_binary_masks -> np.unique(cuda_tensor)`

The reproduced exception is:
`TypeError: can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.`
