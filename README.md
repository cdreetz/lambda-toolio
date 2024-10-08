# Lambda Cloud Client

Lambda Cloud Client is a Python package that provides an easy-to-use interface for interacting with the Lambda Cloud API. It allows users to manage instances, SSH keys, and run ML scripts on Lambda Cloud instances.

## Features

- Check available instance types
- Launch instances
- Manage SSH keys
- Run ML scripts on remote instances
- Terminate instances
- Interactive assistant for easy usage

## Installation

You can install the Lambda Cloud Client directly from GitHub using pip:

```
pip install git+https://github.com/cdreetz/lambda-toolio.git
```

Or using Poetry:

```
poetry add git+https://github.com/cdreetz/lambda-toolio.git
```

## Usage

To use the Lambda Cloud Client as a Python module:

```python
from lambda_toolio import LambdaToolio

client = LambdaToolio()
client.interactive_assistant()
```

To use the Lambda Cloud Client as a command-line tool:

```
lambda-toolio
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/cdreetz/lambda-toolio).

## License

The Lambda Cloud Client is licensed under the [MIT License](LICENSE).