import sys

import torch

sys.path.insert(0, "codebase")

from x_transformers import XTransformer


def main() -> None:
    torch.manual_seed(0)

    batch_size = 1
    num_tokens = 202
    enc_seq_len = 258
    dec_seq_len_base = 30
    dec_seq_len = dec_seq_len_base + 1

    model = XTransformer(
        dim=64,
        tie_token_emb=True,
        return_tgt_loss=True,
        enc_num_tokens=num_tokens,
        enc_depth=2,
        enc_heads=4,
        enc_max_seq_len=enc_seq_len,
        dec_num_tokens=num_tokens,
        dec_depth=2,
        dec_heads=4,
        dec_max_seq_len=dec_seq_len,
    )

    src = torch.randint(2, num_tokens, (batch_size, enc_seq_len))
    tgt = torch.cat(
        (torch.ones((batch_size, 1), dtype=torch.long), src[:, :dec_seq_len_base]),
        dim=1,
    )
    src_mask = torch.ones(batch_size, src.shape[1]).bool()

    model.train()
    loss = model(src, tgt, mask=src_mask)
    print(f"training loss: {loss.item():.6f}", flush=True)
    loss.backward()
    print("backward completed", flush=True)

    model.eval()
    start_tokens = torch.ones((batch_size, 1), dtype=torch.long)
    print("calling generate...", flush=True)
    sample = model.generate(src, start_tokens, enc_seq_len, mask=src_mask)
    print(f"generated sample shape: {tuple(sample.shape)}", flush=True)


if __name__ == "__main__":
    main()
