import launch

if not launch.is_installed("anthropic"):
    launch.run_pip("install anthropic")
    print("[Prompt-Artisan] Installing anthropic...")

if not launch.is_installed("openai"):
    launch.run_pip("install openai")
    print("[Prompt-Artisan] Installing openai...")