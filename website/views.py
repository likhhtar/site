from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import vk

APIVersion = 5.73

def get_name(vk_api, id):
    profiles = vk_api.users.get(user_ids=id, fields='first_name, last_name', v=APIVersion)
    return profiles[0]['first_name'] + ' ' + profiles[0]['last_name']

views = Blueprint('views', __name__)
session = vk.Session(access_token='f63e74dd9a1d05dbf59707d202a6f98480b9cc1e1edca4da023b697723bf632a55357e4cec505547f458f')
vk_api = vk.API(session)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Слишком короткое имя.', category='error')
        else:
            new_note = Note(data=note, date=get_name(vk_api, note), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Ученик добавлен!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})