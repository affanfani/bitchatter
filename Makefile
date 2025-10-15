# University Department Chatbot - Development Commands

.PHONY: help install run test clean lint format

help:  ## Show this help message
	@echo "University Department Chatbot - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

run:  ## Run the Flask development server
	flask run --host=0.0.0.0 --port=5000

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=html

lint:  ## Run linting
	flake8 app/ tests/
	black --check app/ tests/

format:  ## Format code
	black app/ tests/
	isort app/ tests/

clean:  ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

init-db:  ## Initialize database
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade

reset-db:  ## Reset database
	rm -f university_chatbot.db
	rm -rf migrations/
	make init-db

dev-setup:  ## Complete development setup
	make install
	make init-db
	@echo "Development setup complete! Run 'make run' to start the server."
