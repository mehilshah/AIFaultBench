#!/usr/bin/env python3
"""Reproduce the Gemma4 streaming/non-streaming classification mismatch.

The local environment cannot import the full vLLM package because its torch
installation is broken. This harness loads the real
``vllm.parser.gemma4`` source file with a small in-memory stub package shell
so the actual parser class and its prompt-state logic run unchanged.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import traceback
import types
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"

PLAIN_ANSWER = "This is a direct final answer without channel markers."
STREAM_CHUNKS = [
    "This is a",
    " direct final answer",
    " without channel markers.",
]


def install_package(name: str, path: Path | None = None) -> None:
    module = types.ModuleType(name)
    module.__path__ = [str(path)] if path is not None else []
    sys.modules[name] = module


def install_stub_environment() -> None:
    install_package("vllm", CODEBASE / "vllm")
    install_package("vllm.parser", CODEBASE / "vllm" / "parser")
    install_package("vllm.parser.engine", CODEBASE / "vllm" / "parser" / "engine")
    install_package("vllm.entrypoints", CODEBASE / "vllm" / "entrypoints")
    install_package(
        "vllm.entrypoints.openai", CODEBASE / "vllm" / "entrypoints" / "openai"
    )
    install_package(
        "vllm.entrypoints.openai.engine",
        CODEBASE / "vllm" / "entrypoints" / "openai" / "engine",
    )

    logger_mod = types.ModuleType("vllm.logger")

    def init_logger(name: str):
        import logging

        return logging.getLogger(name)

    logger_mod.init_logger = init_logger
    sys.modules["vllm.logger"] = logger_mod

    events_mod = types.ModuleType("vllm.parser.engine.events")

    class EventType(Enum):
        TEXT_CHUNK = auto()
        REASONING_START = auto()
        REASONING_CHUNK = auto()
        REASONING_END = auto()
        TOOL_CALL_START = auto()
        TOOL_NAME = auto()
        ARG_VALUE_CHUNK = auto()
        TOOL_CALL_END = auto()

    @dataclass(slots=True)
    class SemanticEvent:
        type: EventType
        value: str = ""
        tool_index: int = -1

    events_mod.EventType = EventType
    events_mod.SemanticEvent = SemanticEvent
    sys.modules["vllm.parser.engine.events"] = events_mod

    cfg_mod = types.ModuleType("vllm.parser.engine.parser_engine_config")

    class ParserState(Enum):
        CONTENT = auto()
        REASONING = auto()
        TOOL_PREAMBLE = auto()
        TOOL_NAME = auto()
        TOOL_ARGS = auto()
        TOOL_BETWEEN = auto()

    @dataclass(frozen=True, slots=True)
    class Transition:
        next_state: ParserState
        events: tuple = ()
        skip_in_token_id_mode: bool = False

    @dataclass(frozen=True)
    class ParserEngineConfig:
        name: str
        terminals: dict = field(default_factory=dict)
        token_id_terminals: dict = field(default_factory=dict)
        transitions: dict = field(default_factory=dict)
        content_events: dict = field(default_factory=dict)
        initial_state: ParserState = ParserState.CONTENT
        arg_converter: object | None = None
        stream_arg_deltas: bool = True
        tool_args_json: bool = True
        arg_structural_chars: object | None = None
        preserve_tokens: frozenset = field(default_factory=frozenset)
        strip_trailing_reasoning_whitespace: bool = True
        drop_whitespace_only_content_before_tools: bool = True
        strip_content_whitespace_with_tools: bool = True
        validate_tool_names: bool = False

    cfg_mod.ParserState = ParserState
    cfg_mod.Transition = Transition
    cfg_mod.ParserEngineConfig = ParserEngineConfig
    sys.modules["vllm.parser.engine.parser_engine_config"] = cfg_mod

    proto_mod = types.ModuleType("vllm.entrypoints.openai.engine.protocol")

    @dataclass
    class DeltaMessage:
        content: str | None = None
        reasoning: str | None = None
        tool_calls: list | None = None

        def model_dump(self, exclude_none: bool = True):
            payload = {
                "content": self.content,
                "reasoning": self.reasoning,
                "tool_calls": self.tool_calls,
            }
            if exclude_none:
                return {k: v for k, v in payload.items() if v is not None}
            return payload

    proto_mod.DeltaMessage = DeltaMessage
    sys.modules["vllm.entrypoints.openai.engine.protocol"] = proto_mod

    parser_mod = types.ModuleType("vllm.parser.engine.parser_engine")

    class ParserEngine:
        def __init__(
            self,
            tokenizer,
            tools=None,
            *,
            parser_engine_config,
            model_config=None,
            **kwargs,
        ):
            self.model_tokenizer = tokenizer
            self._tools = tools
            self.parser_engine_config = parser_engine_config
            self._streaming_initialized = False
            self._reasoning_ended = False
            self.vocab = tokenizer.get_vocab()
            self._reasoning_start_token_id = self.vocab.get("<|channel>")
            self._reasoning_end_token_id = self.vocab.get("<channel|>")
            self._engine = SimpleNamespace(
                state=parser_engine_config.initial_state, reset=self._reset_engine
            )

        def _reset_engine(self, initial_state=None):
            self._engine.state = (
                initial_state
                if initial_state is not None
                else self.parser_engine_config.initial_state
            )

        def initialize_streaming(self, initial_state=None):
            if not self._streaming_initialized:
                self._streaming_initialized = True
                self._reset(initial_state=initial_state)

        def _reset(self, initial_state=None):
            self._reset_engine(initial_state)
            self._reasoning_ended = False

        def _preprocess_feed(self, delta_text, delta_token_ids):
            return delta_text, delta_token_ids

        def adjust_initial_state_from_prompt(self, prompt_token_ids):
            return

        def _events_to_delta(self, events, finished=False):
            if not events:
                return None
            reasoning = "".join(
                ev.value for ev in events if ev.type == events_mod.EventType.REASONING_CHUNK
            ) or None
            content = "".join(
                ev.value for ev in events if ev.type == events_mod.EventType.TEXT_CHUNK
            ) or None
            return proto_mod.DeltaMessage(content=content, reasoning=reasoning)

        def parse_delta(
            self,
            delta_text,
            delta_token_ids,
            request,
            prompt_token_ids=None,
            finished=False,
        ):
            if not self._streaming_initialized:
                self.adjust_initial_state_from_prompt(prompt_token_ids or [])
                self.initialize_streaming()

            text, _ = self._preprocess_feed(delta_text, delta_token_ids)
            if not text:
                return None

            state = self._engine.state
            if "<|channel>" in text:
                before, after = text.split("<|channel>", 1)
                events = []
                if before:
                    events.append(
                        events_mod.SemanticEvent(events_mod.EventType.TEXT_CHUNK, before)
                    )
                self._engine.state = cfg_mod.ParserState.REASONING
                if after:
                    events.append(
                        events_mod.SemanticEvent(
                            events_mod.EventType.REASONING_CHUNK, after
                        )
                    )
                return self._events_to_delta(events, finished=finished)

            if "<channel|>" in text:
                before, after = text.split("<channel|>", 1)
                events = []
                if before:
                    event_type = (
                        events_mod.EventType.REASONING_CHUNK
                        if state == cfg_mod.ParserState.REASONING
                        else events_mod.EventType.TEXT_CHUNK
                    )
                    events.append(events_mod.SemanticEvent(event_type, before))
                self._engine.state = cfg_mod.ParserState.CONTENT
                if after:
                    events.append(
                        events_mod.SemanticEvent(events_mod.EventType.TEXT_CHUNK, after)
                    )
                return self._events_to_delta(events, finished=finished)

            event_type = (
                events_mod.EventType.REASONING_CHUNK
                if state == cfg_mod.ParserState.REASONING
                else events_mod.EventType.TEXT_CHUNK
            )
            return self._events_to_delta(
                [events_mod.SemanticEvent(event_type, text)], finished=finished
            )

        def extract_reasoning(self, model_output, request):
            if "<|channel>" in model_output and "<channel|>" in model_output:
                _, rest = model_output.split("<|channel>", 1)
                reasoning, content = rest.split("<channel|>", 1)
                return reasoning or None, content or None
            return None, model_output or None

    parser_mod.ParserEngine = ParserEngine
    sys.modules["vllm.parser.engine.parser_engine"] = parser_mod


def load_gemma4_parser():
    spec = importlib.util.spec_from_file_location(
        "vllm.parser.gemma4", CODEBASE / "vllm" / "parser" / "gemma4.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["vllm.parser.gemma4"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.Gemma4Parser


class FakeTokenizer:
    bos_token_id = None
    eos_token_id = None
    pad_token_id = None

    def __init__(self):
        self._vocab = {
            "<|channel>": 100,
            "<channel|>": 101,
            "<|tool_call>": 102,
            "<tool_call|>": 103,
            "<|turn>": 104,
            "<|tool_response>": 105,
        }
        self._inverse_vocab = {token_id: token for token, token_id in self._vocab.items()}

    def get_vocab(self):
        return self._vocab

    def decode(self, token_ids):
        return "".join(self._inverse_vocab.get(tid, f"<token:{tid}>") for tid in token_ids)


def dump_delta(delta):
    if delta is None:
        return None
    if hasattr(delta, "model_dump"):
        return delta.model_dump(exclude_none=True)
    return {
        name: value
        for name in ("reasoning", "content", "tool_calls")
        if (value := getattr(delta, name, None)) is not None
    }


def main() -> int:
    install_stub_environment()
    Gemma4Parser = load_gemma4_parser()

    request = SimpleNamespace(tools=None, tool_choice=None)

    nonstream_parser = Gemma4Parser(
        FakeTokenizer(), chat_template_kwargs={"enable_thinking": True}
    )
    nonstream_reasoning, nonstream_content = nonstream_parser.extract_reasoning(
        PLAIN_ANSWER, request
    )

    stream_parser = Gemma4Parser(
        FakeTokenizer(), chat_template_kwargs={"enable_thinking": True}
    )
    prompt_token_ids = [stream_parser.vocab["<|turn>"]]
    stream_deltas = []
    for index, chunk in enumerate(STREAM_CHUNKS):
        delta = stream_parser.parse_delta(
            chunk,
            [],
            request,
            prompt_token_ids=prompt_token_ids if index == 0 else None,
            finished=False,
        )
        prompt_token_ids = None
        stream_deltas.append(dump_delta(delta))
    final_delta = stream_parser.parse_delta(
        "",
        [],
        request,
        prompt_token_ids=None,
        finished=True,
    )

    reproducible = (
        nonstream_reasoning is None
        and nonstream_content == PLAIN_ANSWER
        and all(item == {"reasoning": chunk} for item, chunk in zip(stream_deltas, STREAM_CHUNKS))
        and dump_delta(final_delta) is None
    )

    evidence = (
        "non-streaming="
        f"{(nonstream_reasoning, nonstream_content)!r}; "
        f"streaming_chunks={stream_deltas!r}; "
        f"finished={dump_delta(final_delta)!r}"
    )

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Load the real vLLM Gemma4 parser module through a stubbed package shell.",
            "Call non-streaming extract_reasoning() on plain text without channel markers.",
            "Stream the same text in chunks after a prompt ending with <|turn> and observe all chunks labeled as reasoning.",
        ],
        "blocking_reason": None if reproducible else "The mismatch did not reproduce in the local harness.",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("Gemma4 parser reproduction")
    print(f"non-streaming: reasoning={nonstream_reasoning!r}, content={nonstream_content!r}")
    print(f"streaming chunks: {stream_deltas!r}")
    print(f"final delta: {dump_delta(final_delta)!r}")
    print(f"reproducible: {reproducible}")

    return 0 if reproducible else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        RESULT_PATH.write_text(
            json.dumps(
                {
                    "reproducible": False,
                    "evidence": traceback.format_exc(),
                    "steps": [
                        "Load the Gemma4 parser through a stubbed vLLM package shell.",
                        "Run the non-streaming and streaming parser paths on the same plain answer.",
                    ],
                    "blocking_reason": "Unexpected exception while running the repro.",
                    "reproduction_command": "bash run_repro.sh",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise
