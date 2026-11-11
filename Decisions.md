# Design Decisions

## 1. Why Python?
Because it has strong AI + automation libraries.

---

## 2. Why offline wake word?
To reduce latency and avoid internet dependency.

---

## 3. Why modular architecture?
So each feature can be improved independently.

---

## 4. Why no full UI initially?
Focus on functionality first.

---

## 5. Why a reusable confirmation mechanism?
Actions with meaningful side effects should be confirmed before execution. The confirmation component is independent of application execution so it can be reused for future sensitive actions.

The confirmation component reads affirmative and negative keywords from the intent configuration, returns a result, and never executes the pending action itself. Unknown responses are not interpreted as consent.

---

## 6. Why keep Kayal termination separate?
Commands that close external applications are different from commands that terminate Kayal. Kayal's own exit commands remain in `src/config/termination.py`.
