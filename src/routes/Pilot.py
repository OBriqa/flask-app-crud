from flask import Blueprint, current_app, jsonify, render_template, redirect, url_for, request

# Models
from models.ModelPilot import ModelPilot

# Entities
from models.entities.Pilot import Pilot

# Utils
from utils.Format import ceil
from utils.Format import Format
from utils.Format import classes, id_class, fid_class
from utils.Format import PAGE_ELEMENTS, NUM_NAV_BUTTONS

from utils.error_handler import page_not_found, internal_server_error

main = Blueprint("pilot", __name__)

@main.route('/', methods=['GET'])
def get_pilots():

    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelPilot.get_id() if order is None else order

    key = ModelPilot.get_id()
    headings = ModelPilot.get_headings()
    attributes = ModelPilot.get_attributes()

    max_page = int(ceil(ModelPilot.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        pilots, status = ModelPilot.get_pilots(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = pilots,
                                titol = 'Pilots',
                                attributes = attributes,
                                max_page = max_page,
                                num_page = num_page,
                                classes = classes,
                                id_class = id_class,
                                fid_class = fid_class,
                                current_url = request.url,
                                num_nav_buttons = NUM_NAV_BUTTONS,
                                headings = headings), 200
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/cercar', methods=['GET'])
def cercar():
    try:
        headings = ModelPilot.get_headings()
        attributes = ModelPilot.get_attributes()
        return render_template('search_entity.html',
                                titol = 'Pilots',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/search/', methods=['GET', 'POST'])
def search():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelPilot.get_id() if order is None else order

    if request.method == 'POST':        
        query['nomP'] = request.form['nomP']
        query['nomP-op'] = request.form['nomP-op']

        query['dataN'] = request.form['dataN']
        query['dataN-op'] = request.form['dataN-op']

        query['nacionalitat'] = request.form['nacionalitat']
        query['nacionalitat-op'] = request.form['nacionalitat-op']
        
        Format.parse_query(query)
        current_app.config['search'] = query

    elif request.method == 'GET':
        query = current_app.config['search']

    key = ModelPilot.get_id()
    headings = ModelPilot.get_headings()
    attributes = ModelPilot.get_attributes()

    max_page = int(ceil(ModelPilot.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        pilots, status = ModelPilot.get_pilots(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = pilots,
                                titol = 'Pilots',
                                attributes = attributes,
                                max_page = max_page,
                                num_page = num_page,
                                classes = classes,
                                id_class = id_class,
                                fid_class = fid_class,
                                current_url = request.url,
                                num_nav_buttons = NUM_NAV_BUTTONS,
                                headings = headings), 200
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<nomP>', methods=['GET'])
def get_pilot(nomP):
    
    try:
        pilot, status = ModelPilot.get_pilot(nomP)
        if pilot != None:
            headings = ModelPilot.get_headings()
            attributes = ModelPilot.get_attributes()
            return render_template('entity_model.html',
                                    id = nomP,
                                    data = [pilot],
                                    titol = 'Pilots',
                                    attributes = attributes,
                                    headings = headings), 200
        else:
            return page_not_found(404, 'pilot.get_pilots'), 404    

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/add', methods=['POST'])
def add_pilot():
    
    # TODO: check parameter integrity
    nomP = request.form['nomP']
    dataN = request.form['dataN']
    nacionalitat = request.form['nacionalitat']

    try:
        pilot = Pilot(nomP, dataN, nacionalitat)
        affected_rows, status = ModelPilot.add_pilot(pilot)

        if affected_rows > 0:
            return redirect(url_for('pilot.get_pilot', nomP = nomP)), 302
        else:
            return internal_server_error(status, 'pilot.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/afegir', methods=['GET'])
def afegir():

    try:
        headings = ModelPilot.get_headings()
        attributes = ModelPilot.get_attributes()
        return render_template('add_entity.html',
                                titol = 'Pilots',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<nomP>', methods=['POST', 'PUT'])
def update_pilot(nomP):

    # TODO: check parameter integrity
    dataN = request.form['dataN']
    nacionalitat = request.form['nacionalitat']

    try:
        pilot = Pilot(nomP, dataN, nacionalitat)
        affected_rows, status = ModelPilot.update_pilot(pilot)

        if affected_rows > 0:
            return redirect(url_for('pilot.get_pilot', nomP = nomP)), 302
        else:
            return internal_server_error(status, 'pilot.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/actualitzar/<nomP>', methods=['GET'])
def actualitzar(nomP):
    
    try:
        headings = ModelPilot.get_headings()
        attributes = ModelPilot.get_attributes()
        pilot, status = ModelPilot.get_pilot(nomP)
        return render_template('modify_entity.html',
                                id = nomP,
                                data = pilot,
                                titol = 'Pilots',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/delete/<nomP>', methods=['POST', 'DELETE'])
def delete_pilot(nomP):
    
    try:
        # TODO: check parameter integrity
        affected_rows, status = ModelPilot.delete_pilot(nomP)

        if affected_rows > 0:
            return redirect(url_for('pilot.get_pilots')), 302
        else:
            return internal_server_error(status, "pilot.get_pilots"), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500