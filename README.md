# pim-cli

`pim` is a CLI tool to declaratively install and manage machine learning models from a `Pimfile`.
## WARNING
**THIS IS VERY MUCH IN DEVELOPMENT AT THE MOMENT**

## 🚀 Why Pim?

Modern AI workflows require more than just installing Python packages — they depend on large pretrained models, often fetched from different frameworks with inconsistent interfaces and storage behaviors.

**Pim** is a lightweight, framework-agnostic CLI tool that solves this by treating models as first-class dependencies — just like packages and pip — with simple, reproducible install workflows. It has first-class Hugging Face support, but built to install from anywhere (PyTorch, OpenAI, local).

### ✅ What Pim Does
- Installs pretrained models from Hugging Face, TorchVision, and Scikit-learn
- Uses a `Pimfile` (like `Pipfile` or `requirements.txt`) to declare which models your project depends on
- Centralizes model downloads in a shared cache (`~/.pim`) or a user-defined directory
- Securely supports authentication for gated models (e.g., Hugging Face token access)
- Lets you run `pim install` from anywhere — no manual Python scripting required

### 🧠 Why It’s Different
| Feature                          | pip / conda            | pim                           |
|----------------------------------|-------------------------|-------------------------------|
| Installs Python packages         | ✅                      | ❌                            |
| Declarative install file (`Pimfile`)| ✅                     | ✅                            |
| Installs pretrained ML models    | ❌                      | ✅                            |
| Unified CLI for multiple frameworks | ❌                   | ✅                            |
| Model caching & directory control| ❌                      | ✅                            |
| Handles gated models & auth      | ❌                      | ✅                            |

Pim doesn’t replace tools like pip or conda — it **complements them** by handling the growing complexity of working with large-scale pretrained model artifacts in a clean, declarative, and scriptable way.



## Installation

```bash
pip install pim-cli
```

## 📦 `pim install` – Usage & Cache Behavior

The `pim install` command is used to install one or more AI models listed in your `Pimfile`, or provided directly via CLI.

### 🔹 Basic Usage

Install models listed in a `Pimfile`:
```bash
pim install
```

Install specific models by name (framework prefix required) or from a custom Pimfile: 
```bash
pim install hf:bert-base-uncased torch:resnet18 --file ./configs/my_Pimfile
```

### 🗃 Cache Directory Behavior
By default, Pim stores downloaded models in a cache directory. This allows models to be reused across sessions and avoids re-downloading.

Pim resolves the cache directory using the following priority:

1. `--cache-dir` CLI flag (highest priority)
2. `PIM_CACHE_DIR` environment variable
3. `~/.cache/pim` (default caching location)

### 🌱 Set a persistent custom cache directory
If you'd like to use a different default cache path for all future Pim commands, add the following to your `~/.bashrc` or `~/.zshrc`:

```` bash
export PIM_CACHE_DIR="/mnt/data/my-models"
````

### 📌 Notes
* If the specified cache directory does not exist, Pim will create it.
* Cache directories are framework-agnostic: all models will be organized under the same cache path.

## 🤖 Why Multi-Framework Model Support Matters

While Hugging Face is rapidly becoming the central registry for models in NLP, vision, and generative AI, it’s not the only ecosystem. `pim` was created with a broader goal: to make it as easy to install AI models as it is to install Python packages with `pip`.

Many foundational and open-source models live outside Hugging Face:
- 🧠 Whisper and CLIP from OpenAI are hosted on GitHub
- 🖼 TorchVision provides classic models like ResNet and MobileNet
- 🏭 Enterprises often train their own models stored as `.pt`, `.joblib`, `.onnx`, or `.pkl`
- 🎯 Future formats like ONNX or TFLite may become more common for deployment

Instead of locking users into one model hub, **`pim` supports models from multiple frameworks**, with a consistent interface for:
- Installing models and their weights
- Managing versioned lock files (`Pim.lock`)
- Keeping installation declarative via the `Pimfile`

This multi-framework philosophy ensures `pim` stays flexible, forward-compatible, and useful in both research and production workflows.

## License

MIT
