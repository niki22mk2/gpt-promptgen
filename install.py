import launch

if not launch.is_installed("anthropic"):
    launch.run_pip("install anthropic")
    print("[Prompt-Gen] Installing anthropic...")

if not launch.is_installed("openai"):
    launch.run_pip("install openai")
    print("[Prompt-Gen] Installing openai...")

if not launch.is_installed("toml"):
    launch.run_pip("install toml")
    print("[Prompt-Gen] Installing toml...")