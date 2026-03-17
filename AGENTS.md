# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## Project Overview

Pure Python implementation of the Compact Frame Format (CFF) binary framing protocol. Single-file library with zero production dependencies, designed for hardware CRC peripheral compatibility and MCU use cases.

## Commands

```bash
# Install with dev + test dependencies
uv sync --all-extras

# Run all tests
python -m pytest

# Run tests with coverage (CI enforces 95% minimum)
python -m pytest --cov=compact_frame_format --cov-report=html --cov-fail-under=95

# Run a single test
python -m pytest tests/test_cff.py::TestFrameClass::test_frame_init_default

# Lint and format
ruff check .
ruff format --check .

# Auto-fix lint/format issues
ruff check --fix .
ruff format .

# Install pre-commit hooks
pre-commit install
```

## Architecture

The entire implementation lives in `compact_frame_format/cff.py` (~316 lines):

- **`Cff`** — Stateful frame handler. Creates frames with auto-incrementing counters (`create`), parses single frames (`parse`), finds frames in arbitrary byte streams (`find_frame`), and parses all frames from a stream (`parse_frames`).
- **`CFrame`** — Immutable dataclass representing a parsed frame (frame_counter, payload).
- **`ParseResultEnum`** — Enum of parse outcomes (SUCCESS, FRAME_TOO_SHORT, INVALID_PREAMBLE, INCOMPLETE_FRAME, HEADER_CRC_MISMATCH, PAYLOAD_CRC_MISMATCH, STRUCT_ERROR, UNEXPECTED_ERROR).
- **`FrameError`** — Exception class for frame operations.

**Frame wire format:** 2-byte preamble (`0xFACE`) + 2-byte LE counter + 2-byte LE payload size + 2-byte header CRC + variable payload + 2-byte payload CRC. CRC algorithm is CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF) with a pre-computed lookup table.

Public API is exported from `compact_frame_format/__init__.py`: `Cff`, `PREAMBLE`, `HEADER_SIZE_BYTES`, `PAYLOAD_CRC_SIZE_BYTES`.

## Testing

- `tests/test_cff.py` — Unit tests covering frame creation, parsing, CRC validation, edge cases.
- `tests/test_integration.py` — Integration tests using binary test data files in `tests/data/`, stream processing, and byte-level corruption resilience.
- Test data files (`tests/data/*.bin`) are pre-built binary frames; `stream.bin` is a concatenation of all individual frames.

## Code Quality

- **Ruff** for linting and formatting (line length 120, target Python 3.9+, rules: E/W/F/I/B/C4/UP).
- **Pre-commit hooks**: ruff linter, check-yaml, check-json, check-toml, check-case-conflict, check-merge-conflict.
- CI tests against Python 3.9, 3.10, 3.11, 3.12.
