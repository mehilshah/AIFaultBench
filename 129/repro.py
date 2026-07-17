from ax import Client, RangeParameterConfig


def main() -> None:
    print("Starting Ax homepage sample repro")
    client = Client()
    client.configure_experiment(
        parameters=[
            RangeParameterConfig(
                name="x1",
                bounds=(-10.0, 10.0),
                parameter_type=ParameterType.FLOAT,
            ),
            RangeParameterConfig(
                name="x2",
                bounds=(-10.0, 10.0),
                parameter_type=ParameterType.FLOAT,
            ),
        ],
    )


if __name__ == "__main__":
    main()
