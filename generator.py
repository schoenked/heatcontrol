import requests
import sys
import os
import glob

# Configuration: File paths
URL_FILE = "hass_url.local"
TOKEN_FILE = "hass_token.local"

def read_config_file(filename):
    """Reads a single line from a file and strips whitespace."""
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        sys.exit(1)

# Load configuration
HASS_URL = read_config_file(URL_FILE)
HASS_TOKEN = read_config_file(TOKEN_FILE)

def render_template(template_str):
    """
    Sends a Jinja2 template to Home Assistant to be rendered.
    """
    base_url = HASS_URL.rstrip('/')
    api_endpoint = f"{base_url}/api/template"

    headers = {
        "Authorization": f"Bearer {HASS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {"template": template_str}

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"  [API Error] HTTP Error: {err}")
    except Exception as e:
        print(f"  [API Error] Request Failed: {e}")
    return None

def process_jinja_files():
    """Finds all .jinja files, renders them, removes empty lines, and writes to .yaml."""
    jinja_files = glob.glob("*.jinja")

    if not jinja_files:
        print("No *.jinja files found in the current directory.")
        return

    print(f"Found {len(jinja_files)} jinja file(s). Processing...\n")

    for input_file in jinja_files:
        # Determine output filename (example.jinja -> example.yaml)
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.yaml"

        print(f"Processing '{input_file}' -> '{output_file}'...")

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                template_content = f.read()

            rendered_content = render_template(template_content)

            if rendered_content is not None:
                # Remove empty lines (including lines that are just whitespace)
                lines = rendered_content.splitlines()
                non_empty_lines = [line for line in lines if line.strip()]
                final_content = "\n".join(non_empty_lines)

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(final_content)
                    # Add a trailing newline for valid POSIX file standards
                    f.write("\n")
                print("  Success.")
            else:
                print("  Skipped writing file due to render error.")

        except Exception as e:
            print(f"  [File Error] Could not process file: {e}")

if __name__ == "__main__":
    print(f"--- Connected to {HASS_URL} ---")
    process_jinja_files()