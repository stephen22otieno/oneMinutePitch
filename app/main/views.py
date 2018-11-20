from flask import render_template,redirect,url_for,abort
from . import main
from ..models import Category, User,Peptalk, Comments
from .. import db
from flask_login import login_required, current_user
from .forms import PeptalkForm,CommentForm

# Views

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    categories = Category.get_categories()

    title = 'Home - Welcome to One Minute Pitch'
    return render_template('index.html', title = title, categories = categories)

@main.route('/category', methods = ['GET','POST'])
@login_required
def category(id):
    '''
    category route function returns a list of pitches chosen and allows users to create a new pitch
    '''

    category = Category.query.get(id)

    if category is None:
        abort(404)

    pitches = Peptalk.get_pitches(id)
    title = "Pitches"
    return render_template('category.html', title = title, category = category,pitches = pitches)

# Dynamic routing for pitches
@main.route('/pitches', methods = ['GET','POST'])
@login_required
def pitches(id):
    '''
    Function to check Pitches form
    '''
    form = pitchForm()
    pitches = pitches.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_pitch = Peptalk(content=content,user_id=current_user.id,category_id=category.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id = category.id))

    title = 'Pitches'
    return render_template('new_pitches.html', title = title, pitch_form = form)

# Dynamic routing for one pitch
@main.route('/single_pitch', methods = ['GET','POST'])
@login_required
def single_pitch(id):
    '''
    Function the returns a single pitch for comment to be added
    '''

    # pitches = Peptalk.query.get(id)

    if pitches is None:
        abort(404)

    if form.validate_on_submit():
        single_pitch= single_pitch.get_single_pitch(id)
        title = 'Comment Section'
        return render_template('pitch.html', title = title, pitches = pitches, comment = comment)



@main.route('/comment', methods = ['GET','POST'])
@login_required
def comment(id):
    '''
    Function that returns a list of comments for the particular pitch
    '''
    form = CommentForm()
    comment=comment.query.filter_by(id=id).first()

    if pitches is None:
        abort(404)

    if form.validate_on_submit():
        comment_section_id = form.comment_section_id.data
        comment = Comments(comment_section_id=comment_section_id,user_id=current_user.id,pitches_id=pitches.id)
        comment.save_comment()
        return redirect(url_for('.category', id = pitches.id))

    title = 'Comment'
    return render_template('comments.html', title = title, comment_form = form)
