# GEMINI.md — Project Rules for "Image Classifier for Fruits"

> **Source of truth:** [`PROJECT_WORKFLOW.md`](file:///e:/codepro1/PROJECT_WORKFLOW.md)
> **Last updated:** 2026-10-03 (Phase 0 — Reconnaissance)

---

## Locked Decisions

| Decision | Choice | Rationale |
|---|---|---|
| ML Framework | TensorFlow / Keras 2.20.0 (CPU) | Installed, matches workflow spec |
| Frontend Framework | React + Vite | Workflow default |
| UI Libraries | React Bits (copy-paste, plain CSS) + Vengeance UI (copy-paste, Tailwind + Framer Motion + Radix) | User-approved; extra deps accepted |
| Dataset | Fruits-360 (Kaggle) — apple, banana, orange only | License to be verified in Phase 1 |
| Package manager (Python) | pip | Already in use |
| Package manager (JS) | npm | Already in use |

---

## Non-Negotiable Rules

1. **Single-phase execution:** Work only on the phase explicitly named by the user. Do not start the next phase until the user says to proceed.
2. **Checklist is the source of truth:** Read `PROJECT_WORKFLOW.md` at the start of each session. Use the active phase checklist as the task boundary.
3. **No scope expansion:** Do not add features, files, libraries, pages, services, or infrastructure unless required by the active phase or explicitly approved by the user.
4. **Plan before editing:** First inspect the repository and report a short plan listing the exact files to create/change. Wait for approval before edits when the change is more than a small, clearly scoped task.
5. **Protect existing work:** Never delete, overwrite, or mass-reformat existing files without explaining why and receiving approval.
6. **No fake completion:** Do not mark a checklist item complete unless the relevant file exists and/or the command or test has actually succeeded.
7. **No invented APIs:** Verify package names, imports, components, and CLI flags from installed packages or their official documentation. Do not guess package names or APIs.
8. **No secret leakage:** Never print, commit, or expose API keys, tokens, passwords, or `.env` contents. This project should not require a paid API key.
9. **Dataset integrity:** Do not scrape websites, bypass access controls, or download datasets from untrusted sources. Use a small public dataset with its license/terms checked, or ask the user to provide images. Record the dataset source and class counts.
10. **Reproducibility:** Use a fixed random seed where supported. Record image size, split ratios, classes, training settings, and evaluation metrics.
11. **Correct evaluation:** Split train/validation/test data without leakage. Do not claim accuracy until evaluation actually runs. Do not train or evaluate on the test set repeatedly to tune the model.
12. **Safe uploads:** Validate file type and size on the server. Handle corrupt or unsupported images with a clear error. Do not execute uploaded files.
13. **Small changes:** Prefer minimal, understandable code. Avoid unnecessary abstractions and premature optimization.
14. **No hidden actions:** Do not install packages, change global settings, modify system files, or run destructive commands without asking first.
15. **No unapproved substitutions:** If a requested UI library, dependency, dataset, or model framework is unavailable, explain the blocker and ask the user before choosing an alternative.
16. **Report at phase end:** List files changed, commands run, actual results, unresolved issues, and checklist items completed. Stop after the phase report.
17. **Do not fabricate:** Never invent metrics, screenshots, test results, dataset sources, or completion status.
18. **Keep PROJECT_WORKFLOW.md current:** Update checkboxes only after verifying the corresponding work. Do not rewrite the workflow or change the plan without approval.

---

## Environment Snapshot (Phase 0)

| Tool | Version |
|---|---|
| Python | 3.12.0 |
| pip | 26.1.1 |
| Node.js | v24.17.0 |
| npm | 11.13.0 |
| TensorFlow | 2.20.0 (CPU, oneDNN) |
| FastAPI | 0.117.1 |
| Uvicorn | 0.36.0 |
| NumPy | 2.2.6 |
| Matplotlib | 3.10.5 |
| scikit-learn | 1.7.1 |
| Pillow | 11.3.0 |
| CUDA | Not available (CPU-only) |
