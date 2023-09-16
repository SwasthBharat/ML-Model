import requests
import base64
import json
import pytz
import datetime
import os

dat = ""

token = os.getenv('T2')

repositories_list = {
    "Android User App": "https://github.com/SwasthBharat/Android-User-app",
    "Backend Server": "https://github.com/SwasthBharat/Backend-Server",
    "Doctor Dashboard": "https://github.com/SwasthBharat/Doctor-Dashboard",
    "Frontend Web": "https://github.com/SwasthBharat/Frontend-Web",
    "ML Model": "https://github.com/SwasthBharat/ML-Model",
}

repositories = {
    "Android User App": "https://api.github.com/repos/SwasthBharat/Android-User-app",
    "Backend Server": "https://api.github.com/repos/SwasthBharat/Backend-Server",
    "Doctor Dashboard": "https://api.github.com/repos/SwasthBharat/Doctor-Dashboard",
    "Frontend Web": "https://api.github.com/repos/SwasthBharat/Frontend-Web",
    "ML Model": "https://api.github.com/repos/SwasthBharat/ML-Model",
}


def fetch_last_commit_info(repo_url):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(f"{repo_url}/commits/main", headers=headers)

    if response.status_code == 200:
        commit_data = response.json()
        b = {}
        datL = commit_data["files"]
        for i in datL:
            b[i["filename"]] = i.get("blob_url")
        return {
            "ub": commit_data["commit"]["author"]["name"],
            "ua": commit_data["commit"]["author"]["date"],
            "cm": commit_data["commit"]["message"],
            "cd": commit_data["commit"]["committer"]["date"],
            "cf": len(commit_data["files"]),
            "url": commit_data["html_url"],
            "un": commit_data["author"]["html_url"],
            "fn": b,
            "curl": commit_data['parents'][0]['html_url'] if len(commit_data['parents']) > 0  else ""
        }
    else:
        return None


def convert_to_ist(utc_time_str):
    utc_time = datetime.datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    ist = pytz.timezone("Asia/Kolkata")
    return utc_time.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%Y-%m-%d %H:%M:%S IST")


for project,repo_url in repositories.items():
    
    commit_info = fetch_last_commit_info(repo_url)
    if commit_info:
        dat+= f"# [**{project}**]({repositories_list[project]})"
        dat += "\n"
        dat += f"   - Updated by [{commit_info['ub']}]({commit_info['un']})"
        dat += "\n"
        if commit_info['curl'] == "":
            dat += f"   - Updated at {convert_to_ist(commit_info['ua'])}"
        else:
            dat += f"   - Updated at [{convert_to_ist(commit_info['ua'])}]({commit_info['curl']})"
        dat += "\n"
        dat += f"   - Latest Commit Message: {commit_info['cm']}"
        dat += "\n"
        dat += f"   - No. of Changed Files: {commit_info['cf']}"
        dat+="\n"
        kkk = "\n"
        
        for i,j in commit_info['fn'].items():
            kkk+= f"      - [{i}]({j})"
            kkk+= "\n"
            
        
        dat += f"   - Files modified: {kkk}"
        dat += "\n\n\n"


print(dat)


# Set up your Personal Access Token and other variables
token = os.getenv('T1')
repo_owner = "SwasthBharat"
repo_name = ".github"
file_path = "README.md"
commit_message = "Update README"
branch_name = "main"
file_content = dat

# Function to convert UTC time to IST
def convert_to_ist(utc_time_str):
    utc_time = datetime.datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    ist = pytz.timezone("Asia/Kolkata")
    return utc_time.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%Y-%m-%d %H:%M:%S IST")

# Prepare the API request to create or update the file
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

# Fetch the current file content for comparison
response = requests.get(url, headers=headers)
current_file_content = response.json()["content"]
current_file_sha = response.json()["sha"]

# Encode the new file content
file_content_encoded = base64.b64encode(file_content.encode()).decode()

data = {
    "message": commit_message,
    "content": file_content_encoded,
    "sha": current_file_sha,
    "branch": branch_name,
}

response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("File updated successfully.")
else:
    print(f"Failed to update file. Status code: {response.status_code}")
    print(response.text)
