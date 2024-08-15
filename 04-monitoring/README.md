**To use this application through the UI**:

1. Export the __POSTGRES_HOST='localhost'__ variable.
2. Enter the Ollama container and pull the __gemma:2b__ model.
3. Run the prep.py script to index the documents and initialize the Postgres database (this script only needs to be run once).
   If you run it multiple times, it will not execute, so you'll need to delete the volumes first and then try running it again.
4. Use the UI to ask your questions:
   
![image](https://github.com/user-attachments/assets/c4f4fc5b-b679-4733-931c-f4ebabb2cf00)

Dashboard of monitoring using Grafana:
![image](https://github.com/user-attachments/assets/d358a493-cd7e-4c71-81b4-9619beeb04a2)
