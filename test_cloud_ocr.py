import base64
import os
import requests
import json

# User provided info
API_URL = "https://g49fgd0070pda7k8.aistudio-app.com/layout-parsing"
TOKEN = "a6803449a14d76b8484003c68f5aa3547e54e59d"
file_path = "data/samples/contract_sample.pdf"

def test_cloud_ocr():
    print(f"Testing Cloud OCR on {file_path}")
    
    with open(file_path, "rb") as file:
        file_bytes = file.read()
        file_data = base64.b64encode(file_bytes).decode("ascii")

    headers = {
        "Authorization": f"token {TOKEN}",
        "Content-Type": "application/json"
    }

    # PDF = 0, Image = 1
    # contract_sample.pdf is a PDF
    payload = {
        "file": file_data,
        "fileType": 0,
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False,
    }

    print("Sending request...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            # Dump the first result's structure to see if we have coords/bboxes
            print("Response Keys:", result.keys())
            if "result" in result and "layoutParsingResults" in result["result"]:
                first_page = result["result"]["layoutParsingResults"][0]
                print("Page 1 Keys:", first_page.keys())
                
                # Check for parsingResult or similar which might have bboxes
                if "parsingResult" in first_page:
                    print("parsingResult snippet:", str(first_page["parsingResult"])[:500])
                else:
                    print("No 'parsingResult' key found.")
                    
                # Save raw response to inspect
                with open("cloud_ocr_response.json", "w") as f:
                    json.dump(result, f, indent=2)
                print("Saved full response to cloud_ocr_response.json")
            else:
                print("Unexpected JSON structure:", result)
        else:
            print("Error Response:", response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_cloud_ocr()
