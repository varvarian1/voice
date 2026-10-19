#!/usr/bin/env python3
"""Cross-platform bootstrap: ensure Ollama + gemma4:e4b are installed and running
natively on the host, then hand off to `docker compose up --build`."""

import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.request

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(PROJECT_DIR, "models", "ollama")
MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:e4b")
OLLAMA_URL = "http://localhost:11434"


def ollama_installed() -> bool:
    return shutil.which("ollama") is not None


def install_ollama() -> None:
    system = platform.system()
    print("Ollama не найдена, устанавливаю...")

    if system == "Linux":
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
    elif system == "Windows":
        if shutil.which("winget") is None:
            raise SystemExit(
                "winget не найден. Установите Ollama вручную: https://ollama.com/download"
            )
        subprocess.run(
            ["winget", "install", "--id", "Ollama.Ollama", "-e", "--silent"], check=True
        )
    elif system == "Darwin":
        raise SystemExit(
            "Установите Ollama вручную: https://ollama.com/download (или `brew install ollama`)"
        )
    else:
        raise SystemExit(f"Неизвестная ОС: {system}, установите Ollama вручную.")


def ensure_running() -> None:
    os.makedirs(MODELS_DIR, exist_ok=True)
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = MODELS_DIR

    if platform.system() == "Linux" and shutil.which("systemctl"):
        print(f"Настраиваю systemd-сервис ollama на хранение моделей в {MODELS_DIR}...")
        override_dir = "/etc/systemd/system/ollama.service.d"
        os.makedirs(override_dir, exist_ok=True)
        with open(os.path.join(override_dir, "override.conf"), "w") as f:
            f.write(f'[Service]\nEnvironment="OLLAMA_MODELS={MODELS_DIR}"\n')
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "--now", "ollama"], check=True)
    else:
        print(f"Запускаю ollama serve в фоне (модели в {MODELS_DIR})...")
        subprocess.Popen(
            ["ollama", "serve"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def wait_for_api(timeout: int = 60) -> None:
    print("Жду готовности Ollama API...")
    for _ in range(timeout):
        try:
            urllib.request.urlopen(OLLAMA_URL, timeout=1)
            return
        except Exception:
            time.sleep(1)
    raise SystemExit("Ollama API не поднялась за отведённое время.")


def model_present() -> bool:
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    return MODEL in result.stdout


def main() -> None:
    if platform.system() == "Linux" and hasattr(os, "geteuid") and os.geteuid() != 0:
        print(
            "Предупреждение: на Linux этот скрипт обычно нужно запускать с правами root "
            "(sudo python3 run.py) для установки/настройки systemd-сервиса Ollama.",
            file=sys.stderr,
        )

    if not ollama_installed():
        install_ollama()

    ensure_running()
    wait_for_api()

    if model_present():
        print(f"Модель {MODEL} уже скачана в {MODELS_DIR}, пропускаю загрузку.")
    else:
        print(f"Скачиваю модель {MODEL}...")
        subprocess.run(["ollama", "pull", MODEL], check=True)

    print("Запускаю docker compose up --build...")
    docker = shutil.which("docker")
    if docker is None:
        raise SystemExit("docker не найден в PATH.")
    os.execvp(docker, [docker, "compose", "up", "--build", *sys.argv[1:]])


if __name__ == "__main__":
    main()
