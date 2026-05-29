import time

import config.settings as settings

from collector.collector import load_logs

from analyzer.analyzer import run_analysis


monitor_running = False


def run_monitor():

    global monitor_running

    monitor_running = True

    print("\n[+] ArgusCore monitoring started\n")

    while monitor_running:

        # =========================
        # DEBUG
        # =========================

        if settings.DEBUG_MODE:

            print("[DEBUG] Loading logs")

        # =========================
        # LOAD LOGS
        # =========================

        load_logs()

        # =========================
        # DEBUG
        # =========================

        if settings.DEBUG_MODE:

            print("[DEBUG] Running analysis engine")

        # =========================
        # RUN ANALYSIS
        # =========================

        run_analysis()

        # =========================
        # DEBUG
        # =========================

        if settings.DEBUG_MODE:

            print(
                "[DEBUG] Waiting next cycle...\n"
            )

        time.sleep(settings.MONITOR_INTERVAL)


def stop_monitor():

    global monitor_running

    monitor_running = False

    print("\n[+] Monitoring stopped\n")