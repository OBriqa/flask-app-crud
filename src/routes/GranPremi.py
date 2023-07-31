from flask import Blueprint, current_app, jsonify, render_template, redirect, url_for, request

# Models
from models.ModelGranPremi import ModelGranPremi

# Entities
from models.entities.GranPremi import GranPremi

# Utils
from utils.Format import ceil
from utils.Format import Format
from utils.Format import classes, id_class, fid_class
from utils.Format import PAGE_ELEMENTS, NUM_NAV_BUTTONS

from utils.error_handler import page_not_found, internal_server_error

main = Blueprint("granpremi", __name__)

@main.route('/', methods=['GET'])
def get_gransPremis():

    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelGranPremi.get_id() if order is None else order

    key = ModelGranPremi.get_id()
    headings = ModelGranPremi.get_headings()
    attributes = ModelGranPremi.get_attributes()

    max_page = int(ceil(ModelGranPremi.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        granspremis, status = ModelGranPremi.get_gransPremis(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = granspremis,
                                titol = 'Grans Premis',
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
        headings = ModelGranPremi.get_headings()
        attributes = ModelGranPremi.get_attributes()
        return render_template('search_entity.html',
                                titol = 'Grans Premis',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/search/', methods=['GET', 'POST'])
def search():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelGranPremi.get_id() if order is None else order

    if request.method == 'POST':        
        query['nomGP'] = request.form['nomGP']
        query['nomGP-op'] = request.form['nomGP-op']

        query['circuit'] = request.form['circuit']
        query['circuit-op'] = request.form['circuit-op']

        query['situat'] = request.form['situat']
        query['situat-op'] = request.form['situat-op']
        
        Format.parse_query(query)
        current_app.config['search'] = query

    elif request.method == 'GET':
        query = current_app.config['search']

    key = ModelGranPremi.get_id()
    headings = ModelGranPremi.get_headings()
    attributes = ModelGranPremi.get_attributes()

    max_page = int(ceil(ModelGranPremi.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        granspremis, status = ModelGranPremi.get_gransPremis(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = granspremis,
                                titol = 'Grans Premis',
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
    
@main.route('/<nomGP>', methods=['GET'])
def get_granPremi(nomGP):
    
    try:
        granpremi, status = ModelGranPremi.get_granPremi(nomGP)
        if granpremi != None:
            headings = ModelGranPremi.get_headings()
            attributes = ModelGranPremi.get_attributes()
            return render_template('entity_model.html',
                                    id = nomGP,
                                    data = [granpremi],
                                    titol = 'Grans Premis',
                                    attributes = attributes,
                                    headings = headings), 200
        else:
            return page_not_found(404, 'granpremi.get_gransPremis'), 404    

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/add', methods=['POST'])
def add_granPremi():
    
    # TODO: check parameter integrity
    nomGP = request.form['nomGP']
    circuit = request.form['circuit']
    situat = request.form['situat']

    try:
        granpremi = GranPremi(nomGP, circuit, situat)
        affected_rows, status = ModelGranPremi.add_granPremi(granpremi)

        if affected_rows > 0:
            return redirect(url_for('granpremi.get_granPremi', nomGP = nomGP)), 302
        else:
            return internal_server_error(status, 'granpremi.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/afegir', methods=['GET'])
def afegir():

    try:
        headings = ModelGranPremi.get_headings()
        attributes = ModelGranPremi.get_attributes()
        return render_template('add_entity.html',
                                titol = 'Grans Premis',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/update/<nomGP>', methods=['POST', 'PUT'])
def update_granPremi(nomGP):

    # TODO: check parameter integrity
    circuit = request.form['circuit']
    situat = request.form['situat']

    try:
        granpremi = GranPremi(nomGP, circuit, situat)
        affected_rows, status = ModelGranPremi.update_granPremi(granpremi)

        if affected_rows > 0:
            return redirect(url_for('granpremi.get_granPremi', nomGP = nomGP)), 302
        else:
            return internal_server_error(status, 'granpremi.afegir'), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/actualitzar/<nomGP>', methods=['GET'])
def actualitzar(nomGP):
    
    try:
        headings = ModelGranPremi.get_headings()
        attributes = ModelGranPremi.get_attributes()
        granpremi, status = ModelGranPremi.get_granPremi(nomGP)
        return render_template('modify_entity.html',
                                id = nomGP,
                                data = granpremi,
                                titol = 'Grans Premis',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/delete/<nomGP>', methods=['POST', 'DELETE'])
def delete_pilot(nomGP):
    
    try:
        # TODO: check parameter integrity
        affected_rows, status = ModelGranPremi.delete_granPremi(nomGP)

        if affected_rows > 0:
            return redirect(url_for('granpremi.get_gransPremis')), 302
        else:
            return internal_server_error(status, "granpremi.get_gransPremis"), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500