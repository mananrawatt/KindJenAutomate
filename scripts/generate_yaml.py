import os
from jinja2 import Environment, FileSystemLoader

def render_template(template_name, variables, output_path):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    output = template.render(variables)
    with open(output_path, "w") as f:
        f.write(output)

def load_env(env_file):
    vars = {}
    with open(env_file) as f:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            key, value = line.strip().split('=', 1)
            vars[key] = value
    return vars

if __name__ == "__main__":
    os.makedirs("rendered_yamls", exist_ok=True)
    variables = load_env("params.env")
    render_template("deployment_template.yaml", variables, "rendered_yamls/deployment.yaml")
    render_template("service_template.yaml", variables, "rendered_yamls/service.yaml")
