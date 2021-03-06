# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, url_for
from log import log
import util
import os

app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.cfg'), silent=True)

@app.route('/')
def home():
    log.info('Fetching demo gist.')
    gist_id = '5123482'
    gist = util.get_gist_by_id(gist_id)
    source = util.get_slides_source_from_gist(gist)

    return render_template('index.html', gist_id=gist_id, source=source)

@app.route('/s/', methods=['GET'])
@app.route('/s/<gist_id>/', methods=['GET'])
def play_gist(gist_id=None):
    # Fix url to a restful style.
    if gist_id is None:
        if 'gist_id' in request.args:
            return redirect(url_for('play_gist', gist_id=request.args['gist_id']))
        else:
            abort(404)
    else:
        log.info('Creating slides from gist: %s' % gist_id)
        gist = util.get_gist_by_id(gist_id)
        if gist is None:
            abort(404)
        
        title = gist.get('description', 'Remarks')
        source = util.get_slides_source_from_gist(gist)
        return render_template('slideshow.html', title=title, source=source)

