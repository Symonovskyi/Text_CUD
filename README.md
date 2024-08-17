# Text_CUD

## Description

This Python module makes it easy to modify XML/HTML content. Whether you're cleaning up, updating, or adding attributes to your markup, this tool is here to help.

<img src="https://raw.githubusercontent.com/Symonovskyi/Symonovskyi/main/src/projects/Text_CUD/Text_CUD-background.webp" alt="background">

## Features

Key features include:

- **Create (Add Attributes)**: Easily add new attributes to your elements.
- **Update (Replace Attribute Values)**: Quickly change existing attribute values as needed.
- **Delete (Remove Attributes)**: Remove unwanted attributes from your markup with ease.
- **Asynchronous Support**: Handles asynchronous operations smoothly, perfect for high-performance tasks.
- **Thread-Safe**: Works well in multithreaded environments, making it reliable for large datasets.

### When to Use It

This tool is especially useful in scenarios like:

- **Markup Cleanup**: Automatically remove unnecessary or problematic attributes from your HTML/XML before processing or rendering.
- **Dynamic Content Updates**: Easily adjust styles or add custom data attributes in your web apps.
- **Batch Content Processing**: Efficiently modify attributes across large sets of XML/HTML files, ideal for bulk processing or content migration.
- **Rendering Preparation**: Prepare your content for different rendering engines or platforms by fine-tuning attributes.

---

### Installation

To get started, you can install the module directly from GitHub. Just follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/Symonovskyi/Text_CUD.git
    cd Text_CUD
    ```

2. Install the dependencies and the package. You have two options:

   - **Install dependencies directly:**

     ```bash
     pip install beautifulsoup4
     ```

   - **Or install everything using the requirements file:**

     ```bash
     pip install -r requirements.txt
     ```

### Requirements

- **Python**: Version 3.6 or later
- **Dependencies**: `beautifulsoup4` is the main requirement.

---

## Testing Instructions

Testing is simple. Follow these steps to make sure everything works:

1. Ensure all dependencies are installed, including `beautifulsoup4` and `unittest` (unittest is included with Python).
2. Navigate to the directory where test files are located.
3. Run the tests:

    - **To run all tests:**

      ```bash
      python -m unittest discover
      ```

    - **To run a specific test file:**

      ```bash
      python -m unittest test_markup_modifier.py
      ```

Make sure everything passes before using the module in your projects!

---

## Usage Examples

### 1. Remove Attributes

Easily remove unwanted attributes from your XML/HTML content.

**Input:**

```html
<img src="image.png" alt="An image" width="500" height="300" />
```

**Output:**

```html
<img src="image.png" alt="An image" />
```

**Code:**

```python
content = '<img src="image.png" alt="An image" width="500" height="300" />'

rules = {
    "remove_attributes": [
        {"attributes": ["width", "height"]}
    ]
}

cleaner = MarkupModifier(content)
cleaner.apply_rules(rules)
result = cleaner.get_cleaned_text()
```

---

### 2. Replace Attribute Values

Replace specific attribute values while preserving the rest of the content.

**Input:**

```html
<span style="font-size: 12px; color: red;">Hello</span>
```

**Output:**

```html
<span style="font-size: 12px; color: green;">Hello</span>
```

**Code:**

```python
content = '<span style="font-size: 12px; color: red;">Hello</span>'

rules = {
    "replace_attributes": [
        {"attribute": "style", "old_value": "color: red;", "new_value": "color: green;"}
    ]
}

cleaner = MarkupModifier(content)
cleaner.apply_rules(rules)
result = cleaner.get_cleaned_text()
```

---

### 3. Add Attributes

Add new attributes to specified elements, enhancing their functionality.

**Input:**

```html
<a href="https://example.com">Click Here</a>
```

**Output:**

```html
<a href="https://example.com" target="_blank">Click Here</a>
```

**Code:**

```python
content = '<a href="https://example.com">Click Here</a>'

rules = {
    "add_attributes": [
        {"tag": "a", "attribute": "target", "value": "_blank"}
    ]
}

cleaner = MarkupModifier(content)
cleaner.apply_rules(rules)
result = cleaner.get_cleaned_text()
```

---

### 4. Combine Multiple Operations

Apply multiple operations in one pass to streamline your XML/HTML processing.

**Input:**

```html
<p class="text" style="color: black;" id="intro">Hello, World!</p>
```

**Output:**

```html
<p class="text" style="color: gray;" data-type="intro-text">Hello, World!</p>
```

**Code:**

```python
content = '<p class="text" style="color: black;" id="intro">Hello, World!</p>'

rules = {
    "remove_attributes": [
        {"attributes": ["id"]}
    ],
    "replace_attributes": [
        {"attribute": "style", "old_value": "color: black;", "new_value": "color: gray;"}
    ],
    "add_attributes": [
        {"tag": "p", "attribute": "data-type", "value": "intro-text"}
    ]
}

cleaner = MarkupModifier(content)
cleaner.apply_rules(rules)
result = cleaner.get_cleaned_text()
```

---

## When to Use

Text_CUD is ideal in situations where you need to:

- **Clean Up Markup**: Remove unnecessary attributes from your XML/HTML to streamline your content.
- **Customize Content**: Dynamically adjust attributes to match design or functional requirements.
- **Prepare for Processing**: Modify attributes to get your content ready for rendering or further processing.

Whether you’re fine-tuning styles, cleaning up data, or adding new attributes, this tool offers a straightforward solution for managing XML/HTML content.

---

## Licensing

This project is distributed under a dual license: [MIT License](./LICENSE_MIT) and [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE_CC_BY_4.0).

### What does this mean for you?

When you use this project, we just ask that you follow a few simple rules:

1. **Give Credit**: Please make sure to give proper credit to the authors of this project. This can be as simple as including a notice in your documentation or about page, linking back to the original project.
2. **Share Any Changes**: If you make any modifications, let others know by mentioning that changes were made. This helps keep things transparent and benefits the community.
3. **Keep These Licenses with the Project**: When you share or distribute this project, just make sure that both license files stay with it. That’s all! This ensures that everyone knows the rules, just like you do.

We’re excited to see what you create with this project! Thank you for following these simple guidelines and helping keep the spirit of open source alive and well.

