#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, jsonify, current_app, request
from app.models.building import BuildingModel
from . import main
from app import db

@main.route('/', methods=['GET', 'POST'])
def index():
    # db.create_all()
    # db.session.commit()
    return render_template('main/index.html')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return jsonify("RadhaKrishna")


@main.route('/manage/apps/new', methods=['GET', 'POST'])
def create_app():
    form = CreateAppForm(csrf_enabled=False)
    if form.validate_on_submit():
        application = App(
            application_name=form.application_name.data,
            application_description=form.application_description.data,
            application_website=form.application_website.data,
            callback=form.callback.data,
            user_id = session['auth_data']['personID'])
        db.session.add(application)
        db.session.flush()

        item = Client(
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=' '.join([
                'http://localhost:8000/authorized',
                'http://127.0.0.1:8000/authorized',
                'http://127.0.1:8000/authorized',
                'http://127.1:8000/authorized',
                ]),
            _default_scopes='building buildings',
            user_id = session['auth_data']['personID'],
            app_id=application.application_id
        )
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('main.update_app', application_id=application.application_id))
    return render_template('account/create_app.html', user=current_user, form=form)


@main.route('/manage/apps/<int:application_id>', methods=['GET', 'POST'])
def update_app(application_id):
    current_app.logger.info("RadhaKrishnaHanuman")
    current_app.logger.info(application_id)
    app = App.query.filter_by(application_id=application_id).first()
    client = Client.query.filter_by(app_id=application_id).first()
    client_id = client.client_id
    client_secret = client.client_secret
    form_dict = {}
    form_dict['application_name'] = app.application_name
    form_dict['application_description'] = app.application_description
    form_dict['application_website'] = app.application_website
    form_dict['callback'] = app.callback
    form = UpdateAppForm(**form_dict)
    if form.validate_on_submit():
        app.application_name=form.application_name.data
        app.application_description=form.application_description.data
        app.application_website=form.application_website.data
        app.callback=form.callback.data
        db.session.commit()

        return redirect(url_for('main.all_apps'))
    return render_template('account/update_app.html', user=current_user, form=form, app_name=form_dict['application_name'], client_id=client_id, client_secret=client_secret, app_id=application_id)


@main.route('/manage/apps', methods=['GET', 'POST'])
def all_apps():
    current_app.logger.info("RadhaKrishnaHanuman")
    apps_list = App.query.filter_by(user_id = session['auth_data']['personID']).all()
    current_app.logger.info(apps_list)
    return render_template('account/all_apps.html', user=current_user, apps_list=apps_list)


@main.route('/manage/apps/<int:application_id>/delete', methods=['GET', 'POST'])
def delete_app(application_id):
    current_app.logger.info("RadhaKrishnaHanuman")
    client = Client.query.filter_by(app_id=application_id).first()
    Token.query.filter_by(client_id=client.client_id).delete()
    Client.query.filter_by(app_id=application_id).delete()
    App.query.filter_by(application_id=application_id).delete()
    db.session.commit()
    return redirect(url_for('main.all_apps'))
