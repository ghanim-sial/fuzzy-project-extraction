# fuzzy-project-extraction
An implementation of the Project Name Extraction Function using the Fuzzy Wuzzy library and deployed using FastAPI.
Main.py file contains the code to not only create the Fuzzy Wuzzy Project Extraction Function, but also includes the code to deploy it using Fast API. The function is created, pickled, and unpickled before instantiating Fast API.
Function makes use of a list input of existing Project Names, and uses the Fuzzy Wuzzy partial_ratio scoring function to extract project names and/or any variations due to spelling errors. 

Part of a larger implementation with a Spacy named-entity-recognition model as a second phase.

'test spacy fuzzy implementation.ipynb' combines functionality of Spacy and Fuzzy Wuzzy to create a two-check extraction function. After Fuzzy Wuzzy function has been called, spacy function will be called to looks for any project name entities in the text. If any of the spacy extracted entities are in the zameen active projects list and not in the fuzzy wuzzy returned results, it will combine the results of both functions for an expanded list. 
