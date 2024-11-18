import requests

# Set up GitHub API details
BASE_URL = "https://api.github.com"
TOKEN = "your_personal_access_token"  # Replace with your token
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def search_repositories():
    """Search for repositories with 'machine learning' and 'Python'."""
    url = f"{BASE_URL}/search/repositories?q=machine+learning+language:python&per_page=5"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Error: {response.status_code} - {response.json().get('message', '')}")
        return []

def get_commits(owner, repo):
    """Fetch commit history for a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits?per_page=5"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.json().get('message', '')}")
        return []

def get_contents(owner, repo, path=""):
    """Fetch contents of a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.json().get('message', '')}")
        return []

# Main workflow
if __name__ == "__main__":
    # Step 1: Search repositories
    repositories = search_repositories()
    print("Found Repositories:")
    for repo in repositories:
        print(f"- Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}")

        # Step 2: Get commit history for each repository
        commits = get_commits(repo['owner']['login'], repo['name'])
        print(f"  Latest Commits for {repo['name']}:")
        for commit in commits[:3]:
            print(f"    - Message: {commit['commit']['message']}")

        # Step 3: Get contents of the repository
        contents = get_contents(repo['owner']['login'], repo['name'])
        print(f"  Repository Contents:")
        for content in contents[:3]:  # Limit to 3 items for brevity
            print(f"    - {content['name']} ({content['type']})")
