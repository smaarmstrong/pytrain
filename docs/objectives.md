# pytrain coverage objectives

The source of truth for what the catalogue must teach. Every objective below
maps to at least one task; a task's `meta.json` names its objective verbatim.
Advanced/bonus material is tagged `[advanced]` and carries the `advanced` tag
in meta.json. Target: ~15+ tasks per domain.

Grading philosophy: graders assert **behaviour**, never style — any correct
implementation passes. Randomness is seeded, time/network dependence avoided,
per-task third-party deps declared in `meta.json` `deps`.

## core — language core (target ≥ 18)

- [ ] list/dict/set comprehensions incl. nested and conditional
- [ ] generator expressions vs list comprehensions (laziness observable)
- [ ] generator functions: `yield`, generator state, `send`
- [ ] `yield from` and generator delegation [advanced]
- [ ] closures and variable capture (`nonlocal`, late binding pitfall)
- [ ] decorators: plain function decorator preserving metadata (`functools.wraps`)
- [ ] decorators with arguments (decorator factory)
- [ ] class decorators [advanced]
- [ ] context managers: class-based (`__enter__`/`__exit__`) incl. exception handling
- [ ] context managers: `contextlib.contextmanager`
- [ ] dunder methods: `__repr__`/`__str__`/`__eq__`/`__hash__`
- [ ] dunder methods: container protocol (`__len__`, `__getitem__`, `__contains__`, `__iter__`)
- [ ] dunder methods: operator overloading (`__add__`, `__lt__`, reflected ops)
- [ ] callable objects (`__call__`) and `__getattr__` delegation [advanced]
- [ ] unpacking: `*`/`**`, starred assignment, keyword-only and positional-only params
- [ ] exceptions: custom hierarchies, `raise ... from`, `else`/`finally`
- [ ] `match`/`case` structural pattern matching
- [ ] iterators: the protocol itself (`__iter__`/`__next__`, `StopIteration`)
- [ ] scoping: LEGB, mutable default argument pitfall
- [ ] f-strings incl. format specs, `=` debugging, nested quotes

## dsa — data structures & algorithms (target ≥ 20)

- [ ] stack & queue from first principles (list / deque)
- [ ] singly linked list: build, reverse, detect cycle
- [ ] binary search (index + bisect variants, rotated array [advanced])
- [ ] sorting: implement merge sort; stability observable
- [ ] sorting: quicksort or heapsort; `key=` based custom ordering
- [ ] heaps: heapq k-smallest / merge k sorted / priority queue with tie-breaks
- [ ] hash maps: frequency counting, two-sum-style lookups, anagram grouping
- [ ] sets: dedupe, intersection problems, sliding-window uniqueness
- [ ] binary tree: build, traversals (DFS pre/in/post, BFS by level)
- [ ] binary search tree: insert/validate/in-order [advanced]
- [ ] graphs: adjacency list, BFS shortest path (unweighted)
- [ ] graphs: DFS, cycle detection, topological sort
- [ ] graphs: Dijkstra with heapq [advanced]
- [ ] recursion: classic problems (permutations, subsets, flatten nested)
- [ ] dynamic programming: 1-D (fib/climb stairs/house robber pattern)
- [ ] dynamic programming: 2-D (grid paths, edit distance or LCS) [advanced]
- [ ] two pointers & sliding window (max window sum, longest substring)
- [ ] string algorithms: palindromes, run-length encoding, str manipulation
- [ ] big-O in practice: an O(n) requirement graded with a time budget on large N
- [ ] trie or union-find (pick one) [advanced]

## stdlib — the standard library (target ≥ 18)

- [ ] collections: Counter, defaultdict, deque
- [ ] collections: namedtuple / OrderedDict move_to_end LRU sketch
- [ ] itertools: islice, chain, groupby, pairwise
- [ ] itertools: product, permutations, combinations, accumulate [advanced]
- [ ] functools: lru_cache / cache, partial
- [ ] functools: reduce, singledispatch [advanced]
- [ ] dataclasses: basics, defaults, field(default_factory), frozen/eq/order
- [ ] dataclasses: `__post_init__`, InitVar [advanced]
- [ ] pathlib: traversal, globbing, reading/writing, path arithmetic
- [ ] re: groups, named groups, findall/finditer, sub with function
- [ ] re: greedy vs lazy, lookarounds [advanced]
- [ ] json: load/dump, custom encoder/object_hook, round-tripping
- [ ] argparse: subcommands, types, defaults, error exit codes
- [ ] logging: levels, handlers, formatters, getLogger hierarchy
- [ ] subprocess: run, capture, check, pipelines
- [ ] datetime & zoneinfo: parsing, arithmetic, tz conversion
- [ ] csv + sqlite3: load a CSV into SQLite and query it
- [ ] os/shutil/tempfile: env vars, dir trees, safe temp usage
- [ ] textwrap/string/secrets grab-bag [advanced]

## oop — OOP & design (target ≥ 14)

- [ ] classes: properties (getter/setter/deleter), class vs instance attrs
- [ ] classmethod / staticmethod (alternative constructors)
- [ ] inheritance & super() incl. cooperative multiple inheritance / MRO
- [ ] abstract base classes: abc.ABC, @abstractmethod
- [ ] protocols: structural typing with typing.Protocol (runtime_checkable)
- [ ] composition over inheritance (delegation exercise)
- [ ] descriptors: a validated-attribute descriptor [advanced]
- [ ] `__slots__` and object size/attribute control [advanced]
- [ ] pattern: strategy (swap behaviour via injected callables/objects)
- [ ] pattern: observer / pub-sub
- [ ] pattern: factory + registry (plugin lookup by name)
- [ ] pattern: adapter or facade over an awkward interface
- [ ] pattern: builder or fluent interface [advanced]
- [ ] enum: Enum, auto, StrEnum/IntEnum, Flag [advanced]

## typing — static typing (target ≥ 14)

Graded by behaviour AND, where noted, by running mypy in the task venv and
asserting zero errors (`mypy-clean`).

- [ ] annotate a real module: params, returns, Optional, unions (mypy-clean)
- [ ] generics: TypeVar-based generic functions (mypy-clean)
- [ ] generics: a generic container class (Stack[T]) (mypy-clean)
- [ ] PEP 695 `def f[T](...)` / `class C[T]` syntax [advanced, python>=3.12]
- [ ] Protocol: define + implement structurally (mypy-clean)
- [ ] TypedDict: required/NotRequired keys, nested (mypy-clean)
- [ ] Literal, Final, and enums in signatures
- [ ] overload: @typing.overload for a polymorphic function [advanced]
- [ ] Callable types, ParamSpec for decorators [advanced]
- [ ] Self type, __init_subclass__ typing niceties [advanced]
- [ ] NewType and type aliases (`type X = ...` on 3.12+ / TypeAlias)
- [ ] narrowing: isinstance/TypeGuard/TypeIs (mypy-clean)
- [ ] variance: covariant containers, Sequence vs list in APIs
- [ ] dataclasses + typing integration; typing at runtime via get_type_hints

## concurrency — threading, multiprocessing, asyncio (target ≥ 14)

- [ ] threading: Thread + join, Lock protecting shared state (race made visible)
- [ ] threading: producer/consumer with queue.Queue
- [ ] concurrent.futures: ThreadPoolExecutor map/submit/as_completed
- [ ] concurrent.futures: ProcessPoolExecutor for CPU-bound work
- [ ] multiprocessing: Pool, passing data, why pickling matters [advanced]
- [ ] GIL in practice: measure thread vs process speedup on CPU-bound task [advanced]
- [ ] asyncio: coroutines, await, asyncio.run
- [ ] asyncio: gather with concurrency observable (total time < sum of sleeps)
- [ ] asyncio: create_task, cancellation, timeouts (wait_for / asyncio.timeout)
- [ ] asyncio: async iterators / async generators
- [ ] asyncio: async context managers, locks, semaphores
- [ ] asyncio: TaskGroup and ExceptionGroup handling (3.11)
- [ ] asyncio: producer/consumer with asyncio.Queue
- [ ] bridging: run_in_executor / asyncio.to_thread [advanced]

## testing — testing & quality (target ≥ 14)

Meta-tasks: the learner WRITES tests/config; the grader runs their tests
against known-good and known-bad implementations to check they discriminate.

- [ ] pytest basics: write tests for a spec (must fail buggy impl, pass good one)
- [ ] fixtures: setup/teardown, fixture composition, yield fixtures
- [ ] parametrize: table-driven tests incl. ids and marks
- [ ] tmp_path / monkeypatch built-in fixtures
- [ ] mocking: unittest.mock.Mock, patch as decorator/context manager
- [ ] mocking: side_effect, call assertions, spec autospec [advanced]
- [ ] exceptions & warnings: pytest.raises, pytest.warns, match=
- [ ] approx & floats, comparing collections
- [ ] property-style testing: write a randomized (seeded) invariant test [advanced]
- [ ] coverage thinking: write tests reaching listed branches of a gnarly function
- [ ] doctest: make docstrings executable and correct
- [ ] TDD kata: implement code to make a provided failing suite pass
- [ ] ruff: fix a module until `ruff check` is clean without changing behaviour
- [ ] mypy as quality gate: type a module until mypy passes strict-ish flags

## packaging — venv, pyproject, build & distribute (target ≥ 10)

Graded via subprocess: build artefacts, installability, entry points.

- [ ] pyproject.toml: author metadata/deps for a given module (validates + builds)
- [ ] src layout: restructure a flat module into src/ package (import works installed)
- [ ] entry points: console_scripts that installs a working CLI
- [ ] build a wheel + sdist with `python -m build` / `uv build`; assert contents
- [ ] editable install & extras ([dev] extra with pytest) [advanced]
- [ ] version handling: __version__ single-sourced [advanced]
- [ ] dependency pinning: write constraints satisfying given scenario (resolver-checked)
- [ ] package data: include non-Python files and read them via importlib.resources
- [ ] uv workflows: lock + sync a small project [advanced]
- [ ] publishable checks: twine check / metadata validation [advanced]

## web — Flask, FastAPI, Django (target ≥ 18)

Graded with each framework's test client (no live servers, no ports).

- [ ] Flask: routes, methods, URL params, query strings, JSON in/out
- [ ] Flask: request validation + error handlers (abort, custom 404/400)
- [ ] Flask: blueprints and app factory
- [ ] Flask: sessions/cookies or before_request auth hook [advanced]
- [ ] FastAPI: path/query/body params with pydantic models
- [ ] FastAPI: response_model, status codes, HTTPException
- [ ] FastAPI: dependency injection (Depends), reusable deps
- [ ] FastAPI: async endpoints doing concurrent work [advanced]
- [ ] FastAPI: pydantic v2 validators, field constraints, nested models
- [ ] FastAPI: middleware / CORS / headers [advanced]
- [ ] FastAPI: a small CRUD API with in-memory store (full REST semantics)
- [ ] Django: models + ORM queries (tested via in-memory SQLite)
- [ ] Django: views + URLconf + JSON responses (test client)
- [ ] Django: forms or model validation [advanced]
- [ ] DRF: serializers + a ModelViewSet CRUD (APIClient) [advanced]
- [ ] auth pattern: token check via dependency/middleware in any framework
- [ ] pagination + filtering endpoint semantics
- [ ] httpx: write an API *client* with retries/timeouts against a mock transport

## data — numpy, pandas, polars, matplotlib, sklearn, SQLAlchemy (target ≥ 18)

Deterministic: fixed seeds, tiny in-repo datasets generated by the grader.

- [ ] numpy: array creation, dtypes, reshaping, slicing/fancy indexing
- [ ] numpy: broadcasting and vectorised arithmetic (no-loop constraint via timing)
- [ ] numpy: aggregation, axis semantics, boolean masking
- [ ] numpy: linalg basics (solve, norms) [advanced]
- [ ] pandas: construct/inspect DataFrames, dtypes, selection (loc/iloc)
- [ ] pandas: filtering, sorting, assign/derived columns
- [ ] pandas: groupby-aggregate incl. named aggregations
- [ ] pandas: joins/merges incl. how= semantics, concat
- [ ] pandas: missing data (isna/fillna/dropna) and type coercion
- [ ] pandas: time series (resample, rolling) [advanced]
- [ ] polars: the same core ops in polars expressions (select/filter/group_by/agg)
- [ ] polars: lazy frames and query optimisation observable [advanced]
- [ ] matplotlib: build a figure to spec — assert axes, labels, series data from the Figure object
- [ ] matplotlib: multi-panel subplots / twin axes [advanced]
- [ ] sklearn: train/test split + a pipeline (scaler + model), score threshold on a seeded synthetic set
- [ ] sklearn: cross-validation + GridSearchCV on a tiny grid [advanced]
- [ ] SQLAlchemy: Core — tables, insert/select on in-memory SQLite
- [ ] SQLAlchemy: ORM — models, relationships, session queries

## projects — composite, end-to-end (target ≥ 8)

Multi-file workspaces graded end-to-end. Each integrates several domains.

- [ ] CLI tool: argparse + pathlib + json — a todo/notes manager with subcommands
- [ ] text pipeline: read files, regex-extract, aggregate with collections, report
- [ ] REST API: FastAPI CRUD + validation + auth dependency, graded via httpx client
- [ ] data pipeline: CSV -> pandas clean/transform -> SQLite + summary output
- [ ] log analyser: parse real-ish logs, stats with itertools/collections, CLI output
- [ ] mini web app: Flask app factory + blueprint + forms/JSON + tests
- [ ] async scraper/worker: asyncio + httpx against a provided local mock (no network) [advanced]
- [ ] library: package a reusable module with pyproject, entry point and tests [advanced]
