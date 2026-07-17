
## 16. Language detection via lingua-rs (the last Python surface)

`num2words_sentence(lang=None)` now detects in Rust. Exact parity with
Python's langdetect is impossible AND undesirable — langdetect mis-detects
short text badly ('Compré 6 manzanas' -> en, Chinese -> ko). The port swaps
the engine deliberately:

- Script-exclusive languages (zh/ja/ko/ar/he/th/hi/el) are identified from
  Unicode ranges at zero model cost (kana -> ja, hangul -> ko, Han -> zh).
- lingua-rs (25 Latin/Cyrillic models) separates shared-alphabet languages.
- The Python regex heuristics remain as the last resort, but WITHOUT the
  0.7-confidence gate: lingua's normalized confidences over 25 candidates
  rarely clear 0.7 on short text, and the heuristics are worse (the Italian
  \bi\b pattern matches English "I").

Agreement with the Python oracle: 43/49 (88%); every disagreement is lingua
being right or both being arbitrary — none favors langdetect.

Size is the real cost: each lingua high-accuracy model is ~5.7MB, so the
full build is a 144MB .so / 97MB wheel (just under PyPI's 100MB limit).
Cargo feature `lang-detect` (default on) gates it: `maturin build
--no-default-features` produces the 5.8MB slim .so where lang=None falls
back to the Python chain, byte-identical to before. First detection pays
~6ms lazy model decompression; subsequent calls <1ms.
