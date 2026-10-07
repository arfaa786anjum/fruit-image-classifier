# Fruit Image Classifier — 3-Day Project Workflow

> **Project title:** Image Classifier for Fruits  
> **Goal:** Train a small CNN to classify fruit images (initial classes: apple, banana, orange) and provide a clean React web interface for uploading an image and viewing the predicted class and confidence.  
> **Schedule:** 3 days, 5 controlled phases.  
> **Execution rule:** Gemini CLI must follow only the active phase and its checklist. Do not begin later phases, add unrequested features, or change the approved stack without asking.

---

## 1. Project scope

### Required deliverables
- A small, clearly documented fruit-image dataset workflow.
- A CNN image-classification training script.
- Training/validation metrics and a saved model.
- A prediction interface that accepts an image and displays the predicted fruit and confidence.
- A React frontend with a polished, responsive UI.
- A backend/API that loads the trained model and serves predictions.
- README with setup, run, and test instructions.
- Basic tests and a final checklist.

### Initial classes
- `apple`
- `banana`
- `orange`

Keep the class list small for the three-day timeline. Add more classes only if the user explicitly approves it.

### Suggested stack
- **ML:** Python, TensorFlow/Keras, NumPy, Matplotlib, scikit-learn
- **API:** Python + FastAPI, Uvicorn
- **Frontend:** React + Vite
- **UI:** React Bits and Vengence UI *only if their package/docs are available and compatible*. Verify the exact package names and installation instructions before using them. If either library cannot be verified or installed, stop and ask before substituting; do not silently invent packages.
- **Image handling:** Pillow
- **Testing:** pytest for Python; the existing frontend test setup if one is already present.

Use one package manager per part of the app, based on existing repository conventions. Do not introduce Docker, a database, authentication, cloud hosting, or a paid API.

---

## 2. Non-negotiable Gemini CLI rules

Copy these rules into the repository's `GEMINI.md` (or merge them into the existing file without deleting existing useful rules).

1. **Single-phase execution:** Work only on the phase explicitly named by the user. Do not start the next phase until the user says to proceed.
2. **Checklist is the source of truth:** Read this file at the start of each session. Use the active phase checklist as the task boundary.
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
18. **Keep this file current:** Update checkboxes only after verifying the corresponding work. Do not rewrite the workflow or change the plan without approval.

---

## 3. Repository layout target

Use this as the intended layout, adapting only when an existing repository already has a sensible structure.

```text
fruit-image-classifier/
├── GEMINI.md
├── PROJECT_WORKFLOW.md
├── README.md
├── .gitignore
├── ml/
│   ├── requirements.txt
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── data/
│   │   ├── README.md
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   ├── models/
│   ├── reports/
│   └── tests/
├── backend/
│   ├── requirements.txt
│   ├── main.py
│   └── tests/
└── frontend/
    ├── package.json
    ├── index.html
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── components/
        ├── styles/
        └── assets/
```

Do not create empty folders/files merely to match this tree. Create them when the active phase needs them. Keep generated datasets and model binaries out of version control unless there is a specific reason to include them.

---

## 4. Three-day phase plan

| Day | Phase | Outcome |
|---|---|---|
| Day 1 — morning | Phase 1: Repository, requirements, dataset | Scope and data ready |
| Day 1 — afternoon | Phase 2: CNN training and evaluation | Trained model and honest metrics |
| Day 2 | Phase 3: Prediction API | Working `/health` and `/predict` endpoints |
| Day 3 — morning | Phase 4: React UI | Responsive upload-and-predict interface |
| Day 3 — afternoon | Phase 5: Integration, tests, documentation | End-to-end demo and final README |

This is a target schedule, not a guarantee. Dataset access, installation problems, and training time may affect completion. If blocked, report the blocker rather than skipping tests or pretending the task succeeded.

---

# Phase 1 — Setup, scope, and dataset

**Target:** Day 1, morning  
**Exit condition:** Environment and dataset are documented, class folders are valid, and no model training has started.

## Phase 1 checklist
- [x] Inspect the current repository and existing instructions.
- [x] Confirm Python and Node.js versions and package-manager availability.
- [x] Confirm the selected UI libraries' exact names, official docs, compatibility, and installation steps.
- [x] Create/confirm `GEMINI.md` and `PROJECT_WORKFLOW.md`.
- [x] Create the minimal Python and React project structure needed for this plan.
- [x] Select a small dataset or ask the user to provide images.
- [x] Verify license/terms and document the source.
- [x] Organize images into `train`, `validation`, and `test` folders for each class.
- [x] Check class counts, unsupported files, and corrupted images.
- [x] Add `.gitignore` for virtual environments, node modules, caches, local data, and generated model artifacts as appropriate.
- [x] Update only Phase 1 checkboxes that have been verified.

## Phase 1 master prompt

```text
You are Gemini CLI acting as a careful project engineer for the project
"Image Classifier for Fruits".

ACTIVE PHASE: PHASE 1 ONLY — SETUP, SCOPE, AND DATASET.

Read GEMINI.md and PROJECT_WORKFLOW.md first. If either does not exist,
inspect the repository and propose creating it. Follow all project rules.

Goal:
Prepare the minimum repository structure and a small, legally usable image
dataset for apple, banana, and orange classification.

Allowed tasks:
1. Inspect the current repository and report its structure.
2. Check installed Python, Node.js, npm/pnpm/yarn availability without
   changing global configuration.
3. Verify React Bits and Vengence UI package names and official installation
   documentation. Do not guess. If "Vengence UI" is ambiguous or cannot be
   verified, stop and ask me to confirm the intended library.
4. Propose the exact files/folders to create or change before editing.
5. After approval, create only the minimal Phase 1 files and folder structure.
6. Find or use a small public dataset only after checking its source and terms,
   or ask me to supply images if safe, suitable data cannot be verified.
7. Document class names, source, license/terms, counts, image formats, and
   the train/validation/test split.
8. Validate that files can be opened as images and that each required class
   has enough examples for a meaningful small demo.
9. Add an appropriate .gitignore without deleting existing rules.

Data split target: 70% train, 15% validation, 15% test, stratified by class
where possible. Avoid duplicate or near-duplicate images across splits.
Use a fixed seed where supported.

Strict limits:
- Do not train a model in Phase 1.
- Do not implement the backend or UI.
- Do not add extra fruit classes.
- Do not add Docker, a database, authentication, cloud services, or paid APIs.
- Do not install anything globally.
- Do not overwrite or delete existing work.
- If dataset licensing, the UI library, or dependencies are uncertain, stop
  and ask me instead of guessing.

Before editing, return:
A. Repository findings
B. Exact proposed files/folders
C. Dataset choice and terms, or the missing decision
D. Commands you intend to run

After approved work, run only Phase 1 validation checks. Update the Phase 1
checklist accurately. Report files changed, commands/results, data counts,
and blockers. STOP. Do not begin Phase 2.
```

---

# Phase 2 — CNN model training and evaluation

**Target:** Day 1, afternoon  
**Exit condition:** A reproducible training script, saved model, evaluation report, and known limitations.

## Phase 2 checklist
- [x] Confirm Phase 1 is complete and data paths are valid.
- [x] Define image size, batch size, epoch limit, and random seed.
- [x] Implement a small CNN using TensorFlow/Keras.
- [x] Add sensible image normalization and training-only augmentation.
- [x] Train using the training set and monitor validation metrics.
- [x] Save the best model based on validation performance.
- [x] Evaluate once on the held-out test set after model selection.
- [x] Generate accuracy/loss history and a confusion matrix or classification report.
- [x] Save model metadata: class order, image size, and preprocessing steps.
- [x] Add a small prediction helper and basic ML tests.
- [x] Record actual results and limitations; do not promise a target accuracy.

## Phase 2 master prompt

```text
ACTIVE PHASE: PHASE 2 ONLY — CNN TRAINING AND EVALUATION.

Read GEMINI.md and PROJECT_WORKFLOW.md. Verify Phase 1's dataset and checklist
before changing files. If Phase 1 is incomplete, report what is missing and
stop; do not silently repair unrelated tasks.

Goal:
Train a small, understandable CNN to classify apple, banana, and orange images.

Allowed tasks:
1. Implement ml/train.py using TensorFlow/Keras, or report a compatibility
   blocker and ask before changing frameworks.
2. Implement ml/evaluate.py and ml/predict.py if required for this phase.
3. Use the documented data directories and class order only.
4. Normalize images consistently. Apply augmentation only to training data.
5. Use a fixed seed where supported, and use validation data for model selection.
6. Save the best model and its metadata in the documented model directory.
7. Evaluate the selected model on the held-out test set once after model
   selection; report accuracy, per-class precision/recall/F1 where supported,
   and a confusion matrix.
8. Add focused tests for loading an image, preprocessing shape, class mapping,
   and prediction output shape.
9. Document exact training commands and settings.

Suggested initial settings: image size 128x128, batch size 32, up to 15 epochs,
early stopping on validation loss, and a fixed seed. Adjust only if hardware or
dataset size requires it, and document the reason. These are starting values,
not promises of performance.

Strict limits:
- Do not build the API or React UI.
- Do not add classes or change the dataset split without approval.
- Do not report fabricated or assumed accuracy.
- Do not train on validation/test data.
- Do not repeatedly tune against the test set.
- Do not add transfer learning or a different framework unless I approve it.
- Do not download unrelated datasets or large pretrained weights without asking.
- Do not begin Phase 3.

First report the files you plan to create/change and the commands you intend to
run. Then implement only the approved scope. Run the training and focused tests
if the environment supports them. If execution is blocked by missing packages,
RAM, GPU, or data, give the exact error and next decision needed.

At the end, update Phase 2 checkboxes only when verified. Report actual metrics,
model path, commands/results, and limitations. STOP.
```

---

# Phase 3 — Prediction API

**Target:** Day 2  
**Exit condition:** API loads the trained model and returns a prediction for a valid image.

## Phase 3 checklist
- [x] Confirm the saved model and metadata from Phase 2 exist.
- [x] Implement a FastAPI application that loads the model once at startup.
- [x] Add `GET /health`.
- [x] Add `POST /predict` for one uploaded image.
- [x] Validate MIME type, file extension where useful, and maximum upload size.
- [x] Handle unreadable images and model errors with clear HTTP responses.
- [x] Return predicted class and class confidence/probabilities with documented semantics.
- [x] Enable local frontend access through narrowly scoped CORS for the configured dev origin.
- [x] Add API tests for valid, invalid, and oversized uploads where practical.
- [x] Document how to run the API and confirm it works before UI integration.

## Phase 3 master prompt

```text
ACTIVE PHASE: PHASE 3 ONLY — PREDICTION API.

Read GEMINI.md and PROJECT_WORKFLOW.md. Verify that Phase 2 produced a real
model and metadata. If not, stop and report the blocker.

Goal:
Expose the trained fruit classifier through a small local FastAPI service.

Allowed tasks:
1. Create backend/main.py and backend requirements/tests only as needed.
2. Load the saved model once during application startup, not on every request.
3. Implement GET /health with a clear service/model readiness status.
4. Implement POST /predict accepting one image upload.
5. Apply exactly the preprocessing and class mapping used during training.
6. Return JSON containing predicted_class, confidence, and class probabilities
   if available. Document whether confidence is a raw softmax score and avoid
   describing it as a calibrated probability.
7. Limit upload size and reject unsupported or corrupt images safely.
8. Configure CORS only for the local React development origin needed by this app.
9. Add focused tests and API run instructions.

Strict limits:
- Do not retrain or alter the model.
- Do not create or change the frontend.
- Do not add login, database, history storage, external API calls, or deployment.
- Do not expose local filesystem paths or stack traces to clients.
- Do not accept arbitrary URLs as image input.
- Do not loosen CORS to every origin unless I explicitly approve it.
- Do not begin Phase 4.

First list exact files and commands. Then implement only the API scope.
Run tests and start the server if possible. Test /health and /predict using a
known valid image and at least one invalid image. If any test cannot run,
explain why and do not mark it complete.

Update Phase 3 checkboxes accurately. Report endpoints, commands, actual test
results, and blockers. STOP.
```

---

# Phase 4 — React UI with React Bits and Vengence UI

**Target:** Day 3, morning  
**Exit condition:** A responsive upload UI can call the API and display results/errors.

## Phase 4 checklist
- [x] Confirm the API works independently before frontend integration.
- [x] Verify the exact React Bits and Vengence UI libraries and installed APIs.
- [x] Build a single-page React interface using the approved libraries.
- [x] Include project title, concise instructions, upload/drop zone, preview, and classify action.
- [x] Show loading, success, API error, invalid file, and empty states.
- [x] Display predicted fruit and confidence clearly.
- [x] Include retry/reset and accessible labels/focus states.
- [x] Use responsive layout and consistent visual hierarchy.
- [x] Keep API base URL in a documented frontend environment variable.
- [x] Do not claim the prediction works until a real API response is received.

## Phase 4 master prompt

```text
ACTIVE PHASE: PHASE 4 ONLY — REACT USER INTERFACE.

Read GEMINI.md and PROJECT_WORKFLOW.md. Confirm Phase 3's API has passed its
independent smoke test. If it has not, stop and report the missing evidence.

Goal:
Build a polished, simple, responsive React interface for fruit image
classification using React Bits and Vengence UI, after verifying their exact
package names and component APIs.

Before coding:
1. Inspect the existing frontend and package manager.
2. Verify official documentation and the exact components/packages for React
   Bits and the library I called "Vengence UI". Do not assume spelling or APIs.
3. If the intended Vengence UI library is unclear, ask me to identify it.
4. List exact files to create/change and the UI components you intend to use.

Required UI:
- Clear title: "Fruit Image Classifier".
- Short subtitle explaining apple, banana, and orange classification.
- Drag-and-drop area plus a browse button.
- Image preview and file name.
- A "Classify Image" action disabled when no valid image is selected.
- Loading indicator while waiting for the API.
- Result panel showing predicted class and confidence from the actual API response.
- Friendly messages for invalid file type, oversized file, API unavailable, and
  server-side image errors.
- Reset/try-another-image action.
- Responsive desktop/mobile layout and accessible labels, keyboard focus, and
  sufficient contrast.

Strict limits:
- Do not fake predictions or hardcode demo results.
- Do not create a second backend or duplicate model logic in JavaScript.
- Do not add authentication, accounts, history, analytics, database, themes
  beyond what is needed, or unrelated pages.
- Do not use unverified UI packages or invent component names.
- Do not modify the model or API behavior in this phase.
- Do not begin Phase 5.

Use the API contract documented by Phase 3. Keep the API base URL configurable
through a frontend environment variable and document the local default. Do not
put secrets in frontend code.

Implement only after the plan is clear. Run the available frontend checks and
manually test the upload-to-result flow against the real API if possible.
Update Phase 4 checklist accurately, report files changed and actual results,
and STOP.
```

---

# Phase 5 — Integration, testing, and handoff

**Target:** Day 3, afternoon  
**Exit condition:** The project can be run locally using the README and has a verified end-to-end demo.

## Phase 5 checklist
- [x] Review all prior phase checklists and resolve only in-scope blockers.
- [x] Verify frontend and backend configuration match.
- [x] Run Python tests and frontend checks/build.
- [x] Start the API and frontend using documented commands.
- [x] Test one valid image for each available class where data permits.
- [x] Test invalid image, unsupported type, oversized upload, and API-offline states.
- [x] Verify the displayed result comes from the real model/API.
- [x] Finalize README with environment setup, dataset attribution, training, evaluation, and run steps.
- [x] Document model metrics, limitations, and known issues.
- [x] Confirm `.gitignore` excludes virtual environments, node_modules, local datasets if appropriate, caches, and large model artifacts where appropriate.
- [x] Review for secrets, unused files, accidental scope expansion, and fabricated claims.
- [x] Mark only verified checklist items complete and produce the final handoff report.

## Phase 5 master prompt

```text
ACTIVE PHASE: PHASE 5 ONLY — INTEGRATION, TESTS, AND HANDOFF.

Read GEMINI.md and PROJECT_WORKFLOW.md. Review the completion status of Phases
1–4. Do not assume a phase is complete merely because its checklist says so;
check available evidence. Do not rebuild the project from scratch.

Goal:
Verify that the app runs end to end, document it, and report honest results.

Allowed tasks:
1. Check frontend API URL/configuration against the backend.
2. Run existing Python tests and frontend lint/build/test commands.
3. Start backend and frontend using documented local commands where possible.
4. Test real image upload and prediction end to end.
5. Test error handling: invalid/corrupt file, unsupported type, oversized file,
   and backend unavailable.
6. Fix small, clearly scoped integration defects only. Before broad refactors or
   changes to earlier phase architecture, explain the issue and ask permission.
7. Finalize README.md with prerequisites, installation, dataset source/terms,
   training, evaluation metrics, API startup, frontend startup, testing, and
   known limitations.
8. Review .gitignore and check for secrets or accidental generated data.
9. Ensure all reported metrics and claims match actual outputs.

Strict limits:
- Do not add new features or fruit classes.
- Do not deploy or publish the app.
- Do not add Docker, a database, authentication, analytics, or paid services.
- Do not hide failing tests or warnings that materially affect the demo.
- Do not fabricate screenshots, test outputs, or performance claims.
- Do not mark any item complete unless verified.

Before making fixes, report failures and list the exact files you plan to change.
After approved fixes, rerun relevant tests. Update the checklists based on
evidence. Finish with:
A. Exact commands to install and run the project
B. Test results and model metrics
C. Files created/changed
D. Known limitations and remaining TODOs
E. A phase-by-phase checklist status

STOP after the handoff report. Do not continue adding improvements.
```

---

## 5. Overall master prompt (project controller)

Use this once to initialize the project. It must not implement all phases at once.

```text
Act as a disciplined senior ML/full-stack engineer. Build my internship project:
"Image Classifier for Fruits" using a small CNN to classify apple, banana, and
orange images, with a React frontend and a local prediction API.

The project must be completed in a three-day target schedule using the five
phases in PROJECT_WORKFLOW.md:
Phase 1 — Setup and dataset
Phase 2 — CNN training and evaluation
Phase 3 — Prediction API
Phase 4 — React UI
Phase 5 — Integration, tests, and README

FIRST ACTION ONLY:
1. Inspect the repository and all existing instructions.
2. Create or propose GEMINI.md and PROJECT_WORKFLOW.md containing this workflow
   and phase checklists.
3. Verify the exact package names and official documentation for React Bits and
   the requested "Vengence UI". If the latter is ambiguous, ask me to confirm.
4. Return a concise plan and wait for approval.

Do not implement all phases now. Do not skip ahead. In each subsequent session,
I will give you the relevant phase prompt. Execute only that phase, only its
checklist, and only approved files. If blocked, explain the blocker and ask me
what to do. Never fabricate success, metrics, data sources, or tests. At every
phase end, update only verified checkboxes, summarize evidence, and stop.
```

---

## 6. Suggested day-by-day working routine

### Day 1
- Morning: Finish Phase 1; confirm images and class counts before training.
- Afternoon: Run Phase 2 training. If training is slow, reduce epochs or dataset size only with a documented reason.

### Day 2
- Build and test the FastAPI prediction service.
- Confirm model preprocessing and class labels match the training script.

### Day 3
- Build the React UI using the verified UI libraries.
- Integrate, test error states, and finish README and demo steps.

---

## 7. Final acceptance checklist

- [ ] Three fruit classes are supported: apple, banana, orange.
- [ ] Dataset source and terms are documented.
- [ ] Train/validation/test split avoids leakage as far as practical.
- [ ] CNN training is reproducible and evaluation metrics are real.
- [ ] Saved model and preprocessing/class metadata are consistent.
- [ ] API validates uploads and returns prediction results.
- [ ] React UI sends the selected image to the real API.
- [ ] Loading, success, empty, and error states work.
- [ ] README contains copyable local setup/run/test commands.
- [ ] No unapproved features or dependencies were added.
- [ ] All unchecked items and limitations are disclosed.

**Important:** Three days is a target, not a promise. A smaller working project with honest results is preferable to a larger project with untested or fabricated functionality.
