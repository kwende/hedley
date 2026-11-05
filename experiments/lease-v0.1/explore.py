"""Finite model experiment, not a verifier for production code. Python 3.10+."""

import argparse
from collections import deque
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class State:
    owner: str = "-"
    generation: int = 0
    active: bool = False
    done: bool = False
    token_a: int = 0
    token_b: int = 0


def token(state, worker):
    return state.token_a if worker == "A" else state.token_b


def step(state, action, fenced, max_claims):
    """Each transition is atomic. None means disabled, not an error response."""
    verb, *args = action.split()
    worker = args[0] if args else "-"
    if verb == "claim":
        if state.done or state.active or state.generation >= max_claims:
            return None
        generation = state.generation + 1
        return replace(
            state,
            owner=worker,
            generation=generation,
            active=True,
            **{"token_" + worker.lower(): generation},
        )
    if verb == "expire":
        return replace(state, active=False) if state.active and not state.done else None
    if verb == "complete":
        if state.done or token(state, worker) == 0:
            return None
        authorized = (
            state.active
            and state.owner == worker
            and token(state, worker) == state.generation
        )
        if fenced and not authorized:
            return None
        return replace(state, done=True, active=False)
    raise ValueError(action)


ACTIONS = ("claim A", "claim B", "expire", "complete A", "complete B")


def violation(state, action):
    if not action.startswith("complete "):
        return False
    worker = action.split()[1]
    return not (
        state.active
        and state.owner == worker
        and token(state, worker) == state.generation
    )


def explore(fenced, max_claims):
    initial = State()
    queue = deque([(initial, [])])
    seen = {initial}
    edges = 0
    bad = []
    while queue:
        state, path = queue.popleft()
        for action in ACTIONS:
            new = step(state, action, fenced, max_claims)
            if new is None:
                continue
            edges += 1
            trace = path + [action]
            if violation(state, action):
                bad.append(trace)
            if new not in seen:
                seen.add(new)
                queue.append((new, trace))
    return len(seen), edges, bad


def replay(actions, fenced, max_claims):
    state = State()
    print("  initial:", state)
    for action in actions:
        new = step(state, action, fenced, max_claims)
        if new is None:
            print(" ", action, "=> BLOCKED; state unchanged")
        else:
            state = new
            print(" ", action, "=>", state)
    return state


def checks():
    for bound in (1, 2, 3):
        assert explore(False, bound)[2], "Known defect was not detected"
        assert not explore(True, bound)[2], "Fenced model admitted stale completion"
    state = step(State(), "claim A", True, 3)
    assert step(state, "complete A", True, 3).done
    assert step(state, "claim B", True, 3) is None
    state = step(state, "expire", True, 3)
    state = step(state, "claim B", True, 3)
    assert step(state, "complete A", True, 3) is None
    assert step(state, "complete B", True, 3).done
    print("Self-checks passed: defect detection, exclusion, stale rejection, valid progress.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-claims", type=int, default=3)
    parser.add_argument("--mode", choices=["before", "after", "both"], default="both")
    parser.add_argument("--trace")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.max_claims < 1:
        parser.error("--max-claims must be positive")
    if args.self_test:
        checks()
    modes = ("before", "after") if args.mode == "both" else (args.mode,)
    for mode in modes:
        fenced = mode == "after"
        print("\n" + mode.upper())
        if args.trace:
            replay([action.strip() for action in args.trace.split(";") if action.strip()], fenced, args.max_claims)
        else:
            count, edges, bad = explore(fenced, args.max_claims)
            print(f"{count} reachable states; {edges} transitions; {len(bad)} unauthorized completion edges")
            if bad:
                print("Shortest counterexample:", " -> ".join(bad[0]))
            else:
                print("Property holds in this finite model only; no implementation correspondence established.")


if __name__ == "__main__":
    main()

