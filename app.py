from flask import Flask, render_template, request
import subprocess
import os
import sys

app = Flask(__name__)

SCRIPT_FOLDER = os.path.join(os.getcwd(), "Features", "Tests")

def get_script_by_number(number):
    scripts = {}
    for file in os.listdir(SCRIPT_FOLDER):
        if file.endswith(".py"):
            try:
                num = int(file.split("_")[0])
                scripts[num] = file
            except:
                continue
    return scripts.get(number, None)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        try:
            num = int(request.form["script_number"])
            script = get_script_by_number(num)
            if not script:
                message = f"No script found for number {num}."
            else:
                script_path = os.path.join(SCRIPT_FOLDER, script)
                command = [sys.executable, "-m", "pytest", script_path, "-s", "--maxfail=1"]
                result = subprocess.run(command, capture_output=True, text=True, cwd=SCRIPT_FOLDER)
                if result.returncode == 0:
                    message = f"✅ Script {script} ran successfully!\n\n{result.stdout}"
                else:
                    message = f"❌ Script {script} failed.\n\n{result.stdout}\n\n{result.stderr}"
        except Exception as e:
            message = f"⚠️ Error: {str(e)}"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
