"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person
# src/app.py

app = Flask(__name__)
jackson_family = FamilyStructure('Jackson')

# Initialize with initial family members
jackson_family.add_member({
    'first_name': 'John',
    'age': 33,
    'lucky_numbers': [7, 13, 22]
})

jackson_family.add_member({
    'first_name': 'Jane',
    'age': 35,
    'lucky_numbers': [10, 14, 3]
})

jackson_family.add_member({
    'first_name': 'Jimmy',
    'age': 5,
    'lucky_numbers': [1]
})

@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is not None:
            return jsonify(member), 200
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.json
        if not all(key in data for key in ('first_name', 'age', 'lucky_numbers')):
            return jsonify({'error': 'Missing fields in request'}), 400
        if not isinstance(data['lucky_numbers'], list):
            return jsonify({'error': 'lucky_numbers must be a list'}), 400
        
        jackson_family.add_member(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is not None:
            jackson_family.delete_member(member_id)
            return jsonify({'done': True}), 200
        else:
            return jsonify({'error': 'Member not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
