# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import pickle
import re



from fuzzywuzzy import fuzz, process
from rapidfuzz import process as rprocess, fuzz as rfuzz
import pandas as pd

projects_list_final = ['Broadway Heights','Prime City','Icon Valley','Zameen OPAL','Defence Raya Fairways','Zee Avenue','Zameen Ace Mall','Palm Dreams',
'The Opus- Luxury Residencies','Bali Business Boulevard','Zameen Ace Homes','City Star Residencia','City Star Shopping Centre','Mall 35','Canal Valley Daska',
'Zameen Aurum','Pace Circle','Roman Grove','The Mega Mall & Residency','3 Jays Tower','River Courtyard','Zameen Quad','Gulberg City Center','RJS-Lifestyle Residencia',
'Sitara Icon','Residence 15','Sitara Serene','Mall of Gujrat','Grand Gallery','DB32','Amanah Noor Residence','Grande Palladium','The Edge Mall',
'J Heights','Tomorrowland','Highland Villas','Pearl One Residencies','Downtown Rumanza','De Orion Mall','Golf View Rumanza','Serenity Heights',
'Union Tower','Hyde Park One','Rockland Villas','Box Park II','Al Rafi Heights','Platinum Homes DHAM','102 by Icon-Residential Towers','ONE VH','Amanah Mall Service Apartments',
'201 Apartment','North Vista-II','Jinnah Square apartments','Aziz Excellency','River Hills 5','Swiss 99 Tower','River Courtyard Tower 2','Zameen NEO',
'Central Park Townhouses','Saeeda Residency','Nova City','Zen Apartments','Century Venture 1','Beach Resort','Expo Gold','Mountain Village Naran',
'RJs Square','Madison Square','Grand Orchard','Al Rauf Smart City','Rachna Pearl Hotel','Al-Mannan Spanish Villas','Platinum Villas DHAM','Zulekha Residency',
'Boulevard Heights','R&M Tower','Barki Orchard','Smart City Housing Scheme','Spanish Homes','Amber Prime','Damaan City','Bin Qasim Trade Centre','Q High Street','Dream Homes',
'Zameen Phoenix','Zameen Jade','Premier One','Palm Green Villas','Spanish Villas','360 Residences',
'Garden City','Prime City 2','Green Scape Farms','Airport Enclave', 'Spanish', 'Damaan', '360 Res', 'Premium One', 'The Man City', 'Smart City', 'Premier 1', 'Premium 1']
stop_projects = ['Residence', 'Apartment', 'Residencies', 'ONE', 'Zameen', 'Valley']
def contains(list, value):
    counter = 0
    for i in list:
        if i.__contains__(value):
            counter +=1
        return counter
class ProjectNameExtraction:
    def __init__(self, projects_names_list, common_projects_words):
        self.projects_list = projects_names_list
        self.stop_words = common_projects_words
    def project_name(self, text: str) -> str:
        if type(text) == str:
            text = text.replace("\\'", "")
            text = text.replace("'", "")
            text = re.sub(r'[\n.]', '', text)
        threshold = 85
        results = []
        for name in self.projects_list:
            matches = process.extractOne(name, [text], scorer = rfuzz.partial_ratio)
            if any(common_word in text for common_word in self.stop_words):
                threshold = 87
            if name == 'Zen Apartments':
                threshold = 95
            elif name == 'Union Tower':
                threshold = 90
            elif name == 'Prime City 2':
                threshold = 95
            elif name == 'J Heights':
                threshold = 95        
            elif name == 'Tomorrowland':
                threshold = 98
            if matches[1] > threshold:  # Set your threshold for a match
            #matches[1] is the identified match, search string is the project name, i is the row number
                results.append([name, matches[1]])
        return results
            #     return [text, matches[1]]
            # else:
            #     return None

#Function creation with dataframe and project names list input parameters
with open('project_extraction_model.pickle', 'wb') as file:
    pickle.dump(ProjectNameExtraction(projects_names_list=projects_list_final, common_projects_words=stop_projects), file)

# Dummy Sentiment Analysis Model (Replace with your own model)

app = FastAPI()
extraction_model = ProjectNameExtraction(projects_names_list=projects_list_final, common_projects_words = stop_projects)

class ProjectExtractionRequest(BaseModel):
    text: str

class ProjectExtractionResponse(BaseModel):
    extraction: list

@app.post("/extract-projects", response_model=ProjectExtractionResponse)
def extract_projects(request: ProjectExtractionRequest):
    with open('project_extraction_model.pickle', 'rb') as file:
        extraction_model = pickle.load(file)
    try:
        prediction = extraction_model.project_name(request.text)
        return {"extraction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)

