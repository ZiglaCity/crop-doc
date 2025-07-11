import uuid
from fastapi import HTTPException
from PIL import Image
import io

def read_imagefile(file) -> Image.Image:
    image = Image.open(io.BytesIO(file)).convert('RGB')
    return image

# this is an axample of text reponse returned from the prompt to gemini, which we'll be using to avoid wasting tokens calling everytime just to get the same response...
text = """```json
{
  "name": "cassava - brown spot",
  "symptoms": [
    "Small, circular brown spots on leaves, often with dark brown margins and lighter centers.",
    "Spots may enlarge and merge, leading to larger dead (necrotic) areas.",
    "A yellow halo often surrounds the spots, especially on younger lesions.",
    "Severely infected leaves may turn yellow and fall prematurely (defoliation), particularly older leaves."
  ],
  "causes": [
    "Caused by the fungus *Cercosporidium henningsii* (also known as *Cercospora henningsii*).",
    "Spreads primarily through wind-borne spores from infected plants or plant debris.",
    "Favored by warm temperatures and high humidity, common during Ghana's rainy seasons.",
    "Infected crop residue left in the field can serve as a source of infection for new plantings."
  ],
  "treatments": [
    "Direct chemical treatment is generally not practical or cost-effective for smallholder farmers for this disease.",
    "For scattered infected leaves on individual plants, carefully remove and destroy (bury deeply or burn) the affected leaves to reduce spore spread.", 
    "The primary focus should be on preventive measures and cultivating resistant varieties to manage the disease effectively."
  ],
  "preventions": [
    "Plant improved cassava varieties known to be resistant or tolerant to brown spot, as advised by local agricultural extension officers.",
    "Practice good field sanitation: remove and destroy all infected plant debris (leaves, stems) after harvest by burying deeply or burning to reduce disease sources.",
    "Implement crop rotation, avoiding continuous cassava cultivation in the same plot; rotate with crops like maize, legumes, or yams.",
    "Ensure adequate spacing between cassava plants to improve air circulation and reduce humidity within the canopy, which discourages fungal growth.",  
    "Use healthy, disease-free cuttings for planting material, sourcing them from reputable suppliers or healthy mother plants."
  ]
}
```"""


def validate_uuid(id: str):
    try:
        uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format (not a valid UUID)")
