# Online Product Stock Check

This package serves as a template that handles the initialization and operations related to online stock and price checking for <ins>nVidia GeForce RTX 5070 TI</ins> stock in some Spanish retailers. It fetches product data from various URLs, parses the content, and displays the formatted results in the terminal.

The main repo contains this initial example; branches will be used to create specific product and country needs.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Taz5150/online-product-stock-check.git
    ```
2. Navigate to the project directory:
    ```sh
    cd online-product-stock-check
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start the application, run the `__main__.py` script:

```sh
python src/__main__.py
```

## Modules

### `__main__.py`

Main entry point for the online product stock check application. This script initializes the product check module and starts the application.

### `product_check.py`

Handles the initialization and operations related to product stock checking. It fetches product data from various URLs, parses the content, and displays the formatted results.

#### Classes

- `bcolors`: A class for terminal text coloring.

#### Functions

- `fetch(url)`: Fetch the content of the given URL.
- `crawl(parsers, url_type)`: Crawl the URLs and parse the content.
- `main()`: Main function to start the crawling process.
- `init()`: Initialize the product check module.

## Contributing

Contributions are welcome! Please read the contributing guidelines first.

## License

This project is licensed under the MIT License. See the LICENSE file for details.