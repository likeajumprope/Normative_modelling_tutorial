# Install PCNtoolkit for the normative modelling tutorial

## Quick summary — what do I need to do?

You will run the tutorial notebook in **VS Code**, using a separate Python environment containing PCNtoolkit and the other tutorial packages.

1. **Already have VS Code?** Skip installing it in Step 1.
2. **Already have Microsoft's Python and Jupyter extensions?** Skip installing those too.
3. Open the tutorial folder in VS Code (Step 2).
4. Create a Python environment (Step 3). Choose **Conda** if you already use Anaconda or Miniconda; choose **venv** if you already have Python 3.12. If you have neither, the Conda route includes installing Miniconda.
5. Install the packages into that environment (Step 4).
6. Select that environment as the notebook's **kernel**, then run the installation check (Steps 5–6).

**Already set up an environment for this tutorial?** Skip creating it again. Activate it, check the packages, and select it as your notebook kernel. These instructions use Python **3.12** and PCNtoolkit **1.x**.

You need an internet connection to download the software and packages. Run each command one line at a time, pressing **Enter** after each line and waiting for it to finish. Copy only the text inside the command boxes.

## 1. Check VS Code and its extensions

Skip any installation below that you have already completed.

1. Download and install [Visual Studio Code](https://code.visualstudio.com/) for your computer, then open it.
2. Click **Extensions** in the left sidebar (the icon looks like small squares).
3. Search for **Python**. Select the extension published by **Microsoft** (`ms-python.python`) and click **Install**. If it is already installed, make sure it is enabled.
4. Search for **Jupyter** and install the extension published by **Microsoft** (`ms-toolsai.jupyter`) in the same way.

The Python extension helps VS Code use Python. The Jupyter extension lets it open and run notebook files ending in `.ipynb`.

## 2. Open the tutorial folder and a terminal

1. In VS Code, choose **File → Open Folder**.
2. Select the folder containing `normative_modelling_tutorial.ipynb`.
3. Choose **Terminal → New Terminal** from the menu. A panel opens near the bottom of the window.

The **terminal** is where you type the installation commands in Steps 3–4. A **notebook code cell** is where you run the Python check in Step 6. They are different places.

## 3. Create a Python environment

An environment is a separate home for Python and its packages. It helps keep this tutorial's packages separate from those used by other projects.

**Choose either A or B below. You only need one.**

### A. Use Conda (Anaconda or Miniconda)

If you already have Anaconda or Miniconda, you already have Conda. Otherwise, follow the [Miniconda installation instructions](https://www.anaconda.com/docs/getting-started/miniconda/main) for your operating system. After installing, close and reopen VS Code, then open a new terminal.

Check that Conda is available:

```bash
conda --version
```

You should see a version number. If you see “command not found” or “not recognized”, see Troubleshooting below.

Create an environment called `normative`:

```bash
conda create --name normative python=3.12 pip
```

If prompted with `Proceed ([y]/n)?`, type `y` and press Enter. Wait for the installation to finish, then activate the environment:

```bash
conda activate normative
```

Activation makes terminal commands use this environment. You will usually see `(normative)` at the start of the terminal prompt.

If you already created this environment for the tutorial, just run the activation command. **Continue to Step 4.**

### B. Use Python's built-in virtual environment (`venv`)

This route needs Python 3.12 installed on your computer. Check using the command for your operating system below. If Python 3.12 is missing, you can use the Conda route above to install it in an environment, or install Python 3.12 from [Python's downloads](https://www.python.org/downloads/).

**macOS / Linux — run in the VS Code terminal:**

```bash
python3.12 --version
```

It should report `Python 3.12.x`. Create the environment, then activate it:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

**Windows — run in a VS Code PowerShell terminal:**

```powershell
py -3.12 --version
```

It should report `Python 3.12.x`. Create the environment, then activate it:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

These commands create a folder named `.venv` inside your tutorial folder. After activation, you will usually see `(.venv)` at the start of the terminal prompt. If you already created this environment, only run the activation command.

If Windows blocks the activation script, see Troubleshooting below. **Continue to Step 4.**

## 4. Install PCNtoolkit and the tutorial packages

In the **same terminal**, with your environment activated, run:

```bash
python --version
```

Check that it says Python 3.12.x (or 3.11.x for an existing compatible environment). PCNtoolkit 1.3.0 supports Python 3.11 and 3.12; see its [package requirements](https://pypi.org/project/pcntoolkit/).

Then run these commands, waiting for each to finish:

```bash
python -m pip install "pcntoolkit>=1.3" ipykernel
```

Installation may take several minutes. When it finishes, the terminal prompt returns. “Requirement already satisfied” means a package is already installed and is fine.

`pip` downloads and installs Python packages. Using `python -m pip` makes it install into the Python environment you activated. `ipykernel` allows VS Code's Jupyter extension to run notebook cells in that environment.

## 5. Tell the notebook which environment to use

Installing packages is only part of setup: the notebook must also use the environment containing them. The **kernel** is the Python process that runs your notebook cells.

1. Open the Command Palette: **Cmd+Shift+P** on macOS, or **Ctrl+Shift+P** on Windows/Linux.
2. Type **Python: Select Interpreter**, select that command, and choose `normative` for Conda or `.venv` for venv.
3. Click `normative_modelling_tutorial.ipynb` in the file list to open it.
4. At the top right of the notebook, click **Select Kernel**. If a kernel name is already displayed, click that name instead.
5. If shown, choose **Select Another Kernel → Python Environments**.
6. Select the same `normative` or `.venv` environment.

**Do not skip the notebook kernel selection**, even if you selected a Python interpreter in Step 2. An open notebook may still be using a different environment. See [VS Code's kernel guide](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management).

## 6. Check that everything works

In the notebook, click **+ Code** to add a code cell. Paste the following into that cell, then click the triangle beside it or press **Shift+Enter**:

```python
import sys
from importlib.metadata import version
import numpy, scipy, pandas, matplotlib, sklearn
from pcntoolkit import BLR, BsplineBasisFunction, NormData, NormativeModel

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("PCNtoolkit version:", version("pcntoolkit"))
```

Setup worked if:

- The cell finishes without an error.
- The Python executable path contains `normative` or `.venv`, matching your environment.
- Python reports version 3.12 (or 3.11), and PCNtoolkit reports a 1.x version.

You can now run the tutorial cells in order from the top. You can delete the temporary check cell after it succeeds.

## When you return to the tutorial

Open the same folder and notebook in VS Code, and check the selected kernel. You do **not** need to reinstall the packages or recreate the environment each time.

If you want to install more packages from a new terminal, activate the environment again first:

| Environment | Activation command |
|---|---|
| Conda | `conda activate normative` |
| venv on macOS/Linux | `source .venv/bin/activate` |
| venv on Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |

For venv, run the command from the tutorial folder containing `.venv`.

## Troubleshooting

**“conda: command not found” or “conda is not recognized”**

Close and reopen VS Code after installing Miniconda. On Windows, open **Miniconda Prompt** or **Anaconda Prompt** from the Start menu and run the Conda and package installation commands there. Then return to VS Code for kernel selection.

**Conda says to run `conda init` before activation**

Run the command for the shell you are using: `conda init zsh` for the default macOS shell, `conda init bash` for Bash, or `conda init powershell` for Windows PowerShell. Close that terminal, open a new one, and retry `conda activate normative`.

**Windows says running scripts is disabled**

In VS Code's terminal panel, use the dropdown beside the **+** button to open a **Command Prompt** terminal. From the tutorial folder, activate the existing venv with:

```bat
.venv\Scripts\activate.bat
```

Continue with Step 4 in that Command Prompt terminal.

**Python 3.12 cannot be found, or Linux reports that `venv` / `ensurepip` is missing**

Use the Conda route, which creates an environment with the requested Python version. If you prefer venv on Linux, install your distribution's Python 3.12 and corresponding venv support first.

**The environment does not appear in Select Kernel**

Check that Step 4 completed successfully, including installing `ipykernel`. Open the Command Palette, run **Developer: Reload Window**, then try selecting the kernel again.

**`ModuleNotFoundError: No module named 'pcntoolkit'`**

The notebook may be using a different environment from the terminal. Repeat Step 5 and check `sys.executable` using the check cell. If the environment is correct, activate it in a terminal and repeat Step 4. Restart the notebook kernel afterward.

**Packages were installed or updated, but the notebook still gives an import error**

Click **Restart Kernel** in the notebook toolbar (it may be under the **…** menu), then rerun the check cell. Restarting clears Python's memory, so rerun the tutorial from the top afterward.
