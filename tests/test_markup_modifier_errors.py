import sys
import os

# Adding the project's root directory to sys.path to enable module imports.
# This allows the test suite to import modules from the project's root directory,
# ensuring that the tests can be executed without needing to manually adjust the Python environment.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now, we can work within the project's context and import the necessary modules.

import unittest
import asyncio
import concurrent.futures

from text_cud.markup_modifier import MarkupModifier, MarkupModificationError


class TestMarkupModificationErrors(unittest.TestCase):
    """
    Test suite for verifying error handling in the MarkupModifier class.

    This class tests how the MarkupModifier handles invalid inputs and ensures that
    appropriate exceptions are raised.
    """

    def setUp(self):
        """
        Set up the initial HTML/XML content to be used in the tests.

        The `self.text` attribute contains a sample XML/HTML string
        that will be used in tests that verify error handling.
        """
        self.text = (
            "<root>"
            '<element id="1" style="color:blue; border:1px solid black;" background-color:yellow; attribute="value"/>'
            "</root>"
        )

    def run_error_test(self, rules):
        """
        Run a test that expects a MarkupModificationError to be raised.

        Parameters:
        -----------
        rules : dict
            A dictionary defining the modification rules to apply.
        """
        cleaner = MarkupModifier(self.text)
        with self.assertRaises(MarkupModificationError):
            cleaner.apply_rules(rules)

    def test_invalid_remove_attributes(self):
        """
        Tests error handling when 'remove_attributes' contains an invalid value.

        This test verifies that the MarkupModifier correctly raises a MarkupModificationError
        when 'remove_attributes' is provided with a None value instead of a valid list.
        """
        rules = {"remove_attributes": [{"attributes": None}]}
        self.run_error_test(rules)


class TestMarkupModifierAsyncErrors(TestMarkupModificationErrors):
    """
    Test suite for verifying error handling in asynchronous MarkupModifier.

    This class extends TestMarkupModificationErrors to provide asynchronous tests
    for error handling in the MarkupModifier.
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

    def run_error_test_async(self, rules):
        """
        Run an asynchronous test that expects a MarkupModificationError to be raised.

        Parameters:
        -----------
        rules : dict
            A dictionary defining the modification rules to apply.
        """
        cleaner = MarkupModifier(self.text)
        with self.assertRaises(MarkupModificationError):
            asyncio.run(self.apply_rules_async(cleaner, rules))

    def test_invalid_remove_attributes(self):
        """
        Asynchronously tests error handling when 'remove_attributes' contains an invalid value.

        This test verifies that the MarkupModifier correctly raises a MarkupModificationError
        when 'remove_attributes' is provided with a None value instead of a valid list in an asynchronous context.
        """
        rules = {"remove_attributes": [{"attributes": None}]}
        self.run_error_test_async(rules)


class TestMarkupModifierThreadedErrors(TestMarkupModificationErrors):
    """
    Test suite for verifying error handling in multithreaded MarkupModifier.

    This class extends TestMarkupModificationErrors to provide multithreaded tests
    for error handling in the MarkupModifier.
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

    def run_error_test_threaded(self, rules):
        """
        Run a multithreaded test that expects a MarkupModificationError to be raised.

        Parameters:
        -----------
        rules : dict
            A dictionary defining the modification rules to apply.
        """
        cleaner = MarkupModifier(self.text)
        with self.assertRaises(MarkupModificationError):
            self.apply_rules_threaded(cleaner, rules)

    def test_invalid_remove_attributes(self):
        """
        Tests error handling when 'remove_attributes' contains an invalid value in multithreaded mode.

        This test verifies that the MarkupModifier correctly raises a MarkupModificationError
        when 'remove_attributes' is provided with a None value instead of a valid list in a multithreaded context.
        """
        rules = {"remove_attributes": [{"attributes": None}]}
        self.run_error_test_threaded(rules)


if __name__ == "__main__":
    # Run all the defined tests when the script is executed directly.
    unittest.main()
