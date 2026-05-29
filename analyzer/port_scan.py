from database.connection import get_connection

from utils.logger import (
    detection_logger,
    error_logger
)

from config.settings import DEBUG_MODE


def detect_port_scan():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        query = """
            SELECT
                ip_address,
                COUNT(*) as total_scans
            FROM logs
            WHERE event_type = 'port_scan'
            AND processed = FALSE
            GROUP BY ip_address
            HAVING COUNT(*) >= 5;
        """

        if DEBUG_MODE:
            print("\n[DEBUG] Ejecutando detector port scan")
            print(query)

        cursor.execute(query)

        results = cursor.fetchall()

        for result in results:

            ip_address, total_scans = result

            print(
                f"[PORT SCAN] "
                f"IP: {ip_address} | "
                f"Scans: {total_scans}"
            )

            detection_logger.info(
                f"PORT SCAN DETECTADO | "
                f"IP: {ip_address} | "
                f"Scans: {total_scans}"
            )

        cursor.close()

        connection.close()

    except Exception as error:

        error_logger.error(
            f"Error en port_scan.py: {error}"
        )

        if DEBUG_MODE:
            print(f"\n[ERROR DEBUG] {error}\n")