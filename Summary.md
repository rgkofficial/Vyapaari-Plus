## Summary

This change completes a verified repository audit and fixes the highest-confidence startup, migration, security, lifecycle, timestamp, and UI asset defects found in the current `main` checkout.

## Fixes

- Register all runtime SQLAlchemy models with Alembic.
- Add migration `e032e5a4187a` for auth, product, supplier, purchase order, GRN, supplier invoice/payment, and supplier credit-ledger tables.
- Make `get_db_session()` a safe context manager that closes sessions.
- Replace single-round SHA-256 password hashing with PBKDF2-HMAC-SHA256 (600,000 iterations).
- Replace deprecated naive UTC timestamps in billing, purchase orders, and GRNs.
- Correct the desktop logo path to the tracked `assets/logo.jpg`.
- Add regression tests for hashing, session cleanup, and the logo asset.
- Update README and audit documentation to distinguish verified services from incomplete desktop screens and absent AI/OCR modules.

## Verification

- `python -m pytest -q`: **554 passed**.
- `python -m compileall -q app migrations tests`: passed.
- Clean SQLite `alembic upgrade head`: passed through `e032e5a4187a`.
- Clean migration creates 27 tables, including all auth/catalog/supplier/purchasing/GRN/billing/customer/business/inventory tables.
- `git diff --check`: passed.

## Remaining limitations

The desktop dashboard and stock-transfer/reconciliation UI are functional, while Products, Inventory, Billing/POS, Customers, Suppliers, Reports, and Settings remain service-status pages rather than full CRUD/data-entry screens. A PostgreSQL migration review is still required because an older migration creates billing foreign keys before the products table. The API user-creation endpoint remains an unauthenticated bootstrap route and should be restricted for production.
