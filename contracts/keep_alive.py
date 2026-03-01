import os
import threading
import time
import urllib.request
import logging

logger = logging.getLogger(__name__)

def ping_app():
    """
    Pings the application's external URL every 10 minutes to prevent Render from spinning down the free instance.
    """
    url = os.environ.get('RENDER_EXTERNAL_URL')
    if not url:
        logger.warning("RENDER_EXTERNAL_URL is not set. Keep-alive thread will not ping.")
        return

    # Ensure URL ends with a slash or points to a valid public route.
    target_url = url if url.endswith('/') else f"{url}/"

    while True:
        # Wait for 10 minutes (600 seconds) before pinging
        # We sleep first so we don't ping immediately right as the app starts up
        logger.info("Keep-alive thread waiting 10 minutes before next ping...")
        time.sleep(600)
        
        try:
            logger.info(f"Keep-alive pinging {target_url}...")
            # We use a user-agent so it looks distinguishable in logs or to filters
            req = urllib.request.Request(target_url, headers={'User-Agent': 'KeepAlivePing/1.0'})
            with urllib.request.urlopen(req) as response:
                logger.info(f"Keep-alive ping successful: {response.getcode()}")
        except Exception as e:
            logger.error(f"Keep-alive ping failed: {e}")

def start_keep_alive():
    """Starts the background thread if running in a Render production environment."""
    if os.environ.get('RENDER') == 'true' or os.environ.get('RENDER') == '1':
        logger.info("Starting keep-alive background thread...")
        thread = threading.Thread(target=ping_app, daemon=True)
        thread.start()
