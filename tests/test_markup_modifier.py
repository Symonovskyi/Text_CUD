import sys
import os

# Adding the project's root directory to sys.path to enable module imports.
# This allows the test suite to import modules from the project's root directory,
# ensuring that the tests can be executed without needing to manually adjust the Python environment.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now, we can work within the project's context and import the necessary modules.

import unittest
import time
import asyncio
import concurrent.futures

from text_cud.markup_modifier import MarkupModifier


def timed_test(func):
    """
    A decorator to measure the execution time of a test function.

    Parameters:
    -----------
    func : function
        The test function to be timed.

    Returns:
    --------
    function
        The wrapped function that includes timing logic.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        print(f"{func.__name__} took {duration:.4f} seconds")
        return result

    return wrapper


class TestMarkupModifierBase(unittest.TestCase):
    """
    Base test class for setting up initial test data and common utilities.

    This class provides common setup and utility methods that can be used
    by other test classes to avoid code duplication.
    """

    def setUp(self):
        """
        Set up the initial HTML/XML content to be used in the tests.

        The `self.text` attribute contains a sample XML/HTML string
        that will be modified by the tests.
        """
        self.text = (
            "<root>"
            '<element id="1" style="color:red; border:1px solid black; background-color:yellow;" attribute="value"/>'
            "</root>"
        )

    def apply_rules(self, cleaner, rules):
        """
        Apply modification rules using the provided MarkupModifier instance.

        Parameters:
        -----------
        cleaner : MarkupModifier
            The MarkupModifier instance used to modify the content.
        rules : dict
            A dictionary defining the modification rules to apply.
        """
        cleaner.apply_rules(rules)


class TestMarkupModifier(unittest.TestCase):
    """
    Test suite for verifying the functionality of MarkupModifier with valid inputs.

    This class includes tests for different operations such as removing attributes,
    replacing attribute values, and adding new attributes to elements.
    """

    def setUp(self):
        """
        Set up the test environment by initializing the base test setup.

        This method initializes the base test class and prepares the test data
        for each individual test case.
        """
        self.base_test = TestMarkupModifierBase()
        self.base_test.setUp()

    def run_test(self, rules, expected_in, expected_not_in=None):
        """
        Run a generic test with the provided rules and assertions.

        Parameters:
        -----------
        rules : dict
            A dictionary defining the modification rules to apply.
        expected_in : str
            The string that is expected to be present in the modified content.
        expected_not_in : str, optional
            The string that is expected to be absent in the modified content.
        """
        with self.subTest(rules=rules):
            cleaner = MarkupModifier(self.base_test.text)
            self.base_test.apply_rules(cleaner, rules)
            cleaned_text = cleaner.get_cleaned_text()
            self.assertIn(expected_in, cleaned_text)
            if expected_not_in:
                self.assertNotIn(expected_not_in, cleaned_text)

    @timed_test
    def test_remove_style_attribute(self):
        """
        Test the removal of the 'style' attribute from all elements.

        This test verifies that the 'style' attribute is correctly removed
        from the content, and that the resulting content is as expected.
        """
        rules = {"remove_attributes": [{"attributes": ["style"]}]}

        cleaner = MarkupModifier(self.base_test.text)
        self.base_test.apply_rules(cleaner, rules)
        cleaned_text = cleaner.get_cleaned_text()
        self.assertIn('<element attribute="value" id="1"></element>', cleaned_text)
        self.assertNotIn("style", cleaned_text)

    @timed_test
    def test_replace_attribute_value(self):
        """
        Test the replacement of a specific attribute value within the 'style' attribute.

        This test verifies that the 'color:red' style is correctly replaced with 'color:green'
        in the content, and that the original value is no longer present.
        """
        rules = {
            "replace_attributes": [
                {
                    "attribute": "style",
                    "old_value": "color:red",
                    "new_value": "color:green",
                }
            ]
        }
        self.run_test(rules, expected_in="color:green", expected_not_in="color:red")

    @timed_test
    def test_add_new_attribute(self):
        """
        Test the addition of a new attribute to all 'element' tags.

        This test verifies that the new attribute 'data-new="new_value"' is correctly
        added to all 'element' tags in the content.
        """
        rules = {
            "add_attributes": [
                {"tag": "element", "attribute": "data-new", "value": "new_value"}
            ]
        }
        self.run_test(rules, expected_in='data-new="new_value"')


class TestMarkupModifierAsync(TestMarkupModifier):
    """
    Test suite for verifying the asynchronous functionality of MarkupModifier with valid inputs.

    This class includes asynchronous versions of the tests defined in the base TestMarkupModifier class.
    """

    async def apply_rules_async(self, cleaner, rules):
        """
        Apply modification rules asynchronously using the provided MarkupModifier instance.

        Parameters:
        -----------
        cleaner : MarkupModifier
            The MarkupModifier instance used to modify the content.
        rules : dict
            A dictionary defining the modification rules to apply.
        """
        await cleaner.apply_rules_async(rules)

    def run_test_async(self, rules, expected_in, expected_not_in=None):
        """
        Run a generic asynchronous test with the provided rules and assertions.

        Parameters:
        -----------
        rules : dict
            A dictionary defining the modification rules to apply.
        expected_in : str
            The string that is expected to be present in the modified content.
        expected_not_in : str, optional
            The string that is expected to be absent in the modified content.
        """
        with self.subTest(rules=rules):
            cleaner = MarkupModifier(self.base_test.text)
            asyncio.run(self.apply_rules_async(cleaner, rules))
            cleaned_text = cleaner.get_cleaned_text()
            self.assertIn(expected_in, cleaned_text)
            if expected_not_in:
                self.assertNotIn(expected_not_in, cleaned_text)

    @timed_test
    def test_remove_style_attribute(self):
        """
        Asynchronously test the removal of the 'style' attribute from all elements.

        This test verifies that the 'style' attribute is correctly removed from the content
        in an asynchronous context.
        """
        rules = {"remove_attributes": [{"attributes": ["style"]}]}

        cleaner = MarkupModifier(self.base_test.text)
        asyncio.run(self.apply_rules_async(cleaner, rules))
        cleaned_text = cleaner.get_cleaned_text()
        self.assertIn('<element attribute="value" id="1"></element>', cleaned_text)
        self.assertNotIn("style", cleaned_text)

    @timed_test
    def test_replace_attribute_value(self):
        """
        Asynchronously test the replacement of a specific attribute value within the 'style' attribute.

        This test verifies that the 'color:red' style is correctly replaced with 'color:green'
        in the content in an asynchronous context.
        """
        rules = {
            "replace_attributes": [
                {
                    "attribute": "style",
                    "old_value": "color:red",
                    "new_value": "color:green",
                }
            ]
        }
        self.run_test_async(
            rules, expected_in="color:green", expected_not_in="color:red"
        )

    @timed_test
    def test_add_new_attribute(self):
        """
        Asynchronously test the addition of a new attribute to all 'element' tags.

        This test verifies that the new attribute 'data-new="new_value"' is correctly
        added to all 'element' tags in the content in an asynchronous context.
        """
        rules = {
            "add_attributes": [
                {"tag": "element", "attribute": "data-new", "value": "new_value"}
            ]
        }
        self.run_test_async(rules, expected_in='data-new="new_value"')


class TestMarkupModifierThreaded(TestMarkupModifier):
    """
    Test suite for verifying the multithreaded functionality of MarkupModifier with valid inputs.

    This class includes multithreaded versions of the tests defined in the base TestMarkupModifier class.
    """

    def apply_rules_threaded(self, cleaner, rules):
        """
        Apply modification rules using multiple threads via a ThreadPoolExecutor.

        Parameters:
        -----------
        cleaner : MarkupModifier
            The MarkupModifier instance used to modify the content.
        rules : dict
            A dictionary defining the modification rules to apply.

        Returns:
        --------
        Any
            The result of the thread execution.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(cleaner.apply_rules, rules)
            return future.result()

    def run_test_threaded(self, rules, expected_in, expected_not_in=None):
        """
        Run a generic multithreaded test with the provided rules and assertions.

        Parameters:
        -----------
        rules : dict
            A dictionary defining the modification rules to apply.
        expected_in : str
            The string that is expected to be present in the modified content.
        expected_not_in : str, optional
            The string that is expected to be absent in the modified content.
        """
        with self.subTest(rules=rules):
            cleaner = MarkupModifier(self.base_test.text)
            self.apply_rules_threaded(cleaner, rules)
            cleaned_text = cleaner.get_cleaned_text()
            self.assertIn(expected_in, cleaned_text)
            if expected_not_in:
                self.assertNotIn(expected_not_in, cleaned_text)

    @timed_test
    def test_remove_style_attribute(self):
        """
        Multithreaded test for removing the 'style' attribute from all elements.

        This test verifies that the 'style' attribute is correctly removed from the content
        in a multithreaded context.
        """
        rules = {"remove_attributes": [{"attributes": ["style"]}]}

        cleaner = MarkupModifier(self.base_test.text)
        self.apply_rules_threaded(cleaner, rules)
        cleaned_text = cleaner.get_cleaned_text()
        self.assertIn('<element attribute="value" id="1"></element>', cleaned_text)
        self.assertNotIn("style", cleaned_text)

    @timed_test
    def test_replace_attribute_value(self):
        """
        Multithreaded test for replacing a specific attribute value within the 'style' attribute.

        This test verifies that the 'color:red' style is correctly replaced with 'color:green'
        in the content in a multithreaded context.
        """
        rules = {
            "replace_attributes": [
                {
                    "attribute": "style",
                    "old_value": "color:red",
                    "new_value": "color:green",
                }
            ]
        }
        self.run_test_threaded(
            rules, expected_in="color:green", expected_not_in="color:red"
        )

    @timed_test
    def test_add_new_attribute(self):
        """
        Multithreaded test for adding a new attribute to all 'element' tags.

        This test verifies that the new attribute 'data-new="new_value"' is correctly
        added to all 'element' tags in the content in a multithreaded context.
        """
        rules = {
            "add_attributes": [
                {"tag": "element", "attribute": "data-new", "value": "new_value"}
            ]
        }
        self.run_test_threaded(rules, expected_in='data-new="new_value"')


if __name__ == "__main__":
    # Run all the defined tests when the script is executed directly.
    unittest.main()
