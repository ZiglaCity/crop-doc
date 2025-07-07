import requests

API_URL = "http://localhost:8000/predict"

image_url = "https://content.peat-cloud.com/w800/cassava-mosaic-disease-manioc-1561129470.jpg"
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjc8kqYAdM942IDQEBZQbbRoK4RmUVfW_6QA&s"

img_response = requests.get(image_url)
img_bytes = img_response.content

files = {
    "file": ("cassava.jpg", img_bytes, "image/jpeg")
}

response = requests.post(API_URL, files=files)

print("Status Code:", response.status_code)
print("Prediction Result:", response.json())
