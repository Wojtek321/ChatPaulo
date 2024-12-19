# ChatPaulo

Welcome to ChatPaulo, an AI-powered assistant designed to help customers interact with a pizzeria.
It can provide menu information, assist with order placement, and manage other customer inquiries.

## System Architecture
![System Architecture](https://github.com/Wojtek321/ChatPaulo/blob/master/assets/architecture.png?raw=true)

#### Components:

- **Gradio (Inference)**: Provides a user-friendly interface for interacting with the chatbot.

- **Django Rest Framework (API)**: Acts as a bridge between the AI system and the PostgreSQL database, enabling access to data.

- **PostgreSQL (Database)**: Serves as the storage for structured data, including menu information and order records.

- **Qdrant (Vector Database)**: Stores detailed and specific information about each type of pizza and additional details about the pizzeria.

## Chatbot Workflow

![Chatbot Workflow](https://github.com/Wojtek321/ChatPaulo/blob/master/assets/graph_workflow.png?raw=true)

The chatbot workflow illustrates the interactions between the agents:

- **Primary Assistant**: Handles general inquiries and provides initial guidance to address customer needs.
- **Menu Assistant**: Provides information about the menu, including ingredients and the history or origin of various pizzas.
- **Order Assistant**: Assists with placing, modifying, or canceling orders.

## Getting Started

Clone the repository:

```
git clone https://github.com/Wojtek321/ChatPaulo.git
cd ChatPaulo
```

Before building the project, create a .env file in the root directory and add the following API keys:
```
OPENAI_API_KEY=<your_openai_api_key>      # Required for embeddings (GPT model)
ANTHROPIC_API_KEY=<your_anthropic_api_key>  # Optional, for using Claude instead of GPT
```

Build and run the project:

```
make build
make run
```

## Usage

Once the project is running, open your web browser and go to: [http://localhost](http://localhost)



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
