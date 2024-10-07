from flask import jsonify, request
from functools import wraps
from . import main_bp
from ..services.readwise_processor import process_highlights
from ..services.tweet_generator import to_tweet_variations, to_thread
from ..services.typefully_api import create_typefully_draft
from ..logger import get_logger
from ..services.error_reporting import report_error_to_discord
from datetime import datetime, timedelta
from ..config import Config
import asyncio  # Import asyncio to handle asynchronous calls

logger = get_logger(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == Config.SIMIL8_API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 401
    return decorated

@main_bp.route('/')
def health_check():
    return 'Health check passed', 200

@main_bp.route('/typefully', methods=['POST'])
@require_api_key
def create_typefully_content():
    try:
        data = request.json
        account = data.get('account', 'account1')
        tweets = data.get('tweets', [])
        threads = data.get('threads', [])
        scheduled = data.get('scheduled', 'no')
        auto_retweet = data.get('auto_retweet', 'no').lower() == 'yes'

        if account not in ['account1', 'account2']:
            return jsonify({'error': 'Invalid account specified'}), 400

        if not tweets and not threads:
            return jsonify({'error': 'No content provided'}), 400

        schedule = scheduled.lower() == 'yes'
        schedule_date = "next-free-slot" if schedule else None

        if schedule and scheduled.lower() != 'yes':
            schedule_date = scheduled  # Use the provided date/time

        results = []

        # Process individual tweets
        for tweet in tweets:
            # Use asyncio.run to execute the async function
            draft = asyncio.run(create_typefully_draft(
                [tweet],
                account,
                schedule,
                schedule_date,
                auto_retweet
            ))
            results.append({
                'type': 'tweet',
                'draft_id': draft.get('id'),
                'share_url': draft.get('share_url')
            })

        # Process threads
        for thread in threads:
            draft = asyncio.run(create_typefully_draft(
                thread,
                account,
                schedule,
                schedule_date,
                auto_retweet
            ))
            results.append({
                'type': 'thread',
                'draft_id': draft.get('id'),
                'share_url': draft.get('share_url')
            })

        return jsonify({
            'message': 'Typefully drafts created successfully',
            'results': results
        }), 200

    except Exception as e:
        error_message = f"Error creating Typefully content: {str(e)}"
        logger.error(error_message, exc_info=True)
        # Use asyncio.run to execute the async function
        asyncio.run(report_error_to_discord(error_message))
        return jsonify({'error': error_message}), 500

@main_bp.route('/typefullyThreadsWeekly', methods=['POST'])
@require_api_key
def create_typefully_threads_weekly():
    try:
        data = request.json
        account = data.get('account', 'account1')
        threads = data.get('threads', [])

        if account not in ['account1', 'account2']:
            return jsonify({'error': 'Invalid account specified'}), 400

        if not threads:
            return jsonify({'error': 'Please provide at least one thread'}), 400

        # Get today's date and day of the week
        today = datetime.now().date()
        today_weekday = today.weekday()

        # Define the target weekdays (Monday = 0, Wednesday = 2, Friday = 4)
        target_weekdays = [0, 2, 4]

        # Find scheduling slots for all threads
        schedule_dates = []
        current_date = today
        while len(schedule_dates) < len(threads):
            if current_date.weekday() in target_weekdays and (current_date > today or current_date.weekday() > today_weekday):
                schedule_dates.append(current_date)
            current_date += timedelta(days=1)

        # Create a list of scheduling times (all at 4 PM)
        schedule_times = [
            datetime.combine(date, datetime.min.time().replace(hour=16, minute=0))
            for date in schedule_dates
        ]

        results = []

        for index, thread in enumerate(threads):
            schedule_date = schedule_times[index].isoformat()
            
            # Use asyncio.run to execute the async function
            draft = asyncio.run(create_typefully_draft(
                thread,
                account,
                schedule=True,
                schedule_date=schedule_date,
                auto_retweet=False
            ))
            results.append({
                'type': 'thread',
                'draft_id': draft.get('id'),
                'share_url': draft.get('share_url'),
                'scheduled_date': schedule_date
            })

        return jsonify({
            'message': 'Typefully threads scheduled successfully',
            'results': results
        }), 200

    except Exception as e:
        error_message = f"Error creating Typefully threads: {str(e)}"
        logger.error(error_message, exc_info=True)
        asyncio.run(report_error_to_discord(error_message))
        return jsonify({'error': error_message}), 500

