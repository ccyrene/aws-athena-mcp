# AWS Athena MCP Server

A Model Context Protocol (MCP) server for AWS Athena that enables SQL queries and database exploration through a standardized interface.

## 🏗️ Project Structure

The project follows best practices for Python project organization:

```
aws-athena-mcp/
├── src/
│   └── athena_mcp/
│       ├── core/                 # Core system modules
│       │   ├── config.py        # Centralized configurations
│       │   ├── exceptions.py    # Custom exceptions
│       │   └── __init__.py
│       ├── services/            # Business services
│       │   ├── athena_client.py # Athena client factory and management
│       │   ├── athena_service.py # Main Athena operations
│       │   └── __init__.py
│       ├── utils/               # Utilities and helpers
│       │   ├── formatters.py    # Output formatters
│       │   ├── helpers.py       # Helper functions
│       │   ├── validators.py    # Validators
│       │   └── __init__.py
│       ├── handlers/            # MCP handlers
│       │   ├── tool_handlers.py # MCP tool handlers
│       │   └── __init__.py
│       ├── server.py            # Main MCP server
│       └── __init__.py
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── __init__.py
├── main.py                      # Main entry point
├── setup.py                     # Installation configuration
├── pyproject.toml              # Development tools configuration
├── requirements.txt            # Dependencies
└── README.md
```

## 🚀 Features

- **Modular Architecture**: Code organized in well-defined modules following single responsibility principle
- **Complete Type Hints**: Static typing for better maintainability
- **Robust Error Handling**: Custom exceptions and proper error handling
- **Centralized Configuration**: All configurations in a single location
- **Tests Included**: Unit and integration test structure
- **Structured Logging**: Configurable logging system
- **Input Validation**: Validators for different data types

## 🔌 MCP Configuration

To use this server in MCP clients like Cursor, add the following configuration to your `mcp.json` file:

```json
{
  "mcpServers": {
    "athena-connector": {
      "command": "python3",
      "args": ["/path/to/aws-athena-mcp/main.py"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your-access-key",
        "AWS_SECRET_ACCESS_KEY": "your-secret-key",
        "AWS_ATHENA_WORKGROUP": "your-workgroup",
        "AWS_REGION": "us-east-1",
        "AWS_S3_OUTPUT_LOCATION": "s3://your-bucket/athena-results/"
      }
    }
  }
}
```

### Configuration Options

#### Using Direct Credentials:
```json
{
  "command": "python3",
  "args": ["/path/to/aws-athena-mcp/main.py"],
  "env": {
    "AWS_ACCESS_KEY_ID": "AKIA...",
    "AWS_SECRET_ACCESS_KEY": "your-secret-key",
    "AWS_ATHENA_WORKGROUP": "your-workgroup",
    "AWS_REGION": "us-east-1",
    "AWS_S3_OUTPUT_LOCATION": "s3://your-bucket/results/"
  }
}
```

#### Using AWS Profile:
```json
{
  "command": "python3",
  "args": ["/path/to/aws-athena-mcp/main.py"],
  "env": {
    "AWS_PROFILE": "your-aws-profile",
    "AWS_REGION": "us-east-1",
    "AWS_ATHENA_WORKGROUP": "your-workgroup",
    "AWS_S3_OUTPUT_LOCATION": "s3://your-bucket/results/"
  }
}
```

#### Using System Default Credentials:
```json
{
  "command": "python3",
  "args": ["/path/to/aws-athena-mcp/main.py"],
  "env": {
    "AWS_S3_OUTPUT_LOCATION": "s3://your-bucket/results/"
  }
}
```

### Required Environment Variables

- **AWS_S3_OUTPUT_LOCATION**: S3 location where query results will be stored

### Optional Environment Variables

- **AWS_ACCESS_KEY_ID**: AWS access key (if not using profile)
- **AWS_SECRET_ACCESS_KEY**: AWS secret key (if not using profile)
- **AWS_PROFILE**: Locally configured AWS profile
- **AWS_ATHENA_WORKGROUP**: Athena workgroup (default: primary)
- **AWS_REGION** or **AWS_DEFAULT_REGION**: AWS region (default: us-east-1)
- **LOG_LEVEL**: Logging level (DEBUG, INFO, WARNING, ERROR)

> **⚠️ Security**: For production environments, we recommend using IAM roles or AWS profiles instead of direct credentials in the configuration file.

## 📦 Installation

### Development Installation

```bash
# Clone the repository
git clone <repository-url>
cd aws-athena-mcp

# Install in development mode
pip install -e .[dev]
```

### Production Installation

```bash
pip install .
```

## ⚙️ Configuration

Configure the following environment variables:

```bash
# AWS credentials (optional if using profile)
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"

# AWS athena workgroup
export AWS_ATHENA_WORKGROUP="your-workgroup"

# AWS region
export AWS_DEFAULT_REGION="us-east-1"

# Or use an AWS profile
export AWS_PROFILE="your-profile"

# S3 output location (required)
export AWS_S3_OUTPUT_LOCATION="s3://your-bucket/athena-results/"
```

## 🎯 Usage

### Run the Server

```bash
# Using the main entry point
python main.py

# Or using the installed command
athena-mcp
```

### Available Tools

1. **list_databases**: Lists all available databases in Athena
2. **query_athena**: Executes SQL queries in Athena
3. **describe_data_structure**: Describes the structure of a database

## 🧪 Testing

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=src/athena_mcp

# Run specific tests
pytest tests/unit/test_validators.py -v
```

## 🛠️ Development

### Code Quality Tools

```bash
# Code formatting
black src/ tests/

# Import sorting
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

### Development Environment Setup

```bash
# Install development dependencies
pip install -e .[dev]

# Or install manually
pip install pytest pytest-asyncio black isort flake8 mypy
```

## 📋 Implemented Best Practices

### Architecture

- **Separation of Concerns**: Each module has a specific responsibility
- **Dependency Inversion**: Use of interfaces and dependency injection
- **Single Responsibility Principle**: Classes and functions with single purpose
- **Factory Pattern**: For AWS client creation
- **Strategy Pattern**: For different types of formatting and validation

### Code Quality

- **Type Hints**: Static typing in all functions and methods
- **Docstrings**: Complete documentation in Google Style format
- **Error Handling**: Custom exceptions and proper handling
- **Logging**: Structured and configurable logging system
- **Validation**: Rigorous input validation

### Project Structure

- **src/ Layout**: Clear separation between source code and other files
- **Namespace Packages**: Hierarchical organization of modules
- **Test Structure**: Tests organized mirroring code structure
- **Configuration Files**: Centralized and externalized configuration

## 🔧 Troubleshooting

Consult the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file for common issues and solutions.

## 📝 Module Structure

### Core (`src/athena_mcp/core/`)
- **config.py**: Centralized system configurations
- **exceptions.py**: Custom domain exceptions

### Services (`src/athena_mcp/services/`)
- **athena_client.py**: AWS Athena client factory and management
- **athena_service.py**: High-level services for Athena operations

### Utils (`src/athena_mcp/utils/`)
- **formatters.py**: Formatters for different output types
- **helpers.py**: General helper functions and utilities
- **validators.py**: Validators for different input types

### Handlers (`src/athena_mcp/handlers/`)
- **tool_handlers.py**: Handlers for MCP tools

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
