import config.settings as settings

from scripts.monitor import (
    run_monitor,
    stop_monitor
)

import threading

import config.settings as settings

from scripts.monitor import (
    run_monitor,
    stop_monitor
)


# =========================
# GLOBAL STATES
# =========================

monitor_thread = None

monitor_active = False

failed_attempts = 0

class Colors:

    RED = "\033[91m"

    GREEN = "\033[92m"

    RESET = "\033[0m"

monitor_thread = None

monitor_active = False


def show_banner():

    print("\n========================")

    print("     ARGUSCORE")

    print(
        f"     Version {settings.APP_VERSION}"
    )

    print("========================\n")

def verify_admin_password():

    global failed_attempts

    password = input(
        "\nAdministrator Password: "
    )

    if password == settings.ADMIN_PASSWORD:

        failed_attempts = 0

        return True

    failed_attempts += 1

    remaining = (
        settings.MAX_LOGIN_ATTEMPTS
        - failed_attempts
    )

    print(
        f"\n[SECURITY] Invalid password"
    )

    print(
        f"Attempts remaining: "
        f"{remaining}\n"
    )

    if (
        failed_attempts
        >= settings.MAX_LOGIN_ATTEMPTS
    ):

        settings.LOCKDOWN_MODE = True

        print(
            "\n[SECURITY] "
            "LOCKDOWN ACTIVATED"
        )

        print(
            "ArgusCore has been locked.\n"
        )

        exit()

    return False


def system_status():

    print("\n===== SYSTEM STATUS =====\n")

    monitoring_status = (
        "ONLINE"
        if monitor_active
        else "OFFLINE"
    )

    monitoring_color = (
        Colors.GREEN
        if monitor_active
        else Colors.RED
    )

    debug_status = (
        "ENABLED"
        if settings.DEBUG_MODE
        else "DISABLED"
    )

    debug_color = (
        Colors.GREEN
        if settings.DEBUG_MODE
        else Colors.RED
    )

    print(
        f"SCAN MODE: "
        f"{monitoring_color}"
        f"{monitoring_status}"
        f"{Colors.RESET}"
    )

    print(
        f"DEBUG MODE: "
        f"{debug_color}"
        f"{debug_status}"
        f"{Colors.RESET}"
    )

    print(
        f"MONITOR INTERVAL: "
        f"{settings.MONITOR_INTERVAL}s"
    )


def system_status():

    print("\n===== ESTADO SISTEMA =====\n")

    print(f"DEBUG MODE: {settings.DEBUG_MODE}")

    print(
        f"MONITOR INTERVAL: "
        f"{settings.MONITOR_INTERVAL}s"
    )


def show_menu():

    monitoring_status = (
        "ON"
        if monitor_active
        else "OFF"
    )

    monitoring_color = (
        Colors.GREEN
        if monitor_active
        else Colors.RED
    )

    debug_status = (
        "ON"
        if settings.DEBUG_MODE
        else "OFF"
    )

    debug_color = (
        Colors.GREEN
        if settings.DEBUG_MODE
        else Colors.RED
    )

    print(
        f"1. Scan Mode "
        f"{monitoring_color}"
        f"[{monitoring_status}]"
        f"{Colors.RESET}"
    )

    print("2. System Status")

    print(
        f"3. Debug Mode "
        f"{debug_color}"
        f"[{debug_status}]"
        f"{Colors.RESET}"
    )

    print("4. Recent Errors")

    print("5. Recent Detections")

    print("6. Metrics")

    print("7. Exit\n")

def toggle_debug():

    settings.DEBUG_MODE = (
        not settings.DEBUG_MODE
    )

    status = (
        "enabled"
        if settings.DEBUG_MODE
        else "disabled"
    )

    print(
        f"\n[+] Debug mode {status}\n"
    )


def show_errors():

    print("\n===== ERRORES =====\n")

    try:

        with open(
            "logs/errors.log",
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

            if not lines:

                print("No hay errores registrados.\n")

            else:

                for line in lines[-10:]:

                    print(line.strip())

    except FileNotFoundError:

        print("Archivo errors.log no encontrado.\n")

    except Exception as error:

        print(f"[ERROR] {error}")


def show_detections():

    print("\n===== DETECCIONES =====\n")

    try:

        with open(
            "logs/detections.log",
            "r",
            encoding="utf-8"
        ) as file:

            lines = file.readlines()

            if not lines:

                print("No hay detecciones registradas.\n")

            else:

                for line in lines[-10:]:

                    print(line.strip())

    except FileNotFoundError:

        print("Archivo detections.log no encontrado.\n")

    except Exception as error:

        print(f"[ERROR] {error}")


def show_metrics():

    print("\n===== METRICAS =====\n")

    print("Modulo de metricas aun en desarrollo.\n")


def start_monitor():

    global monitor_thread
    global monitor_active

    if monitor_active:

        print(
            "\n[!] Monitoring already active\n"
        )

        return

    print(
        "\n[+] Starting ArgusCore monitor...\n"
    )

    monitor_thread = threading.Thread(
        target=run_monitor,
        daemon=True
    )

    monitor_thread.start()

    monitor_active = True


def toggle_monitoring():

    global monitor_active

    if monitor_active:

        if verify_admin_password():

            stop_monitor()

            monitor_active = False

            print(
                "\n[+] "
                "Scan mode disabled\n"
            )

    else:

        start_monitor()

        print(
            "\n[+] Scan mode enabled\n"
        )


def stop_monitor_secure():

    password = input(
        "\nIngrese contraseña administrador: "
    )

    if password == settings.ADMIN_PASSWORD:

        stop_monitor()

    else:

        print("\n[ERROR] Contraseña incorrecta\n")


def start_console():

    while True:

        show_banner()

        show_menu()

        option = input("Seleccione opción: ")

        # =========================
        # INICIAR MONITOREO
        # =========================

        if option == "1":

            toggle_monitoring()

        # =========================
        # ESTADO SISTEMA
        # =========================

        elif option == "2":

            system_status()

        # =========================
        # DEBUG MODE
        # =========================

        elif option == "3":

            toggle_debug()

        # =========================
        # VER ERRORES
        # =========================

        elif option == "4":

            show_errors()

        # =========================
        # VER DETECCIONES
        # =========================

        elif option == "5":

            show_detections()

        # =========================
        # VER METRICAS
        # =========================

        elif option == "6":

            show_metrics()

        # =========================
        # SALIR
        # =========================

        elif option == "7":

            if verify_admin_password():

                print("\n[+] Shutting down ArgusCore...\n")

                break   


        # =========================
        # OPCION INVALIDA
        # =========================

        else:

            print("\n[!] Invalid option\n")