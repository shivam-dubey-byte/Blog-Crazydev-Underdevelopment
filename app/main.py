from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',message='Welcome')
@app.route("/gallery")
def _gallery_():
    return render_template('pages/gallery.html')
@app.route("/full-width")
def _full_width_():
    return render_template('pages/full-width.html')
@app.route("/sidebar-left")
def _sidebar_left_():
    return render_template('pages/sidebar-left.html')
@app.route("/sidebar-right")
def _sidebar_right_():
    return render_template('pages/sidebar-right.html')
@app.route("/basic-grid")
def _basic_grid_():
    return render_template('pages/basic-grid.html')
@app.route("/font-icons")
def _font_icons_():
    return render_template('pages/font-icons.html',form_submit='/sign-up')

