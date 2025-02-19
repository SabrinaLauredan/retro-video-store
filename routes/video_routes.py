from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime
from flask import Blueprint, jsonify, request


videos_bp = Blueprint("videos", __name__, url_prefix=("/videos"))


@videos_bp.route("", methods=["GET"])
def get_all_videos():
    """
    Retrieves all saved video records.
    """
    video = Video.query.all()
    video_response = [video.to_dict() for video in video]
    return jsonify(video_response), 200


@videos_bp.route("", methods=["POST"])
def create_video():
    """
    Allows client to create a new video record,
    which must have title, release_date, and
    total_inventory in request_body.
    """

    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify(details="Request body must include title."), 400

    if "release_date" not in request_body:
        return jsonify(details="Request body must include release_date."), 400

    if "total_inventory" not in request_body:
        return jsonify(details="Request body must include total_inventory."), 400

    new_video = Video(
    title=request_body["title"],
    release_date=request_body["release_date"],
    total_inventory = request_body["total_inventory"]
    )

    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201


@videos_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    """
    Allows client to retrieve a single video record,
    only after ensuring that the video_id is an integer.
    """

    try: 
        video_id = int(video_id)
    except:
        return jsonify(None), 400

    video = Video.query.get(video_id)

    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    return jsonify(video.to_dict()), 200


@videos_bp.route("/<video_id>", methods=["PUT"])
def edit_video_data(video_id):
    """
    Allows client to edit a single video record,
    only after ensuring that the video_id is an integer.
    """
    try: 
        video_id = int(video_id)
    except:
        return jsonify(None), 400

    video = Video.query.get(video_id)

    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    form_data = request.get_json()

    if "title" not in form_data or "release_date" not in form_data \
    or "total_inventory" not in form_data:
        return jsonify(None), 400

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]

    db.session.commit()

    return jsonify(video.to_dict()), 200


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    """
    Allows client to delete a single video record,
    only after ensuring that the video_id is an integer.
    """
    try: 
        video_id = int(video_id)
    except:
        return jsonify(None), 400

    video = Video.query.get(video_id)

    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    db.session.delete(video)
    db.session.commit()

    return jsonify(id=video.id), 200

@videos_bp.route("/<video_id>/rentals", methods=["GET"]) 
def get_customers_with_video_rented(video_id):
    """
    List of all customers with video rented.
    """
    try: 
        video_id = int(video_id)
    except:
        return jsonify(None), 400
    
    video  = Video.query.get(video_id)
    
    if video == None:
        return jsonify(message=f"Video {video_id} was not found"), 404

    rental_list = Rental.query.filter_by(video_id=video.id, checked_out=True)

    list_of_dicts = []

    for rental in rental_list:
        
        customer = Customer.query.get(rental.video_id)
        list_of_dicts.append({
        "due_date": rental.due_date,
        "name": customer.name,
        "phone": customer.phone,
        "postal_code": customer.postal_code
    })

    return jsonify(list_of_dicts), 200