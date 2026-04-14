from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os, shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

app = Flask(__name__)
app.secret_key = 'folder-extractor-secret-key'

UPLOAD = "uploads"
OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.pdf")

TEXT_EXTENSIONS = ('.txt', '.py', '.html', '.css', '.js', '.json', '.md',
                   '.jsx', '.tsx', '.ts', '.xml', '.yml', '.yaml', '.csv',
                   '.env', '.cfg', '.ini', '.sh', '.bat', '.sql', '.java',
                   '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.go', '.rs',
                   '.swift', '.kt', '.r', '.log', '.conf', '.toml')

def is_text(file):
    return file.lower().endswith(TEXT_EXTENSIONS)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("files")

    if not files or all(f.filename == '' for f in files):
        flash("No files selected. Please choose a folder.", "error")
        return redirect(url_for('home'))

    # Clean up and prepare directories
    shutil.rmtree(UPLOAD, ignore_errors=True)
    os.makedirs(UPLOAD, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save uploaded files
    for f in files:
        if f.filename == '':
            continue
        path = os.path.join(UPLOAD, f.filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f.save(path)

    # Build PDF
    styles = getSampleStyleSheet()
    story = []

    for root, _, filenames in os.walk(UPLOAD):
        for fname in sorted(filenames):
            if not is_text(fname):
                continue

            path = os.path.join(root, fname)
            rel_path = os.path.relpath(path, UPLOAD)

            try:
                with open(path, "r", errors="ignore") as file:
                    content = file.read()
                    # Escape HTML special characters for safe rendering
                    content = content.replace("&", "&amp;")
                    content = content.replace("<", "&lt;")
                    content = content.replace(">", "&gt;")
                    content = content.replace("\n", "<br/>")

                    story.append(Paragraph(f"<b>📄 {rel_path}</b>", styles['Heading3']))
                    story.append(Spacer(1, 10))
                    story.append(Paragraph(f"<font size=8>{content}</font>", styles['Normal']))
                    story.append(Spacer(1, 20))
            except Exception:
                continue

    if not story:
        flash("No readable text files found in the selected folder.", "error")
        return redirect(url_for('home'))

    try:
        doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4)
        doc.build(story)
    except Exception as e:
        flash(f"Error generating PDF: {str(e)}", "error")
        return redirect(url_for('home'))

    return send_file(OUTPUT_FILE, as_attachment=True, download_name="extracted_content.pdf")

if __name__ == "__main__":
    app.run(debug=True)