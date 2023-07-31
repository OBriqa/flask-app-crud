from flask import Blueprint, current_app, jsonify, render_template, request, redirect, url_for

# Models
from models.ModelParticipa import ModelParticipa

# Entities
from models.entities.Participa import Participa

# Utils
from utils.Format import ceil
from utils.Format import Format
from utils.Format import classes, id_class, fid_class
from utils.Format import PAGE_ELEMENTS, NUM_NAV_BUTTONS

from utils.error_handler import page_not_found, internal_server_error

main = Blueprint("participa", __name__)

@main.route('/', methods=['GET'])
def get_participants():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelParticipa.get_id() if order is None else order
            
    key = ModelParticipa.get_id()
    headings = ModelParticipa.get_headings()
    attributes = ModelParticipa.get_atributtes()

    max_page = int(ceil(ModelParticipa.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1
    
    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        participants, status = ModelParticipa.get_participants(num_page, order, query)
        return render_template('base_model.html',
                                id = key, 
                                data = participants,
                                titol = 'Participants',
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
        headings = ModelParticipa.get_headings()
        attributes = ModelParticipa.get_atributtes()
        return render_template('search_entity.html',
                                titol = 'Participants',
                                attributes = attributes,
                                headings = headings), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/search/', methods=['GET', 'POST'])
def search():
    
    query = {}
    page = request.args.get('page')
    order = request.args.get('order')
    order = ModelParticipa.get_id() if order is None else order

    if request.method == 'POST':        
        query['nomP'] = request.form['nomP']
        query['nomP-op'] = request.form['nomP-op']

        query['anyT'] = request.form['anyT']
        query['anyT-op'] = request.form['anyT-op']
        
        Format.parse_query(query)
        current_app.config['search'] = query

    elif request.method == 'GET':
        query = current_app.config['search']

    key = ModelParticipa.get_id()
    headings = ModelParticipa.get_headings()
    attributes = ModelParticipa.get_atributtes()

    max_page = int(ceil(ModelParticipa.get_numElements(query)/PAGE_ELEMENTS))
    max_page = max_page if max_page > 0 else 1

    num_page = Format.parse_numpage(1 if page is None else page, max_page)

    try:
        participants, status = ModelParticipa.get_participants(num_page, order, query)
        return render_template('base_model.html',
                                id = key,
                                data = participants,
                                titol = 'Participants',
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