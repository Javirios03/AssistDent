# AssistDent

AssistDent is a project developed to automatize processes related to the administration of a dental clinic, using NLP and RPAs.

## Authors
    - Francisco Javier Ríos
    - Fernando Ríos
    - Santiago Stolo

## Installation

First of all, install the required dependencies via python's pip package (both a supported version of Python, like 3.9>, and the pip package are a prerrequisite). After opening a command prompt in the directory where the files are located, execute the following command:

```bash
pip install -r requirements.txt
```

This may take several minutes, since certain dependencies (PyTorch, Whisper, etc.) are rather heavy, size-wise.

## Usage

We recommend to set up a virtual environment to avoid messing with the, possibly, local packages present in your device. To do so, we suggest using Python's *venv* module (https://docs.python.org/3/library/venv.html).

Once it's created (if through venv), remember to activate the environment using the correct command (depending on the OS used). For windows:

```bash
path/to/venv/Scripts/activate
```
where *path/to/venv* is the path to the environment created previously

### Demo 2

As of now, the demo has a main functionality: Command Transcription (from voice to text), which may be done either through CPU or GPU. For the first one, you may continue to the nextsection, skipping the following graph.

In order to be able to use your GPU for the NLP task, the correct package of Pytorch must be installed. First of all, after downloading the required dependencies, execute the following script:

```python
import torch
print(torch.cuda.is_available())
```

If its output is *True*, the correct package is installed and PyTorch has access to your GPU for the processing. If *False*, proceed by, in a terminal, uninstalling the package previously installed and installing a new version:

```bash
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Be sure to replace **cu118** with your CUDA Version (you may find more information at https://pytorch.org/get-started/locally/)

#### CPU Whisper

This functionality is enclosed in the Interactive Python Notebook *demo_cpu*. The first cell imports the necessary packages.

#### GPU Whisper

Idem