import sys
import os

# Adding the project's root directory to sys.path to enable module imports.
# This allows the test suite and other scripts to import modules from the
# project's root directory without needing to manually adjust the Python environment.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now, we can work within the project's context and import the necessary modules.

import logging
from text_cud.markup_modifier import MarkupModifier, MarkupModificationError

# Set up basic logging configuration.
# This will configure the logging system to output messages to the console with a level of INFO or higher.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Demonstrates the combined usage of the Text_CUD tool:
    simultaneous removal, replacement, and addition of attributes
    in XML/HTML content.

    The function performs the following operations on the content:
    - Removes the "data-id" attribute from the <div> tag.
    - Replaces the "color: red;" style with "color: blue;" in the <div> tag.
    - Adds a new attribute "data-processed=true" to the <div> tag.

    If any errors occur during processing, they will be caught and logged.
    """

    # The original XML/HTML content to be modified.
    content = '<div class="header" style="color: red;" data-id="123">Welcome</div>'
    logger.info("Исходное содержимое:\n%s", content)

    # Rules for content modification.
    rules = {
        "remove_attributes": [
            {"attributes": ["data-id"]}
        ],  # Removing the "data-id" attribute.
        "replace_attributes": [
            {
                "attribute": "style",
                "old_value": "color: red;",  # Replacing "color: red;" with "color: blue;" in the style attribute.
                "new_value": "color: blue;",
            }
        ],
        "add_attributes": [
            {
                "tag": "div",
                "attribute": "data-processed",
                "value": "true",
            }  # Adding a new attribute "data-processed=true" to the <div> tag.
        ],
    }

    try:
        # Initialize the MarkupModifier with the content.
        cleaner = MarkupModifier(content)

        # Apply the modification rules to the content.
        cleaner.apply_rules(rules)

        # Get the modified content as a string.
        result = cleaner.get_cleaned_text()
        logger.info("Модифицированное содержимое:\n%s", result)

    except MarkupModificationError as e:
        # Log the specific markup modification error.
        logger.error("Ошибка обработки контента: %s", e)
    except Exception as e:
        # Log any unexpected errors.
        logger.error("Неожиданная ошибка: %s", e)


if __name__ == "__main__":
    # Run the main function if the script is executed directly.
    main()
