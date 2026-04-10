def write_to_file(filename, text):
    try:
        with open(filename, 'w') as f: f.write(text)
        return f"File {filename} written."
    except Exception as e: return f"Error writing: {e}"
