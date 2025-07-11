from flask import Flask, render_template, request, redirect, url_for, session
import qrcode
import base64
from io import BytesIO
from urllib.parse import quote
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key_here'  # Bắt buộc cho session hoạt động

@app.route('/')
def index():
    qr_img = session.pop('qr_img', None)
    qr_url = session.pop('qr_url', None)
    return render_template('index.html', qr_img=qr_img, qr_url=qr_url)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    line1 = request.form.get('line1', '')
    line2 = request.form.get('line2', '')

    if not line1 and not line2:
        return redirect(url_for('index'))

    # ✅ Mã hóa chính xác từng dòng
    line1_encoded = quote(line1, safe='')
    line2_encoded = quote(line2, safe='')
    qr_url = f"{request.url_root}shooting?line1={line1_encoded}&line2={line2_encoded}"

    print(f"[QR URL]: {qr_url}")  # ✅ In chính xác ra console

    qr = qrcode.make(qr_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    session['qr_img'] = img_str
    session['qr_url'] = qr_url

    return redirect(url_for('index'))

@app.route('/shooting')
def shooting():
    line1 = request.args.get('line1', '')
    line2 = request.args.get('line2', '')
    return render_template('shooting.html', line1=line1, line2=line2)

if __name__ == '__main__':
   port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
