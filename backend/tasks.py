import time
import logging
from celery_config import celery_app
from db import get_db_connection  # Import your DB connection function

logger = logging.getLogger(__name__)

@celery_app.task(name='debug_task')
def debug_task():
    """
    A simple debug task that logs a message.
    It does not depend on the FastAPI app context.
    """
    logger.info("Executing debug_task...")
    time.sleep(5)  # Simulate some work
    logger.info("Debug task finished.")
    return "Debug task completed successfully!"

@celery_app.task(name='example_db_task')
def example_db_task(some_data):
    """
    An example task that interacts with the database.
    It creates its own database connection.
    """
    logger.info(f"Executing example_db_task with data: {some_data}")
    conn = None
    try:
        # Get a new database connection for this task
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Example: Insert data into a hypothetical 'logs' table
        # Replace with your actual database logic
        cursor.execute(
            "INSERT INTO task_logs (message, created_at) VALUES (%s, NOW())",
            (f"Task executed with data: {some_data}",)
        )
        conn.commit()
        
        cursor.close()
        logger.info("Database operation successful.")
        return {"status": "success", "message": "Data logged to DB."}
    except Exception as e:
        logger.error(f"Database task failed: {e}", exc_info=True)
        # Optional: Implement retry logic with Celery's features
        # raise self.retry(exc=e, countdown=60)
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")
