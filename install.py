import launch

if not launch.is_installed("anthropic"):
    launch.run_pip("install anthropic")
    print("Installing anthropic...")