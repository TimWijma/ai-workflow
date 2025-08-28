# AI Workflow Builder

This project is a full-stack AI workflow builder that allows users to create, save, and run workflows using a visual interface.

## Features

- **Visual Workflow Editor:** Create and manage workflows by dragging and dropping steps.
- **Customizable Steps:** Configure each step with specific parameters.
- **Save and Load:** Save your workflows to the database and load them back into the editor.
- **Execution Engine:** Run your workflows and get the results.

## Tech Stack

- **Frontend:** Vue 3, Vue Flow, PrimeVue
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** PostgreSQL

## Project Setup

### Backend

1.  Navigate to the `backend` directory:
    ```sh
    cd backend
    ```

2.  Create a Python virtual environment:
    ```sh
    python -m venv venv
    ```

3.  Activate the virtual environment:
    -   On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4.  Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5.  Create a `.env` file in the `backend` directory and add the following line with your PostgreSQL connection string:
    ```
    DATABASE_URL=postgresql://user:password@localhost/ai_workflow_db
    ```

6.  Start the backend server:
    ```sh
    uvicorn app.main:app --reload
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```

2.  Install the required dependencies:
    ```sh
    npm install
    ```

3.  Start the frontend development server:
    ```sh
    npm run dev
    ```
