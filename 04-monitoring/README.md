**To use this application using the UI**:

1. Export the POSTGRES_HOST='localhost' variable.
2. Enter the Ollama container and pull the gemma:2b model.
3. Run the prep.py script to index the documents and initialize the Postgres database (this script only needs to be run once).
   If you run it multiple times, it will not execute, so you'll need to delete the volumes first and then try running it again.
4. Use the UI to ask your questions.
