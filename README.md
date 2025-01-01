# Project Deployment Guide

This guide provides instructions on how to deploy the `dicoding-ds-analyst` project.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.11 or later
- You have a virtual environment tool (e.g., `venv`, `virtualenv`)
- You have installed necessary dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ikrar557/dicoding-ds-analyst.git
    ```
2. Navigate to the project directory:
    ```sh
    cd dicoding-ds-analyst
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Deployment

To deploy this project using Streamlit, follow these steps:

1. Run the application:
    ```sh
    streamlit run dashboard/dashboard.py
    ```
2. By default you can access your streamlit project at
   `http://localhost:8501`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

If you have any questions, please contact [ikrarb95@gmail.comm](mailto:ikrarb95@gmail.comm).
