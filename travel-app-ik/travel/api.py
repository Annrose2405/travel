from flask import Blueprint, jsonify, request
from travel.models import Hotel, Room
from travel import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/hotels')
def get_hotel():
    hotels = db.session.scalars(db.select(Hotel)).all()
    hotel_list = [h.to_dict() for h in hotels]
    return jsonify(hotels=hotel_list)

@api_bp.route('/hotels', methods=['POST'])
def create_hotel():
    json_dict = request.get_json()
    if not json_dict:
        return jsonify(message="No input data provided!"), 400
    hotel = Hotel(name=json_dict['name'], description=json_dict['description'],
        destination_id=json_dict['destination_id'])
    for room_json in json_dict['rooms']:
        if "hotel_id" in room_json:
            room = db.session.scalar(db.select(Room).where(Room.id==room_json.id))
        else:
            room = Room(type=room_json['room_type'], num_rooms=room_json['num_rooms'],
                description=room_json['room_description'], rate=room_json['room_rate'],
                hotel_id=hotel.id)
    db.session.add(hotel, room)
    db.session.commit()
    return jsonify(message='Successfully created new hotel!'), 201
# Delete existing hotel
@api_bp.route('/hotels/<int:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    hotel = db.session.scalar(db.select(Hotel).where(Hotel.id==hotel_id))
    db.session.delete(hotel)
    db.session.commit()
    return jsonify(message='Record deleted!'), 200

# Update existing Hotel
@api_bp.route('/hotels/<int:hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    json_dict = request.get_json()
    hotel = db.session.scalar(db.select(Hotel).where(Hotel.id==hotel_id))
    hotel.name = json_dict['name']
    hotel.description = json_dict['description']
    db.session.commit()
    return jsonify(message='Record updated!'), 200