import subprocess
import sys
from pathlib import Path


def converter(base_dir, ui_path):
    templates_dir = base_dir / 'app' / 'templates'
    output_file = str(templates_dir / ui_path.stem) + '.py'
    try:
        subprocess.run(['pyuic5', str(ui_path), '-o', output_file], check=True)
        print(f"Converted successful: {ui_path.name} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error of converting {ui_path.name}: {e}")


def convert_ui_to_py(ui_file=None):
    """
    Converts .ui files to .py files using pyuic5.

    Args:
        ui_file (str, optional): Specific .ui file to convert.
                                If None, converts all .ui files.
    """
    # Define base paths
    base_dir = Path(__file__).parent
    ui_dir = base_dir / 'app' / 'templates' / 'ui'

    if ui_file:
        # Convert specific file
        ui_path = ui_dir / ui_file
        if not ui_path.exists():
            print(f"Error: File {ui_file} not found in {ui_dir}")
            return

        if not ui_file.endswith('.ui'):
            print("Error: File must have .ui extension")
            return

        converter(base_dir, ui_path)

    else:
        # Convert all .ui files
        ui_files = list(ui_dir.glob('*.ui'))
        if not ui_files:
            print(f"Error: No .ui files found in {ui_dir}")
            return

        for ui_path in ui_files:
            converter(base_dir, ui_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        convert_ui_to_py(sys.argv[1])
    else:
        convert_ui_to_py()
