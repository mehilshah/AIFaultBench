import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

import torch  # noqa: E402

from timm.models.eva import Eva  # noqa: E402
from timm.models.vision_transformer import VisionTransformer  # noqa: E402
from timm.optim._optim_factory import create_optimizer_v2  # noqa: E402


def summarize_optimizer(model, label):
    optimizer = create_optimizer_v2(
        model,
        opt="adamw",
        lr=1e-3,
        weight_decay=0.05,
        layer_decay=0.75,
    )
    id_to_name = {id(param): name for name, param in model.named_parameters()}
    groups = []
    for index, group in enumerate(optimizer.param_groups):
        names = [id_to_name[id(param)] for param in group["params"] if id(param) in id_to_name]
        groups.append(
            {
                "group": index,
                "lr_scale": group["lr_scale"],
                "weight_decay": group["weight_decay"],
                "names": names,
            }
        )
    print(f"{label} optimizer groups:")
    print(json.dumps(groups, indent=2))
    return groups


def find_group(groups, param_name):
    for group in groups:
        if param_name in group["names"]:
            return group
    return None


def check_vit():
    model = VisionTransformer(
        img_size=32,
        patch_size=16,
        num_classes=0,
        embed_dim=64,
        depth=1,
        num_heads=4,
        mlp_ratio=2.0,
        class_token=True,
        reg_tokens=1,
        no_embed_class=True,
        global_pool="avg",
    )
    nwd = model.no_weight_decay()
    groups = summarize_optimizer(model, "VisionTransformer")
    cls_group = find_group(groups, "cls_token")
    reg_group = find_group(groups, "reg_token")
    issues = []
    if "reg_token" not in nwd:
        issues.append("VisionTransformer.no_weight_decay() is missing 'reg_token'.")
    if cls_group is None:
        issues.append("VisionTransformer optimizer did not place cls_token in any group.")
    if reg_group is None:
        issues.append("VisionTransformer optimizer did not place reg_token in any group.")
    elif cls_group is not None and reg_group["group"] != cls_group["group"]:
        issues.append(
            "VisionTransformer reg_token is in a different layer-decay group than cls_token: "
            f"cls_token={cls_group}, reg_token={reg_group}."
        )
    return issues


def check_eva():
    model = Eva(
        img_size=32,
        patch_size=16,
        num_classes=0,
        embed_dim=64,
        depth=1,
        num_heads=4,
        class_token=True,
        num_reg_tokens=1,
        global_pool="avg",
        use_abs_pos_emb=True,
        use_rot_pos_emb=False,
    )
    nwd = model.no_weight_decay()
    groups = summarize_optimizer(model, "Eva")
    cls_group = find_group(groups, "cls_token")
    reg_group = find_group(groups, "reg_token")
    issues = []
    if "reg_token" not in nwd:
        issues.append("Eva.no_weight_decay() is missing 'reg_token'.")
    if cls_group is None:
        issues.append("Eva optimizer did not place cls_token in any group.")
    if reg_group is None:
        issues.append("Eva optimizer did not place reg_token in any group.")
    elif cls_group is not None and reg_group["group"] != cls_group["group"]:
        issues.append(
            "Eva reg_token is in a different layer-decay group than cls_token: "
            f"cls_token={cls_group}, reg_token={reg_group}."
        )
    return issues


def main():
    print(f"torch={torch.__version__}")
    issues = []
    issues.extend(check_vit())
    issues.extend(check_eva())
    if issues:
        raise AssertionError("\n".join(issues))
    print("No bug reproduced.")


if __name__ == "__main__":
    main()
