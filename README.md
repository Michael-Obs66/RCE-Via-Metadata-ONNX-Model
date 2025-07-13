# AI-ML-Security---Red-Teaming-Malicious-ONNX-RCE-Data-Exfiltration-via-Model-Metadata
Malicious-ONNX is a proof-of-concept (PoC) demonstrating how ONNX model files can be weaponized using metadata-based payload injection. The attack leverages the metadata_props field to embed an obfuscated Python-based script, enabling remote code execution (RCE) and data exfiltration upon model loading.

# 🧠 What is ONNX?
ONNX (Open Neural Network Exchange) is an open format built to represent machine learning models. It allows models trained in frameworks like PyTorch or TensorFlow to be exported and used in other runtimes or toolchains. ONNX is widely adopted for its flexibility and interoperability.

An ONNX model consists of:
- A computation graph (operators like Conv, Relu, Add, etc.)
- Initializers (weights)
- Metadata (e.g., author, version, description)
- Optional custom fields under metadata_props

While ONNX is designed for portability and speed, its flexible metadata fields introduce an unexpected security surface.

# 🚨 Vulnerability: Metadata-Based RCE via metadata_props
ONNX allows arbitrary metadata to be stored in key-value pairs. This flexibility, if unchecked, can be abused to smuggle executable payloads into an otherwise normal-looking model.
In this project, we demonstrate how an attacker can embed a Base64-obfuscated Python payload into the ONNX file's metadata, specifically under the "run" key.

# 💣 Attack Flow
- A simple ONNX model is created with just one Identity node.
- A malicious Python script is base64-encoded and embedded into the model’s metadata_props.
- When the model is loaded using onnx.load() and the payload is executed via exec(), the following occurs:

# 🔍 Payload Actions
- Collects host system info:
    Hostname
    Username
    OS type and version

- Reads its own ONNX file content.
- Encodes the file in Base64.
- Sends all data to a remote webhook via requests.post().
<img width="1352" height="667" alt="image" src="https://github.com/user-attachments/assets/e644d7f1-3d4e-407f-a004-cc111ee912d3" />

# 🧥 Obfuscation
The payload is wrapped in an exec(base64.b64decode(...)) structure to hide it from plain-text inspection and bypass naïve static scanners.

# 🧪 Test Execution
✅ Step-by-step:
1. Generate ONNX Model             : generate_onnx.py
2. Generate Infected Model         : generate_model.py
3. Upload via hugging face         : https://huggingface.co/Armx888/ONNX_Proc
4. Simulate Loading (Victim Side)  : test_loader.py
5. Result                          : System data + encoded model is POSTed to https://webhook.site/#!/view/78a9abba-f0e1-48d5-8d58-c47745e62317/f0e2f2b6-debb-4d42-8aaf-8295b0a7b8f1/1

# 🧨 Real-World Risk
1. Supply Chain Attack
An attacker uploads a poisoned ONNX model to a public repository like Hugging Face. Any system that downloads and loads it (e.g., for inference) becomes compromised.

2. Exfiltration of Proprietary Models
In internal environments, poisoned models could extract intellectual property or infrastructure details silently.

3. Stealth DDoS Variant
The payload could be extended to perform resource exhaustion, massive file writes, or create reverse shells — turning a model into an attack vector.

# 🔒 Mitigation Strategies
Always validate metadata fields before executing or parsing them.
Avoid using exec() on any content from model files.
Use ONNX model sanitization tools or custom validators.
Treat pre-trained model files as potentially untrusted binaries.

# 📚 References
ONNX Format Overview
ONNX Python API Docs
Model Supply Chain Threats – MITRE ATLAS
CVE-2023-36665 – ONNX Unsafe Loader

# ⚠️ Disclaimer
This project is created strictly for educational and research purposes.
The author is not responsible for any misuse.
Do not deploy or distribute infected models in real environments.

