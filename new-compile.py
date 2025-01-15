import requests
from bs4 import BeautifulSoup


def crawl_website(url):
    """
    Crawl the website and extract elements with relevant attributes.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        elements = []
        for tag in soup.find_all():
            if tag.get("id"):
                elements.append({"tag": tag.name, "id": tag.get("id")})
            elif tag.get("name"):
                elements.append({"tag": tag.name, "name": tag.get("name")})
            elif tag.get("type"):
                elements.append({"tag": tag.name, "type": tag.get("type")})
        return elements
    except Exception as e:
        print(f"Error crawling the website: {e}")
        return []


def infer_placeholder_data(element):
    """
    Infer realistic placeholder data based on the element's attributes.
    """
    if "id" in element:
        field = element["id"].lower()
    elif "name" in element:
        field = element["name"].lower()
    else:
        field = "unknown"

    # Map field names to sample data
    if "name" in field:
        return "John"
    elif "surname" in field or "last" in field:
        return "Doe"
    elif "email" in field:
        return "johndoe@example.com"
    elif "password" in field:
        return "SecurePassword123!"
    elif "cell" in field or "phone" in field:
        return "0812345678"
    elif "address" in field:
        return "123 Main St"
    elif "id_number" in field or "id" in field:
        return "9001011234567"
    elif "term" in field or "checkbox" in field:
        return "checked"
    elif "number" in field:
        return "4111111111111111"
    else:
        return "Sample Text"


def generate_dynamic_cypress_script(elements, target_url, output_file="cypress_script.cy.js"):
    """
    Generate a realistic Cypress script dynamically based on crawled elements.
    """
    try:
        with open(output_file, "w") as file:
            # Write the test suite structure
            file.write("// Cypress script generated dynamically\n")
            file.write("describe('Dynamic Test Suite', () => {\n\n")
            file.write("  before(() => {\n")
            file.write(f"    // Visit the target application\n")
            file.write(f"    cy.visit('{target_url}');\n")
            file.write("  });\n\n")
            file.write("  it('performs actions on dynamically extracted elements', () => {\n\n")

            # Organize elements by type for a structured test
            for element in elements:
                if "id" in element:
                    selector = f"#{element['id']}"
                elif "name" in element:
                    selector = f"[name='{element['name']}']"
                else:
                    selector = element["tag"]

                # Handle different types of fields
                if element["tag"] in ["input", "textarea"]:
                    placeholder = infer_placeholder_data(element)
                    file.write(f"    cy.get('{selector}').type('{placeholder}', {{ delay: 50 }});\n")
                elif element["tag"] == "select":
                    file.write(f"    cy.get('{selector}').select('Option 1');\n")
                elif element["tag"] == "button" or element["tag"] == "a":
                    file.write(f"    cy.get('{selector}').should('be.visible').click();\n")
                elif element["tag"] == "checkbox" or "checkbox" in element.get("type", ""):
                    file.write(f"    cy.get('{selector}').check();\n")
                else:
                    file.write(f"    cy.get('{selector}').should('be.visible');\n")

            # Final assertion
            file.write("\n    // Verify the URL\n")
            file.write("    cy.url().should('include', '/dashboard');\n")
            file.write("\n  });\n")
            file.write("});\n")

        print(f"Cypress script written to {output_file}")
    except Exception as e:
        print(f"Error generating Cypress script: {e}")


def main():
    """
    Main function to crawl a website and generate a Cypress script.
    """
    target_url = "https://parabank.parasoft.com/parabank/register.htm"
    output_script_file = "cypress/e2e/dynamic_cypress_script.cy.js"

    print(f"Crawling the website: {target_url}...")
    elements = crawl_website(target_url)

    if elements:
        print(f"Found {len(elements)} elements. Generating Cypress script...")
        generate_dynamic_cypress_script(elements, target_url, output_file=output_script_file)
        print(f"Cypress script has been successfully generated: {output_script_file}")
    else:
        print("No elements found or an error occurred during crawling.")


if __name__ == "__main__":
    main()

