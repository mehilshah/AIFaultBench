import timm


def main() -> int:
    model = timm.create_model("vit_base_patch16_dinov3.lvd1689m", pretrained=False)
    print(f"created_model={type(model).__name__}")
    print(f"rope_class={type(model.rope).__name__}")

    try:
        model.set_input_size(512)
    except Exception as exc:  # pragma: no cover - repro script
        print(f"exception={type(exc).__name__}: {exc}")
        return 1

    print("set_input_size succeeded unexpectedly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
