import requests

API_URL = "http://localhost:8000/scan"

image_url = "https://content.peat-cloud.com/w800/cassava-mosaic-disease-manioc-1561129470.jpg"

img_response = requests.get(image_url)
img_bytes = img_response.content

files = {
    "file": ("cassava.jpg", img_bytes, "image/jpeg")
}

response = requests.post(API_URL, files=files)

print("Status Code:", response.status_code)
print("Prediction Result:", response.json())
