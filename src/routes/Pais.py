from flask import Blueprint, current_app, jsonify, render_template, request, redirect, url_for

# Models
from models.ModelPais import ModelPais

# Entities
from models.entities.Pais import Pais

# Utils
from utils.Format import ceil
from utils.Format import Format
from utils.Format import classes, id_class, fid_class
from utils.Format import PAGE_ELEMENTS, NUM_NAV_BUTTONS

from utils.error_handler import page_not_found, internal_server_error

main = Blueprint("pais", __name__)

@main.route('/', methods=['GET'])
def get_paissos():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelPais.get_id() if order is None else order
            
    key = ModelPais.get_id()
    headings = ModelPais.get_headings()
    attributes = ModelPais.get_atributtes()

    max_page = int(ceil(ModelPais.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1
    
    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        paissos, status = ModelPais.get_paissos(num_page, order, query)
        return render_template('base_model.html',
                                id = key, 
                                data = paissos,
                                titol = 'Paissos',
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
        headings = ModelPais.get_headings()
        attributes = ModelPais.get_atributtes()
        return render_template('search_entity.html',
                                titol = 'Paissos',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/search/', methods=['GET', 'POST'])
def search():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelPais.get_id() if order is None else order

    if request.method == 'POST':        
        query['codi'] = request.form['codi']
        query['codi-op'] = request.form['codi-op']

        query['nom'] = request.form['nom']
        query['nom-op'] = request.form['nom-op']
        
        Format.parse_query(query)
        current_app.config['search'] = query

    elif request.method == 'GET':
        query = current_app.config['search']

    key = ModelPais.get_id()
    headings = ModelPais.get_headings()
    attributes = ModelPais.get_atributtes()

    max_page = int(ceil(ModelPais.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        paissos, status = ModelPais.get_paissos(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = paissos,
                                titol = 'Paissos',
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
    

@main.route('/<codi>', methods=['GET'])
def get_pais(codi):

    try:
        pais, status = ModelPais.get_pais(codi)
        if pais != None:
            headings = ModelPais.get_headings()
            attributes = ModelPais.get_atributtes()
            return render_template('entity_model.html',
                                    id = codi,
                                    data = [pais],
                                    titol = 'Paissos',
                                    attributes = attributes,
                                    headings = headings)
        else:
            return page_not_found(404, 'pais.get_paissos'), 404    

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_pais():
    
    # TODO: check parameter integrity
    codi = request.form['codi']
    nom = request.form['nom']

    try:
        pais = Pais(codi, nom)
        affected_rows, status = ModelPais.add_pais(pais)

        if affected_rows > 0:
            return redirect(url_for('pais.get_pais', codi = codi)), 302
        else:
            return internal_server_error(status, 'pais.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/afegir', methods=['GET'])
def afegir():
    
    try:
        headings = ModelPais.get_headings()
        attributes = ModelPais.get_atributtes()
        return render_template('add_entity.html',
                                titol = 'Paissos',
                                attributes = attributes,
                                headings = headings), 200
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/update/<codi>', methods=['POST', 'PUT'])
def update_pais(codi):

    # TODO: check parameter integrity
    nom = request.form['nom']

    try:
        pais = Pais(codi, nom)
        affected_rows, status = ModelPais.update_pais(pais)

        if affected_rows > 0:
            return redirect(url_for('pais.get_pais', codi = codi)), 302
        else:
            return jsonify({'message': 'error on update'}), 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/actualitzar/<codi>', methods=['GET'])
def actualitzar(codi):
    
    try:
        headings = ModelPais.get_headings()
        attributes = ModelPais.get_atributtes()
        pais, status = ModelPais.get_pais(codi)
        return render_template('modify_entity.html',
                                id = codi,
                                data = pais,
                                titol = 'Paissos',
                                attributes = attributes,
                                headings = headings), 200
    except Exception as ex:
        return jsonify({'message' : str(ex)}), 500
    

@main.route('/delete/<codi>', methods=['POST', 'DELETE'])
def delete_pais(codi):
    
    try:
        # TODO: check parameter integrity
        affected_rows, status = ModelPais.delete_pais(codi)

        if affected_rows > 0:
            return redirect(url_for('pais.get_paissos')), 302
        else:
            return internal_server_error(status, "pais.get_paissos"), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
