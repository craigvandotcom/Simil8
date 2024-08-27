from flask import jsonify, request
from . import main_bp
from ..services.readwise_processor import process_highlights
from ..services.tweet_generator import to_tweet_variations, to_thread
from ..services.typefully_api import create_typefully_draft

@main_bp.route('/')
def health_check():
    return 'Health check passed', 200

@main_bp.route('/process-highlights', methods=['POST'])
def trigger_process_highlights():
    try:
        highlights = process_highlights()
        return jsonify({"status": "success", "highlights_processed": len(highlights)}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main_bp.route('/generate-tweets', methods=['POST'])
def api_generate_tweets():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"status": "error", "message": "Missing content in request"}), 400
    
    try:
        variations = to_tweet_variations(data['content'])
        return jsonify({"status": "success", "variations": variations}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main_bp.route('/generate-thread', methods=['POST'])
def api_to_thread():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"status": "error", "message": "Missing content in request"}), 400
    
    try:
        thread = to_thread(data['content'])
        return jsonify({"status": "success", "thread": thread}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main_bp.route('/create-typefully-draft', methods=['POST'])
def api_create_typefully_draft():
    data = request.json
    if not data or 'tweets' not in data:
        return jsonify({"status": "error", "message": "Missing tweets in request"}), 400
    
    try:
        draft = create_typefully_draft(data['tweets'])
        return jsonify({"status": "success", "draft": draft}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500