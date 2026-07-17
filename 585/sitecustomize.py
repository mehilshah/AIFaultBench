import sys

import torch.distributed.run as distrib_run


def _boom(*args, **kwargs):
    raise RuntimeError("boom from injected sitecustomize")


distrib_run.run = _boom
sys.stderr.write("[sitecustomize] patched torch.distributed.run.run to raise RuntimeError\n")
