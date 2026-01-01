import requests
import sys
import os

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
    Sends a Jinja2 template to Home Assistant to be rendered
    with access to the full state machine.
    """
    # Remove trailing slash from URL if present to prevent double slashes
    base_url = HASS_URL.rstrip('/')
    api_endpoint = f"{base_url}/api/template"

    headers = {
        "Authorization": f"Bearer {HASS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "template": template_str
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        if response is not None:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    # Example 1: Simple state check
    jinja_code = "{{ states('sun.sun') }}"

    # Example 2: Complex logic
    complex_jinja = """
    {% for light in states.light | selectattr('state', 'eq', 'on') | list %}
      - {{ light.name }} is on
    {% else %}
      No lights are on.
    {% endfor %}
    """

    print(f"--- Connecting to {HASS_URL} ---")

    print("\n--- Rendering Simple Template ---")
    print(render_template(jinja_code))

    print("\n--- Rendering Complex Template ---")
    print(render_template(complex_jinja))