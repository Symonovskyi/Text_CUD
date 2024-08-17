from typing import List, Dict, Any
import asyncio
import concurrent.futures
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)


class MarkupModificationError(Exception):
    """
    Custom exception for errors that occur during markup modification.

    Attributes:
    -----------
    message : str
        A description of the error.
    details : str, optional
        Additional details about the error.
    """

    def __init__(self, message="An error occurred in the MarkupModifier", details=None):
        self.message = message
        self.details = details
        super().__init__(f"{self.message}: {self.details}" if details else self.message)
        logging.error(self.message)


class MarkupModifier:
    """
    A class to modify HTML/XML content using BeautifulSoup.

    This class provides various methods to clean, update, or add attributes
    to HTML/XML elements.

    Attributes:
    -----------
    soup : BeautifulSoup
        Parsed HTML/XML content wrapped in a root tag.
    """

    def __init__(self, text: str):
        """
        Initializes the MarkupModifier with the provided text.

        Parameters:
        -----------
        text : str
            The HTML/XML content to be modified.

        Raises:
        -------
        MarkupModificationError
            If there is an error during the initialization or parsing of the text.
        """
        logging.debug("Initializing MarkupModifier")

        try:
            wrapped_text = f"<root>{text}</root>"  # Wrapping the text in a root element for easier parsing
            self.soup = BeautifulSoup(wrapped_text, "html.parser")
            logging.debug(
                "Successful initialization and parsing of the text using BeautifulSoup"
            )
        except Exception as e:
            raise MarkupModificationError(
                "Error during MarkupModifier initialization", details=str(e)
            )

    def remove_style_properties(self, properties: List[str]):
        """
        Removes specified style properties from all elements in the markup.

        Parameters:
        -----------
        properties : List[str]
            A list of CSS properties to be removed from the style attributes.

        Raises:
        -------
        MarkupModificationError
            If the list of properties is empty or an error occurs during property removal.
        """
        logging.debug(f"Removing style properties: {properties}")
        if not properties:
            raise MarkupModificationError(
                "List of properties is empty or None, removal not possible.",
                details="Passed an empty list of properties",
            )

        try:
            for elem in self.soup.find_all(True):
                if elem.has_attr("style"):
                    original_style = elem["style"]
                    logging.debug(f"Original style string: {original_style}")

                    # Filter out the specified properties from the style string
                    updated_style = ";".join(
                        s.strip()
                        for s in original_style.split(";")
                        if not any(s.strip().startswith(prop) for prop in properties)
                    ).strip(";")

                    logging.debug(
                        f"Style string after removing properties: {updated_style}"
                    )

                    if (
                        not updated_style
                    ):
                        del elem["style"]
                    else:
                        elem["style"] = updated_style

            logging.debug("Properties successfully removed")
        except Exception as e:
            raise MarkupModificationError(
                "Error during the removal of style properties", details=str(e)
            )

    def remove_attributes(self, attributes: List[str]):
        """
        Removes specified attributes from all elements in the markup.

        Parameters:
        -----------
        attributes : List[str]
            A list of attributes to be removed.

        Raises:
        -------
        MarkupModificationError
            If the list of attributes is empty or an error occurs during attribute removal.
        """
        logging.debug(f"Removing attributes: {attributes}")
        if not attributes:
            raise MarkupModificationError(
                "List of attributes is empty or None, removal not possible.",
                details="Passed an empty list of attributes",
            )

        try:
            for elem in self.soup.find_all(True):
                for attr in attributes:
                    if elem.has_attr(attr):
                        del elem[attr]
                        logging.debug(f"Attribute {attr} removed from tag {elem.name}")

            logging.debug("Attributes successfully removed")
        except Exception as e:
            raise MarkupModificationError(
                "Error during the removal of attributes", details=str(e)
            )

    def replace_attribute_value(self, attribute: str, old_value: str, new_value: str):
        """
        Replaces a specific value in the given attribute for all elements.

        Parameters:
        -----------
        attribute : str
            The attribute whose value should be replaced.
        old_value : str
            The old value to be replaced.
        new_value : str
            The new value to replace the old value.

        Raises:
        -------
        MarkupModificationError
            If an error occurs during the replacement of attribute values.
        """
        logging.debug(
            f"Starting replace_attribute_value with attribute: {attribute}, old value: {old_value}, new value: {new_value}"
        )

        elements_to_process = self.soup.find_all(attrs={attribute: True})
        logging.debug(
            f"Found {len(elements_to_process)} elements with attribute {attribute}"
        )

        try:
            for elem in elements_to_process:
                current_value = elem.get(attribute)
                logging.debug(
                    f"Current attribute {attribute} value in element: {current_value}"
                )

                if current_value:
                    # Replace the old value with the new value
                    updated_value = current_value.replace(
                        old_value.strip(";"), new_value.strip(";")
                    )
                    if updated_value != current_value:
                        elem[attribute] = updated_value
                        logging.debug(
                            f"Attribute {attribute} updated to: {elem[attribute]}"
                        )

            logging.debug(f"Replacement of attribute {attribute} completed")
        except Exception as e:
            raise MarkupModificationError(
                "Error during attribute value replacement", details=str(e)
            )

    def add_attribute(self, tag: str, attribute: str, value: str):
        """
        Adds a specified attribute with a given value to all elements of a specified tag.

        Parameters:
        -----------
        tag : str
            The tag name of elements to which the attribute should be added.
        attribute : str
            The name of the attribute to add.
        value : str
            The value of the attribute to add.

        Raises:
        -------
        MarkupModificationError
            If an error occurs during the addition of the attribute.
        """
        logging.debug(f"Adding attribute {attribute} with value {value} to tag {tag}")
        try:
            for elem in self.soup.find_all(tag.lower()):
                elem[attribute] = value
                logging.debug(
                    f"Attribute {attribute} added to tag {tag} with value {value}"
                )
            logging.debug("Attribute successfully added")
        except Exception as e:
            raise MarkupModificationError(
                "Error during attribute addition", details=str(e)
            )

    def get_cleaned_text(self) -> str:
        """
        Retrieves the cleaned HTML/XML content as a string.

        Returns:
        --------
        str
            The cleaned HTML/XML content.

        Raises:
        -------
        MarkupModificationError
            If an error occurs while retrieving the cleaned text.
        """
        logging.debug("Getting cleaned text")
        try:
            cleaned_text = (
                self.soup.root.decode_contents()
            )  # Extract the content inside the root tag
            logging.debug(f"Final cleaned text: {cleaned_text}")
            return cleaned_text
        except Exception as e:
            raise MarkupModificationError(
                "Error during retrieval of cleaned text", details=str(e)
            )

    async def apply_rules_async(self, rules: Dict[str, Any]):
        """
        Applies a set of modification rules to the markup asynchronously.

        Parameters:
        -----------
        rules : Dict[str, Any]
            A dictionary defining the modification rules to apply. Supported keys:
            - "remove_attributes": List of attributes to remove.
            - "replace_attributes": List of dictionaries with "attribute", "old_value", and "new_value".
            - "add_attributes": List of dictionaries with "tag", "attribute", and "value".

        Raises:
        -------
        MarkupModificationError
            If an error occurs during asynchronous rule application.
        """
        logging.debug("Applying rules asynchronously")
        loop = asyncio.get_event_loop()

        try:
            # Apply the "remove_attributes" rule asynchronously
            if "remove_attributes" in rules:
                await loop.run_in_executor(
                    None,
                    self.remove_attributes,
                    rules["remove_attributes"][0]["attributes"],
                )

            # Apply the "replace_attributes" rule asynchronously
            if "replace_attributes" in rules:
                for rule in rules["replace_attributes"]:
                    await loop.run_in_executor(
                        None,
                        self.replace_attribute_value,
                        rule["attribute"],
                        rule["old_value"],
                        rule["new_value"],
                    )

            # Apply the "add_attributes" rule asynchronously
            if "add_attributes" in rules:
                for rule in rules["add_attributes"]:
                    await loop.run_in_executor(
                        None,
                        self.add_attribute,
                        rule["tag"],
                        rule["attribute"],
                        rule["value"],
                    )

            logging.debug("Asynchronous rule application completed")
        except Exception as e:
            raise MarkupModificationError(
                "Error during asynchronous rule application", details=str(e)
            )

    def apply_rules(self, rules: Dict[str, Any]):
        """
        Applies a set of modification rules to the markup using a thread pool for parallel processing.

        Parameters:
        -----------
        rules : Dict[str, Any]
            A dictionary defining the modification rules to apply. Supported keys:
            - "remove_attributes": List of attributes to remove.
            - "replace_attributes": List of dictionaries with "attribute", "old_value", and "new_value".
            - "add_attributes": List of dictionaries with "tag", "attribute", and "value".

        Raises:
        -------
        MarkupModificationError
            If an error occurs during the rule application.
        """
        logging.debug(f"Applying rules: {rules}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            try:
                # Submit tasks to the thread pool for each type of rule
                if "remove_attributes" in rules:
                    futures.append(
                        executor.submit(
                            self.remove_attributes,
                            rules["remove_attributes"][0]["attributes"],
                        )
                    )

                if "replace_attributes" in rules:
                    for rule in rules["replace_attributes"]:
                        futures.append(
                            executor.submit(
                                self.replace_attribute_value,
                                rule["attribute"],
                                rule["old_value"],
                                rule["new_value"],
                            )
                        )

                if "add_attributes" in rules:
                    for rule in rules["add_attributes"]:
                        futures.append(
                            executor.submit(
                                self.add_attribute,
                                rule["tag"],
                                rule["attribute"],
                                rule["value"],
                            )
                        )

                # Wait for all tasks to complete
                for future in concurrent.futures.as_completed(futures):
                    future.result()

                logging.debug("Rules successfully applied")
            except Exception as e:
                raise MarkupModificationError(
                    "Error during rule application", details=str(e)
                )
