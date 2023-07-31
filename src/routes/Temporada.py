from flask import Blueprint, current_app, jsonify, render_template, redirect, url_for, request

# Models
from models.ModelTemporada import ModelTemporada

# Entities
from models.entities.Temporada import Temporada

# Utils
from utils.Format import ceil
from utils.Format import Format
from utils.Format import classes, id_class, fid_class
from utils.Format import PAGE_ELEMENTS, NUM_NAV_BUTTONS

from utils.error_handler import page_not_found, internal_server_error

main = Blueprint("temporada", __name__)

@main.route('/', methods=['GET'])
def get_temporades():

    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelTemporada.get_id() if order is None else order

    key = ModelTemporada.get_id()
    headings = ModelTemporada.get_headings()
    attributes = ModelTemporada.get_attributes()

    max_page = int(ceil(ModelTemporada.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        temporades, status = ModelTemporada.get_temporades(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = temporades,
                                titol = 'Temporades',
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
        headings = ModelTemporada.get_headings()
        attributes = ModelTemporada.get_attributes()
        return render_template('search_entity.html',
                                titol = 'Temporades',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/search/', methods=['GET', 'POST'])
def search():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelTemporada.get_id() if order is None else order

    if request.method == 'POST':        
        query['anyT'] = request.form['anyT']
        query['anyT-op'] = request.form['anyT-op']

        query['pilotCampio'] = request.form['pilotCampio']
        query['pilotCampio-op'] = request.form['pilotCampio-op']

        query['constructorCampio'] = request.form['constructorCampio']
        query['constructorCampio-op'] = request.form['constructorCampio-op']
        
        Format.parse_query(query)
        current_app.config['search'] = query

    elif request.method == 'GET':
        query = current_app.config['search']

    key = ModelTemporada.get_id()
    headings = ModelTemporada.get_headings()
    attributes = ModelTemporada.get_attributes()

    max_page = int(ceil(ModelTemporada.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        temporades, status = ModelTemporada.get_temporades(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = temporades,
                                titol = 'Temporades',
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


@main.route('/<int:anyT>', methods=['GET'])
def get_temporada(anyT):
    
    try:
        temporada, status = ModelTemporada.get_temporada(anyT)
        if temporada != None:
            headings = ModelTemporada.get_headings()
            attributes = ModelTemporada.get_attributes()
            return render_template('entity_model.html',
                                    id = anyT,
                                    data = [temporada],
                                    titol = 'Temporades',
                                    attributes = attributes,
                                    headings = headings), 200
        else:
            return page_not_found(404, 'temporada.get_temporades'), 404    

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/add', methods=['POST'])
def add_temporada():
    
    # TODO: check parameter integrity
    anyT = request.form['anyT']
    pilotCampio = request.form['pilotCampio']
    constructorCampio = request.form['constructorCampio']

    try:
        temporada = Temporada(anyT, pilotCampio, constructorCampio)
        affected_rows, status = ModelTemporada.add_temporada(temporada)

        if affected_rows > 0:
            return redirect(url_for('temporada.get_temporada', anyT = anyT)), 302
        else:
            return internal_server_error(status, 'temporada.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/afegir', methods=['GET'])
def afegir():

    try:
        headings = ModelTemporada.get_headings()
        attributes = ModelTemporada.get_attributes()
        return render_template('add_entity.html',
                                titol = 'Temporades',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/update/<int:anyT>', methods=['POST', 'PUT'])
def update_temporada(anyT):

    # TODO: check parameter integrity
    pilotCampio = request.form['pilotCampio']
    constructorCampio = request.form['constructorCampio']

    try:
        temporada = Temporada(anyT, pilotCampio, constructorCampio)
        affected_rows, status = ModelTemporada.update_temporada(temporada)

        if affected_rows > 0:
            return redirect(url_for('temporada.get_temporada', anyT = anyT)), 302
        else:
            return internal_server_error(status, 'temporada.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/actualitzar/<int:anyT>', methods=['GET'])
def actualitzar(anyT):
    
    try:
        headings = ModelTemporada.get_headings()
        attributes = ModelTemporada.get_attributes()
        temporada, status = ModelTemporada.get_temporada(anyT)
        return render_template('modify_entity.html',
                                id = anyT,
                                data = temporada,
                                titol = 'Temporades',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/delete/<int:anyT>', methods=['POST', 'DELETE'])
def delete_temporada(anyT):
    
    try:
        # TODO: check parameter integrity
        affected_rows, status = ModelTemporada.delete_temporada(anyT)

        if affected_rows > 0:
            return redirect(url_for('temporada.get_temporades')), 302
        else:
            return internal_server_error(status, "temporada.get_temporades"), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500