import subprocess

def register_jupyter_kernel(env_name, display_name=None):
    display_name = display_name or f"Pim: {env_name}"
    subprocess.run(
        f"conda run -n {env_name} python -m ipykernel install --user --name={env_name} --display-name='{display_name}'",
        shell=True,
        check=True
    )
