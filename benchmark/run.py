# -*- coding: utf-8 -*-

from collections.abc import Callable
from pathlib import Path
import timeit

import pytomlpp
import qtoml
import rtoml
import toml #type: ignore
import tomlkit

import tomli


def benchmark(
    name: str,
    run_count: int,
    func: Callable,
    col_width: tuple,
    compare_to: float | None = None,
) -> float:
    placeholder = "Running..."
    # print(f"{name:>{col_width[0]}} | {placeholder}", end="", flush=True)
    print("%s | %s" % (name, placeholder), end="", flush=True)
    time_taken = timeit.timeit(func, number=run_count)
    print("\b" * len(placeholder), end="")
    time_suffix = " s"
    # print(f"{time_taken:{col_width[1]-len(time_suffix)}.3g}{time_suffix}", end="")
    print("%s%s" % (time_taken,time_suffix), end="")
    if compare_to is None:
        print(" | baseline (100%)", end="")
    else:
        delta = compare_to / time_taken
        # print(f" | {delta:.2%}", end="")
        print(" | %s" % delta, end="")
    print()
    return time_taken


def run(run_count):
    #type(int) -> None
    data_path = Path(__file__).parent / "data.toml"
    test_data = data_path.read_bytes().decode(encoding = 'utf8')

    # qtoml has a bug making it crash without this newline normalization
    test_data = test_data.replace("\r\n", "\n")

    col_width = (10, 10, 28)
    col_head = ("parser", "exec time", "performance (more is better)")
    print("Parsing data.toml %s times:" % run_count)
    print("-" * col_width[0] + "---" + "-" * col_width[1] + "---" + col_width[2] * "-")
    print(
        # f"{col_head[0]:>{col_width[0]}} | {col_head[1]:>{col_width[1]}} | {col_head[2]}"
        "%s | %s | %s" % col_head
    )
    print("-" * col_width[0] + "-+-" + "-" * col_width[1] + "-+-" + col_width[2] * "-")
    # fmt: off
    baseline = benchmark("rtoml", run_count, lambda: rtoml.loads(test_data), col_width)  # noqa: E501
    benchmark("pytomlpp", run_count, lambda: pytomlpp.loads(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("tomli", run_count, lambda: tomli.loads(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("toml", run_count, lambda: toml.loads(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("qtoml", run_count, lambda: qtoml.loads(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("tomlkit", run_count, lambda: tomlkit.parse(test_data), col_width, compare_to=baseline)  # noqa: E501
    # fmt: on


if __name__ == "__main__":
    run(5000)
