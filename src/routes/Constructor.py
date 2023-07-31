from flask import Blueprint, current_app, jsonify, render_template, request, redirect, url_for

# Models
from models.ModelConstructor import ModelConstructor

# Entities
from models.entities.Constructor import Constructor

# Utils
from utils.Format import ceil
from utils.Format import Format
from utils.Format import classes, id_class, fid_class
from utils.Format import PAGE_ELEMENTS, NUM_NAV_BUTTONS

from utils.error_handler import page_not_found, internal_server_error

main = Blueprint("constructor", __name__)

@main.route('/', methods=['GET'])
def get_constructors():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelConstructor.get_id() if order is None else order
            
    key = ModelConstructor.get_id()
    headings = ModelConstructor.get_headings()
    attributes = ModelConstructor.get_atributtes()

    max_page = int(ceil(ModelConstructor.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1
    
    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        constructors, status = ModelConstructor.get_constructors(num_page, order, query)
        return render_template('base_model.html',
                                id = key, 
                                data = constructors,
                                titol = 'Constructors',
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
        headings = ModelConstructor.get_headings()
        attributes = ModelConstructor.get_atributtes()
        return render_template('search_entity.html',
                                titol = 'Constructors',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/search/', methods=['GET', 'POST'])
def search():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelConstructor.get_id() if order is None else order

    if request.method == 'POST':        
        query['nomC'] = request.form['nomC']
        query['nomC-op'] = request.form['nomC-op']

        query['seu'] = request.form['seu']
        query['seu-op'] = request.form['seu-op']
        
        Format.parse_query(query)
        current_app.config['search'] = query

    elif request.method == 'GET':
        query = current_app.config['search']

    key = ModelConstructor.get_id()
    headings = ModelConstructor.get_headings()
    attributes = ModelConstructor.get_atributtes()

    max_page = int(ceil(ModelConstructor.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        constructors, status = ModelConstructor.get_constructors(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = constructors,
                                titol = 'Constructors',
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


@main.route('/<nomC>', methods=['GET'])
def get_constructor(nomC):

    try:
        constructor, status = ModelConstructor.get_constructor(nomC)
        if constructor != None:
            headings = ModelConstructor.get_headings()
            attributes = ModelConstructor.get_atributtes()
            return render_template('entity_model.html',
                                    id = nomC,
                                    data = [constructor],
                                    titol = 'Constructors',
                                    attributes = attributes,
                                    headings = headings)
        else:
            return page_not_found(404, 'constructor.get_constructors'), 404    

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_constructor():
    
    # TODO: check parameter integrity
    nomC = request.form['nomC']
    seu = request.form['seu']

    try:
        constructor = Constructor(nomC, seu)
        affected_rows, status = ModelConstructor.add_constructor(constructor)

        if affected_rows > 0:
            return redirect(url_for('constructor.get_constructor', nomC = nomC)), 302
        else:
            return internal_server_error(status, 'constructor.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/afegir', methods=['GET'])
def afegir():
    
    try:
        headings = ModelConstructor.get_headings()
        attributes = ModelConstructor.get_atributtes()
        return render_template('add_entity.html',
                                titol = 'Constructors',
                                attributes = attributes,
                                headings = headings), 200
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/update/<nomC>', methods=['POST', 'PUT'])
def update_constructor(nomC):

    # TODO: check parameter integrity
    seu = request.form['seu']

    try:
        constructor = Constructor(nomC, seu)
        affected_rows, status = ModelConstructor.update_constructor(constructor)

        if affected_rows > 0:
            return redirect(url_for('constructor.get_constructor', nomC = nomC)), 302
        else:
            return jsonify({'message': 'error on update'}), 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/actualitzar/<nomC>', methods=['GET'])
def actualitzar(nomC):
    
    try:
        headings = ModelConstructor.get_headings()
        attributes = ModelConstructor.get_atributtes()
        constructor, status = ModelConstructor.get_constructor(nomC)
        return render_template('modify_entity.html',
                                id = nomC,
                                data = constructor,
                                titol = 'Constructors',
                                attributes = attributes,
                                headings = headings), 200
    except Exception as ex:
        return jsonify({'message' : str(ex)}), 500
    

@main.route('/delete/<nomC>', methods=['POST', 'DELETE'])
def delete_constructor(nomC):
    
    try:
        # TODO: check parameter integrity
        affected_rows, status = ModelConstructor.delete_constructor(nomC)

        if affected_rows > 0:
            return redirect(url_for('constructor.get_constructors')), 302
        else:
            return internal_server_error(status, "constructor.get_constructors"), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
