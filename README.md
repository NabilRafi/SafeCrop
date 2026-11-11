# SafeCrop: CLIP fine-tuning kit

Everything you need to fine-tune CLIP for SafeCrop in VS Code, with Claude Code as your assistant.
`CLAUDE.md` tells Claude Code the whole project story, the rules and the plan, so you can just ask it things.

## What you got

| File | What's inside | Size |
| --- | --- | --- |
| `safecrop-clip-finetune.zip` | this folder: code, CLAUDE.md, docs, data tables, saved CLIP features, earlier notebooks | ~5 MB |
| `safecrop_test_images_840.zip` | the 840 test images + the 240 PlantVillage extras | ~80 MB |

## 1. Put the files in place (2 minutes)

**Cloned from GitHub?** Skip this step: the repo already has the code, docs, all results (`results/`), the 840 test
images, the PlantVillage extras and the black gram images. Only `data/images_recipe_b/` is left out; rebuild it with
`python scripts/make_recipe_b.py` when you need recipe B. Start at step 2.

1. Unzip `safecrop-clip-finetune.zip` somewhere easy, for example `Documents/CSE299/`.
2. Unzip `safecrop_test_images_840.zip` **into `safecrop-clip-finetune/data/`**.
   You should now have `data/images/L0`, `L1`, `L2`, `L3` and `data/extra_references/`.

## 2. Install the tools (once)

- **Python 3.12** from [python.org](https://www.python.org/downloads/) (3.10 to 3.13 also work).
  Check in a terminal: `python3 --version` (Mac) or `py --version` (Windows).
- **VS Code** with these extensions: *Python*, *Jupyter*, *Claude Code*, and (optional, for a free GPU)
  *Colab* by Google. When you open the folder, VS Code offers to install the recommended ones: say yes.

## 3. Open the folder and create the Python environment (5-10 minutes)

In VS Code: **File > Open Folder** > `safecrop-clip-finetune`. Then **Terminal > New Terminal** and run:

**Mac**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
On Windows with an NVIDIA graphics card, first install PyTorch with GPU support using the command shown at
[pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/) (Stable, Windows, Pip, CUDA),
then run the last line. (On a Mac the normal install already uses the Apple GPU.)

Then press **Cmd+Shift+P** (Mac) / **Ctrl+Shift+P** (Windows) > **Python: Select Interpreter** > pick `.venv`.
New terminals will now use it automatically (you see `(.venv)` at the start of the line).

## 4. Check that everything works (1 minute)

```bash
python scripts/check_setup.py
```
You should see only `OK` lines, including `CLIP database: 840/840 predictions identical ... L3 40.0`.
That means the data, the noise recipe and the scoring code all match the Step 2 results.

Then, once:
```bash
python scripts/check_setup.py --load-model   # downloads CLIP ViT-L/14 (~1.7 GB, only the first time)
python scripts/smoke_test.py                 # runs every script with a tiny model (~2 minutes)
```

## 5. Start Claude Code

Open the Claude Code panel in VS Code (or type `claude` in the terminal inside this folder).
It reads `CLAUDE.md` by itself. A good first message:

> Read CLAUDE.md and docs/FINETUNING_PLAN.md. Then tell me in a few simple lines what we run first and why.

Ask it to explain anything you don't follow; CLAUDE.md asks it to keep explanations short and plain.

## 6. The experiments

| Step | Command | Where to run |
| --- | --- | --- |
| E0 frozen baseline | `python scripts/reproduce_baseline.py` | your laptop (~2-10 min) |
| E1 noisy copies in the database | `python scripts/noisy_database.py` | laptop (Mac ~10 min) or Colab |
| E2 SVM / linear probe | `python scripts/linear_probe.py --set linear_probe.classifier=svm --tag svm` | laptop |
| E3 fine-tuning, one fold | `python scripts/finetune.py --set finetune.folds=[0] --tag try1` | GPU (Colab T4: ~5 min) |
| E3 fine-tuning, all 840 images | `python scripts/finetune.py --tag full` | GPU (Colab T4: ~20 min) |

Each run makes a folder in `results/` with `summary.md` (the tables for the slides), the predictions and
the settings used. `results/runs.csv` keeps one line per run. Change any setting for one run with
`--set name=value` (all names are in `configs/default.yaml`).

## 7. Free GPU: Colab from VS Code (or the browser)

1. On your computer: `python scripts/pack_for_colab.py` makes `dist/safecrop_code.zip`.
2. Upload `dist/safecrop_code.zip` and (once) `dist/safecrop_test_images_840.zip` into your Google Drive
   folder (now https://drive.google.com/drive/folders/1EB43yD0e2c-kHmsbk46l89na6bvFMeMB). The notebook finds
   the folder by its ID: `DRIVE_FOLDER_ID` in the settings cell, the part after `/folders/` in the link.
3. Open `notebooks/colab_gpu_runner.ipynb`:
   - in VS Code: **Select Kernel > Colab > New Colab Server > GPU (T4)** (sign in with Google the first time);
   - or upload it to [colab.research.google.com](https://colab.research.google.com) and pick **Runtime > Change runtime type > T4 GPU**.
4. Edit the `COMMANDS` list in the settings cell, then run all cells. When Colab asks, sign in with the
   Google account that can open the folder and click **Allow**. The results come back to the same Drive
   folder as `results_<date>.zip`. Download it into the `safecrop-clip-finetune` folder and unzip it there
   (it already contains a `results/` folder), or ask Claude Code to, so the new runs can be read.

When you change the code, run step 1 again and replace the zip in Drive.
Free Colab GPUs have daily limits; if you are cut off, save what finished (the notebook writes files as it goes).

## 8. If something goes wrong

| Problem | Fix |
| --- | --- |
| `test images missing` | the images zip must be unzipped inside `data/` (you need `data/images/L0/...`) |
| out of memory (GPU) | add `--set finetune.batch_photos=8` or `--set finetune.grad_checkpointing=true` |
| an error mentioning `mps` on a Mac | add `--set device=cpu` (slow), or use Colab |
| errors about workers / multiprocessing | add `--set finetune.num_workers=0` |
| the model download stops | run the command again; finished parts are kept in `~/.cache/huggingface` |
| VS Code doesn't use `.venv` | Cmd/Ctrl+Shift+P > Python: Select Interpreter > `.venv` |

## Folder map

```
CLAUDE.md          what Claude Code reads first
configs/           settings (default.yaml, smoke.yaml, vitb16_fast.yaml)
src/safecrop/      the code (noise recipe, data, CLIP, scoring, training)
scripts/           the commands above
notebooks/         Colab GPU runner + the earlier Colab notebooks (previous/)
data/              test-set tables, saved features, baselines (+ images after unzipping)
docs/              project history, fine-tuning plan, data card, original project notes
results/           your runs
```
