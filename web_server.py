from flask import Flask, request, jsonify
from readwise_processor import process_highlights
from tweet_generator import generate_tweet_variations, generate_thread, create_highlight_thread
from typefully_api import create_typefully_draft
import logging

app = Flask(__name__)

def serialize_draft(draft):
    """Helper function to serialize draft data"""
    return {
        "id": draft.get('id'),
        "share_url": draft.get('share_url')
    }

@app.route('/')
def health_check():
    return 'Readwise to Typefully script is running!', 200

@app.route('/process-highlights', methods=['POST'])
def process_readwise_highlights():
    try:
        highlights = process_highlights()
        results = []

        for highlight in highlights:
            try:
                processed_content = generate_tweet_variations(highlight['text'])
                tweet_versions = processed_content
                tweets = [
                    f"📚 {highlight['book_title']}\n\nOriginal highlight: \"{highlight['text']}\"\n\n🔗 {highlight['readwise_url']}"
                ] + tweet_versions
                draft = create_typefully_draft(tweets)
                results.append({
                    "highlight_id": highlight['id'],
                    "draft": serialize_draft(draft)
                })
            except Exception as e:
                logging.error(f"Error processing highlight {highlight['id']}: {str(e)}", exc_info=True)
                results.append({
                    "highlight_id": highlight['id'],
                    "error": str(e)
                })

        return jsonify(results)
    except Exception as e:
        logging.error(f"Error in process_readwise_highlights: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/generate-tweets', methods=['POST'])
def generate_tweets_endpoint():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    try:
        tweet_versions = generate_tweet_variations(data['text'])
        draft = create_typefully_draft(tweet_versions)
        return jsonify(serialize_draft(draft))
    except Exception as e:
        logging.error(f"Error in generate_tweets_endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/generate-threads', methods=['POST'])
def generate_threads_endpoint():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    try:
        thread1 = generate_thread(data['text'])
        thread2 = generate_thread(data['text'])
        draft1 = create_typefully_draft(thread1)
        draft2 = create_typefully_draft(thread2)
        return jsonify({
            "thread1": serialize_draft(draft1),
            "thread2": serialize_draft(draft2)
        })
    except Exception as e:
        logging.error(f"Error in generate_threads_endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/run-frequent-task', methods=['POST'])
def run_frequent_task_endpoint():
    try:
        highlights = process_highlights()
        results = []

        for highlight in highlights:
            thread = create_highlight_thread(highlight)

            # Add logging to check the content of the thread
            logging.info(f"Generated thread for highlight {highlight['id']}: {thread}")

            response = create_typefully_draft(thread)

            # Extract relevant information from the response
            result = {
                "status": "success",
                "highlight_id": highlight['id'],
                "draft_id": response.get("id"),
                "share_url": response.get("share_url"),
                "tweet_count": len(thread)
            }
            results.append(result)

        return jsonify({"message": "Frequent task completed successfully", "results": results})
    except Exception as e:
        logging.error(f"Error in frequent task: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def start_server():
    app.run(host="0.0.0.0", port=8080)