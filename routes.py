from flask import Blueprint, request, jsonify
from models.content_based import content_recommendations
from models.collaborative import collaborative_recommendations

recommend = Blueprint('recommend', __name__)

@recommend.route('/recommend', methods=['GET'])
def recommend_movies():
    title = request.args.get('title')
    user_id = request.args.get('user_id', type=int)

    if title:
        # Content-based recommendations
        recommendations = content_recommendations(title).tolist()
        return jsonify({'recommendations': recommendations})
    elif user_id:
        # Collaborative recommendations
        recommendations = collaborative_recommendations(user_id).index.tolist()
        return jsonify({'recommendations': recommendations})
    else:
        return jsonify({'error': 'Provide either a title or user_id'}), 400
