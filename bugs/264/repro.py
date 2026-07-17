#!/usr/bin/env python3
from tinygrad import Tensor


def main() -> int:
  t = Tensor.arange(4, device="CPU:0")
  print(f"T.tolist()={t.tolist()}")

  got_1 = t.shard(("CPU:0", "CPU:1"), 0).realize().shrink(((2, 4),)).tolist()
  got_2 = t.shard(("CPU:1", "CPU:2"), 0).realize().shrink(((0, 2),)).tolist()

  print(f"1. T.shard(('CPU:0', 'CPU:1'), 0).realize().shrink(((2, 4),)).tolist()={got_1} - should be [2, 3]")
  print(f"2. T.shard(('CPU:1', 'CPU:2'), 0).realize().shrink(((0, 2),)).tolist()={got_2} - should be [0, 1]")

  if got_1 == [2, 3] and got_2 == [0, 1]:
    print("BUG NOT REPRODUCED")
    return 0

  print("BUG REPRODUCED")
  return 1


if __name__ == "__main__":
  raise SystemExit(main())
