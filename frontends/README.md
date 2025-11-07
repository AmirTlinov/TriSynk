# TriSynk Frontend Prototypes

## trisynk-rs
- Location: `frontends/trisynk-rs/frontend.py`
- Usage: `frontends/trisynk-rs/frontend.py frontends/samples/sample.rs --output out.json`
- Emits JSON payload approximating `clmr` module with capabilities, ready for future lowering stages.

## trisynk-cpp
- Location: `frontends/trisynk-cpp/frontend.py`
- Usage: `frontends/trisynk-cpp/frontend.py frontends/samples/sample.cpp --output out.json`
- Produces ABI metadata including layout hash placeholders.

## Testing
Run `frontends/tests/run_smoke.sh` to execute both prototypes against sample sources and ensure JSON artifacts exist.
