import os
import shutil
from datetime import datetime
from dtpr.utils.functions import color_msg


def create_ntuple_class_template(name, output_folder):
    template_source_path = os.path.join(
        os.path.dirname(__file__), "templates/ntuple_class_template.txt"
    )
    if "ntuple" in name.lower():
        final_name = name.lower().replace("ntuple", "_ntuple")
    else:
        final_name = name.lower()
    template_dest_path = os.path.join(output_folder, f"{final_name}.py")

    replace_placeholders(template_source_path, template_dest_path, name)
    print(
        color_msg(f"{name} class created from template in:", "green", return_str=True)
        + color_msg(f"{template_dest_path}", "yellow", return_str=True)
    )


def create_particle_class_template(name, output_folder):
    template_source_path = os.path.join(
        os.path.dirname(__file__), "templates/particle_class_template.txt"
    )
    if "ntuple" in name.lower():
        final_name = name.lower().replace("ntuple", "_ntuple")
    else:
        final_name = name.lower()
    template_dest_path = os.path.join(output_folder, f"{final_name}.py")

    replace_placeholders(template_source_path, template_dest_path, name)
    print(
        color_msg(f"{name} class created from template in:", "green", return_str=True)
        + color_msg(f"{template_dest_path}", "yellow", return_str=True)
    )


def create_event_config_template(output_folder):
    template_source_path = os.path.join(
        os.path.dirname(__file__), "templates/event_config_template.yaml"
    )
    template_dest_path = os.path.join(output_folder, "event_config.yaml")

    shutil.copy(template_source_path, template_dest_path)
    print(
        color_msg(
            f"event_config.yaml created from template in:", "green", return_str=True
        )
        + color_msg(f"{template_dest_path}", "yellow", return_str=True)
    )


def replace_placeholders(file_source_path, file_dest_path, class_name):
    with open(file_source_path, "r") as file:
        content = file.read()
    content = content.replace("{name}", class_name)
    content = content.replace("{date}", datetime.now().strftime("%a %b %d %H:%M:%S %Y"))
    with open(file_dest_path, "w") as file:
        file.write(content)
