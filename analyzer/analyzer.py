import psycopg2

import config.settings as settings

from database.connection import get_connection


def run_analysis():

    detect_brute_force()

    detect_port_scan()

    detect_critical_events()

    mark_logs_as_processed()


# =========================
# BRUTE FORCE
# =========================

def detect_brute_force():

    if settings.DEBUG_MODE:

        print(
            "[DEBUG] Running brute force detector"
        )

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            COUNT(*) as attempts
        FROM logs
        WHERE event_type = 'failed_login'
        GROUP BY ip_address
        HAVING COUNT(*) >= 5;
    """

    if settings.DEBUG_MODE:

        print(query)

    cursor.execute(query)

    results = cursor.fetchall()

    for row in results:

        ip = row[0]

        attempts = row[1]

        print(
            f"[BRUTE FORCE] "
            f"IP: {ip} | Attempts: {attempts}"
        )

    cursor.close()

    conn.close()


# =========================
# PORT SCAN
# =========================

def detect_port_scan():

    if settings.DEBUG_MODE:

        print(
            "[DEBUG] Running port scan detector"
        )

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            COUNT(*) as total_scans
        FROM logs
        WHERE event_type = 'port_scan'
        GROUP BY ip_address
        HAVING COUNT(*) >= 5;
    """

    if settings.DEBUG_MODE:

        print(query)

    cursor.execute(query)

    results = cursor.fetchall()

    for row in results:

        ip = row[0]

        scans = row[1]

        print(
            f"[PORT SCAN] "
            f"IP: {ip} | Scans: {scans}"
        )

    cursor.close()

    conn.close()


# =========================
# CRITICAL EVENTS
# =========================

def detect_critical_events():

    if settings.DEBUG_MODE:

        print(
            "[DEBUG] Running critical event detector"
        )

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            ip_address,
            event_type,
            COUNT(*) as total_events
        FROM logs
        WHERE severity = 'critical'
        GROUP BY ip_address, event_type;
    """

    if settings.DEBUG_MODE:

        print(query)

    cursor.execute(query)

    results = cursor.fetchall()

    for row in results:

        ip = row[0]

        event_type = row[1]

        total_events = row[2]

        print(
            f"[CRITICAL EVENT] "
            f"{event_type} from {ip} "
            f"| Events: {total_events}"
        )

    cursor.close()

    conn.close()


def mark_logs_as_processed():

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        UPDATE logs
        SET processed = TRUE
        WHERE processed = FALSE
    """

    cursor.execute(query)

    conn.commit()

    cursor.close()

    conn.close() 