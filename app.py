from flask import Flask, request, redirect, render_template
import random
import string

app = Flask(__name__, template_folder='.', static_url_path='', static_folder='.')

# stores all urls, resets when server restarts
# TODO: maybe add sqlite later
urls = {}

def generate_code():
    # 6 chars is enough, who cares
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    original = request.form.get('url', '').strip()

    # validation - keep it simple
    if not original:
        return 'bruh, enter a url', 400

    if not original.startswith('http://') and not original.startswith('https://'):
        return 'url needs http:// or https://', 400

    code = generate_code()
    while code in urls:
        code = generate_code()

    urls[code] = original
    short = request.host_url + code

    return render_template('result.html', short=short, original=original)


@app.route('/<code>')
def go(code):
    if code not in urls:
        return 'not found', 404

    # this is the whole point
    return redirect(urls[code], 302)


# run it
if __name__ == '__main__':
    app.run(debug=True, port=5000)
