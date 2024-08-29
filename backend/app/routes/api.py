from flask import jsonify, request
from . import main_bp
from ..services.readwise_processor import process_highlights
from ..services.tweet_generator import to_tweet_variations, to_thread
from ..services.typefully_api import create_typefully_draft
from ..logger import get_logger
import asyncio
from ..services.error_reporting import report_error_to_discord

logger = get_logger(__name__)

@main_bp.route('/')
def health_check():
    return 'Health check passed', 200

@main_bp.route('/process-highlights', methods=['POST'])
def trigger_process_highlights():
    try:
        highlights = process_highlights()
        logger.info("Processed highlights", extra={"count": len(highlights)})
        return jsonify({"status": "success", "highlights_processed": len(highlights)}), 200
    except Exception as e:
        error_message = f"Error processing highlights: {str(e)}"
        logger.error(error_message, extra={"error": str(e)}, exc_info=True)
        asyncio.create_task(report_error_to_discord(error_message))
        return jsonify({"status": "error", "message": str(e)}), 500

@main_bp.route('/generate-tweets', methods=['POST'])
def api_generate_tweets():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"status": "error", "message": "Missing content in request"}), 400
    
    try:
        variations = asyncio.run(to_tweet_variations(data['content']))
        return jsonify({"status": "success", "variations": variations}), 200
    except Exception as e:
        error_message = f"Error generating tweet variations: {str(e)}"
        logger.error(error_message, extra={"error": str(e)}, exc_info=True)
        asyncio.create_task(report_error_to_discord(error_message))
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
        error_message = f"Error generating thread: {str(e)}"
        logger.error(error_message, extra={"error": str(e)}, exc_info=True)
        asyncio.create_task(report_error_to_discord(error_message))
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
        error_message = f"Error creating Typefully draft: {str(e)}"
        logger.error(error_message, extra={"error": str(e)}, exc_info=True)
        asyncio.create_task(report_error_to_discord(error_message))
        return jsonify({"status": "error", "message": str(e)}), 500