from database.connection import get_connection

from utils.logger import (
    detection_logger,
    error_logger
)

from config.settings import DEBUG_MODE


def detect_brute_force():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            SELECT
                ip_address,
                COUNT(*) as attempts
            FROM logs
            WHERE event_type = 'failed_login'
            AND processed = FALSE
            GROUP BY ip_address
            HAVING COUNT(*) >= 5;
        """

        if DEBUG_MODE:
            print("\n[DEBUG] Ejecutando detector brute force")
            print(query)

        cursor.execute(query)

        results = cursor.fetchall()

        for result in results:

            ip_address, attempts = result

            print(
                f"[BRUTE FORCE] "
                f"IP: {ip_address} | "
                f"Intentos: {attempts}"
            )

            detection_logger.info(
                f"BRUTE FORCE DETECTADO | "
                f"IP: {ip_address} | "
                f"Intentos: {attempts}"
            )

        cursor.close()

        connection.close()

    except Exception as error:

        error_logger.error(
            f"Error en brute_force.py: {error}"
        )

        if DEBUG_MODE:
            print(f"\n[ERROR DEBUG] {error}\n")