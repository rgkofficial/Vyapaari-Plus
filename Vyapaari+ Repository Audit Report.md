# Vyapaari+ Repository Audit Report

**Audit date:** 2026-11-02
**Repository:** `mohitraj8503/Vyapaari-Plus`
**Audited revision:** `43b435f` plus the fixes in this working tree

## Executive summary

The repository contains a working Python service layer for GST calculations, product and supplier services, purchase orders/GRNs, billing, customer Udhaar, reports, authentication/RBAC, alerts, and multi-branch stock transfers. The desktop shell has a functional dashboard and transfer/reconciliation UI; most other navigation entries remain service-status pages rather than full data-entry screens.

The previous audit documentation overstated completion and did not match the checked-in code. This audit verified the code directly, fixed the highest-confidence integration defects, and added regression coverage.

## Verification

- Dependencies installed from `requirements.txt` in `.venv` on Python 3.12.3.
- Final suite: **554 tests passed**.
- `python -m compileall -q app migrations tests`: passed.
- Clean SQLite migration: passed through `e032e5a4187a`.
- Clean migration creates **27 tables**, including auth, products, suppliers, purchasing, GRNs, supplier credit, billing, customer ledger, business, and inventory tables.
- `git diff --check`: passed.
- No tracked `.env`, SQLite database, log, or compiled artifact was found in the final diff.

## Prioritized findings and fixes

| ID | Severity | Area | Finding | Fix | Regression/verification |
|---|---|---|---|---|---|
| AUD-01 | Critical | Migrations | `migrations/env.py` imported only inventory models; clean upgrades omitted users, products, suppliers, purchasing, GRNs, and supplier credit tables. | Registered all model modules and added revision `e032e5a4187a`. | Clean `alembic upgrade head`; required-table assertion. |
| AUD-02 | High | DB lifecycle | `get_db_session()` returned a session from a `finally` block that did nothing, providing no safe close boundary. | Converted it to a context manager that yields and closes the session. | `tests/unit/test_core_hardening.py`. |
| AUD-03 | High | Authentication | Passwords were hashed with one SHA-256 round, despite the older report claiming PBKDF2. | Switched to PBKDF2-HMAC-SHA256 with 600,000 iterations and constant-time verification. | `tests/unit/test_core_hardening.py`; auth regression suite. |
| AUD-04 | Medium | Time handling | Billing cancellation, purchase orders, and GRNs used deprecated naive `datetime.utcnow()`. | Replaced with timezone-aware UTC timestamps. | Full suite and compile check; no remaining `datetime.utcnow` in app/migrations. |
| AUD-05 | Medium | Desktop UI | The UI referenced missing `assets/logo1.png`; the tracked asset is `assets/logo.jpg`. | Corrected the path. | `tests/unit/test_core_hardening.py`. |
| AUD-06 | Medium | Documentation | README and prior audit logs claimed AI modules, full screens, and 531/89% verification that were not reproducible from this checkout. | README now distinguishes verified services from UI limitations and absent AI/OCR modules; verification is 554 tests. | Manual README/source comparison. |

## Areas reviewed

### Startup, configuration, and persistence

`app.main` registers runtime models and initializes SQLite with `create_all`; API sessions close correctly through the FastAPI dependency. Alembic now discovers all model modules. The application still uses a development fallback secret key, so production deployment must set `APP_SECRET_KEY` and other secrets explicitly.

### Money, billing, GST, and ledgers

The GST package uses `Decimal`, validates state codes/GSTIN shape and checksum, handles CGST/SGST/IGST, cess, reverse charge, invoice round-off, credit-note rules, e-invoice/e-way payload validation, and QR/signing fallbacks. Billing uses idempotency keys, stock checks, Decimal totals, payment validation, invoice numbering, and rollback handling. Existing tests cover odd-paise splits, discounts, split payments, transfer rollback, customer balance invariants, and exports.

### Inventory transfers

Transfer creation rejects same-branch requests and invalid quantities/costs, supports idempotency keys, deducts source stock atomically, records delivery and carrier events, supports cancellation, and reconciles received/damaged/missing quantities. Existing transfer tests cover conservation, duplicate prevention, cancellation, failure rollback, and reconciliation approval flows.

### Purchasing and supplier credit

Purchase orders, GRNs, supplier invoices/payments, and supplier credit-ledger models/services are present and covered by the existing purchase/GRN/ledger tests. The new migration makes these models available on clean databases instead of relying on `create_all` side effects.

### UI, API, reports, and AI

The API exposes health, auth, business, billing, customer payment, alerts, reports, and transfer routes. Excel/PDF report paths are present. The desktop dashboard and transfer/reconciliation screens are connected; other navigation pages report service availability and do not yet provide complete CRUD/POS forms. There is no `app/ai`, OCR, Prophet, or OpenAI/Ollama implementation in this checkout, so those README vision claims are not verified features.

## Remaining risks and limitations

1. Historical migration `8c3d7e1a4b20` creates billing tables that reference `products` before the new products migration. SQLite accepts this because foreign-key enforcement is normally disabled during DDL; a PostgreSQL migration path needs a reordered baseline or a database-specific migration review.
2. `init_db()` uses `create_all` and should be reserved for local development; production deployments should use Alembic.
3. API user creation is currently an unauthenticated bootstrap endpoint and should be protected or disabled after the first owner account is created.
4. Customer and supplier ledger writes are session-local in some service methods; callers must preserve the documented transaction boundary when composing operations.
5. The desktop application is not a complete data-entry POS/catalog application yet.

## Files changed in this audit

- `app/db/session.py`
- `app/core/security.py`
- `app/modules/billing/service.py`
- `app/modules/purchasing/models.py`
- `app/modules/purchasing/grn_models.py`
- `app/ui/main_window.py`
- `migrations/env.py`
- `migrations/versions/e032e5a4187a_add_auth_catalog_supplier_and_.py`
- `tests/unit/test_core_hardening.py`
- `README.md`
