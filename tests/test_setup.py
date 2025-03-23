import os
import shutil
import tempfile
import setuptools
import unittest
import importlib.util
import logging

class TestSetupConfiguration(unittest.TestCase):
    def setUp(self):
        self.readme_path = os.path.join(os.getcwd(), "README.md")
        if not os.path.exists(self.readme_path):
            logging.warning("Ensure a README.md exists since setup.py reads it.")
        self.temp_readme = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".md")
        self.temp_readme.write("Test README content")
        self.temp_readme.close()
        shutil.copy(self.temp_readme.name, self.readme_path)

        # Monkeypatch setuptools.setup to capture parameters.
        self.original_setup = setuptools.setup
        self.recorded_kwargs = {}
        def dummy_setup(**kwargs):
            self.recorded_kwargs = kwargs
        setuptools.setup = dummy_setup

    def tearDown(self):
        # Restore setuptools.setup and cleanup temporary files.
        setuptools.setup = self.original_setup
        if os.path.exists(self.readme_path):
            os.remove(self.readme_path)
        if os.path.exists(self.temp_readme.name):
            os.remove(self.temp_readme.name)

    def test_setup_config(self):
        # Execute setup.py from its file location.
        spec = importlib.util.spec_from_file_location("setup", os.path.join(os.getcwd(), "setup.py"))
        setup_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup_module)

        # Validate the configuration parameters.
        self.assertEqual(self.recorded_kwargs.get("name"), "pyAdditel")
        self.assertTrue(self.recorded_kwargs.get("use_scm_version"))
        self.assertEqual(self.recorded_kwargs.get("author"), "Jeff Hall")
        self.assertEqual(self.recorded_kwargs.get("author_email"), "rhythmatician5@gmail.com")
        self.assertEqual(self.recorded_kwargs.get("description"), "A Python SDK to communicate with Additel devices")
        self.assertIn("README", self.recorded_kwargs.get("long_description", ""))
        self.assertEqual(self.recorded_kwargs.get("long_description_content_type"), "text/markdown")
        self.assertIn("github.com", self.recorded_kwargs.get("url", ""))
        self.assertEqual(self.recorded_kwargs.get("python_requires"), ">=3.6")
        self.assertIn("src", self.recorded_kwargs.get("package_dir", {}).values())

if __name__ == '__main__':
    unittest.main()