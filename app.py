from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - LTX Desktop</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f5f5; }
        nav { background: #333; padding: 1rem; }
        nav a { color: white; text-decoration: none; margin-right: 1rem; }
        nav a:hover { text-decoration: underline; }
        .container { max-width: 800px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        p { line-height: 1.6; color: #666; }
        .footer { text-align: center; padding: 1rem; color: #999; }
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
    </nav>
    <div class="container">
        {{ content | safe }}
    </div>
    <div class="footer">
        LTX Desktop - Featured on Product Hunt
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    content = """
        <h1>LTX Desktop</h1>
        <p>Welcome to LTX Desktop - A powerful desktop application for modern workflows.</p>
        <p>Featured on Product Hunt!</p>
    """
    return render_template_string(HTML_TEMPLATE, title="Home", content=content)


@app.route('/about')
def about():
    content = """
        <h1>About LTX Desktop</h1>
        <p>LTX Desktop is designed to help you work more efficiently with a sleek, modern interface.</p>
        <p>Built with cutting-edge technology, LTX Desktop offers seamless integration and lightning-fast performance.</p>
    """
    return render_template_string(HTML_TEMPLATE, title="About", content=content)


@app.route('/contact')
def contact():
    content = """
        <h1>Contact Us</h1>
        <p>We'd love to hear from you!</p>
        <p>Email: hello@ltxdesktop.com</p>
    """
    return render_template_string(HTML_TEMPLATE, title="Contact", content=content)


if __name__ == '__main__':
    app.run(debug=True)
