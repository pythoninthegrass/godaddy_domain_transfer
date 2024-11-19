# godaddy_domain_transfer

## Minimum Requirements

* [Python 3.11+](https://www.python.org/downloads/)
* [poetry](https://python-poetry.org/docs/)

## Recommended Requirements

* [asdf](https://asdf-vm.com/)

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/pythoninthegrass/godaddy_domain_transfer.git
    cd godaddy_domain_transfer
    ```
2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```
3. Create a `.env` file in the root directory and add your GoDaddy API credentials and other necessary configurations:
    ```
    API_KEY=your_api_key
    API_SECRET=your_api_secret
    DOMAIN=your_domain
    NEW_EMAIL=your_new_email
    ```

> [!NOTE]
> `NEW_EMAIL` is optional. Only used if you want to change the email address associated with the domain.

## Usage

1. Run the script:
    ```bash
    poetry shell
    python main.py
    ```
2. Follow the instructions printed in the terminal to complete the domain transfer process.

## Further Reading

* [GoDaddy API Documentation](https://developer.godaddy.com/doc)
* [mintuhouse/godaddy-api](https://github.com/mintuhouse/godaddy-api)
* [Poetry Documentation](https://python-poetry.org/docs/)
* [Requests Library Documentation](https://docs.python-requests.org/en/latest/)
* [Python Decouple Documentation](https://pypi.org/project/python-decouple/)
