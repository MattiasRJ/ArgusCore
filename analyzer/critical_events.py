from database.connection import get_connection

from utils.logger import (
    detection_logger,
    error_logger
)

from config.settings import DEBUG_MODE


def detect_critical_events():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            SELECT
                ip_address,
                event_type,
                COUNT(*) as total_events
            FROM logs
            WHERE severity = 'critical'
            AND processed = FALSE
            GROUP BY ip_address, event_type
            HAVING COUNT(*) >= 1;
        """

        if DEBUG_MODE:
            print("\n[DEBUG] Ejecutando detector critical events")
            print(query)

        cursor.execute(query)

        results = cursor.fetchall()

        for result in results:

            ip_address, event_type, total_events = result

            print(
                f"[CRITICAL EVENT] "
                f"{event_type} desde {ip_address} | "
                f"Eventos: {total_events}"
            )

            detection_logger.info(
                f"CRITICAL EVENT DETECTADO | "
                f"IP: {ip_address} | "
                f"Evento: {event_type} | "
                f"Cantidad: {total_events}"
            )

        cursor.close()

        connection.close()

    except Exception as error:

        error_logger.error(
            f"Error en critical_events.py: {error}"
        )

        if DEBUG_MODE:
            print(f"\n[ERROR DEBUG] {error}\n")