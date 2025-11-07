# TriSynk Frontend Prototypes

## trisynk-rs
- Location: `frontends/trisynk-rs/frontend.py`
- Usage: `frontends/trisynk-rs/frontend.py frontends/samples/sample.rs --output out.json`
- Emits JSON payload approximating `clmr` module with capabilities, ready for future lowering stages. Additional fixtures live in `frontends/samples/*.rs` (e.g., `borrows.rs`).

## trisynk-cpp
- Location: `frontends/trisynk-cpp/frontend.py`
- Usage: `frontends/trisynk-cpp/frontend.py frontends/samples/sample.cpp --output out.json`
- Produces ABI metadata including layout hash placeholders. Additional fixtures: `frontends/samples/templates.cpp`.

## Testing
Run `frontends/tests/run_smoke.sh` or `scripts/test_frontends.py` to execute both prototypes against every sample source and ensure JSON artifacts conform to `schema/frontend_ir.schema.json`.
