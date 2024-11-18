Here’s a detailed `troubleshooting_guide.md` file tailored to the client's needs:

---

### **Troubleshooting Guide**

This guide addresses common issues you may encounter when working with the GitHub API to search for repositories with the keywords **"machine learning"** and **"python"**, fetch commits, and extract repository contents.

---

### **1. Rate Limit Exceeded**

#### **Issue**:
The API stops responding and returns an error like:
```json
{
  "message": "API rate limit exceeded for user."
}
```

#### **Cause**:
- Too many requests in a short period.
- GitHub's default rate limit for unauthenticated users is **60 requests per hour**.

#### **Solution**:
- **Authenticate** with a personal access token to increase the limit to **5,000 requests per hour**.
- Include the token in the request header:
  ```
  Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN
  ```
- Monitor remaining requests using the `X-RateLimit-Remaining` response header.

---

### **2. Authentication Errors**

#### **Issue**:
The API returns:
```json
{
  "message": "Bad credentials",
  "documentation_url": "https://docs.github.com/rest"
}
```

#### **Cause**:
- Missing or incorrect personal access token.

#### **Solution**:
- Generate a personal access token from your GitHub account:
  1. Go to **Settings > Developer settings > Personal access tokens**.
  2. Select scopes (e.g., `repo`, `read:org`).
  3. Copy and securely store the token.
- Update your token in the headers:
  ```
  Authorization: Bearer YOUR_PERSONAL_ACCESS_TOKEN
  ```

---

### **3. Pagination Issues**

#### **Issue**:
Not all results are returned in one request.

#### **Cause**:
- GitHub limits the number of items per request to **100**.
- For larger datasets, results are split across pages.

#### **Solution**:
- Use the `?page=` and `?per_page=` parameters in your request to fetch all results.
- Example for the second page of search results:
  ```
  GET https://api.github.com/search/repositories?q=machine+learning+language:python&per_page=10&page=2
  ```

#### **Python Example**:
```python
def fetch_all_pages(url):
    results = []
    page = 1
    while True:
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        if response.status_code != 200 or not response.json().get("items"):
            break
        results.extend(response.json()["items"])
        page += 1
    return results
```

---

### **4. Invalid Query Parameters**

#### **Issue**:
The API returns an error:
```json
{
  "message": "Validation Failed",
  "errors": [
    "The query '...' is malformed."
  ]
}
```

#### **Cause**:
- Improperly formatted query string.
- Missing required parameters.

#### **Solution**:
- Ensure the query is properly constructed. For example:
  ```
  GET https://api.github.com/search/repositories?q=machine+learning+language:python&per_page=5
  ```
- Validate query strings with the [GitHub API Explorer](https://docs.github.com/rest).

---

### **5. Repository or File Not Found**

#### **Issue**:
The API returns:
```json
{
  "message": "Not Found",
  "documentation_url": "https://docs.github.com/rest"
}
```

#### **Cause**:
- Incorrect `owner` or `repo` name.
- The repository or file is private or doesn’t exist.

#### **Solution**:
- Double-check the repository details (e.g., `scikit-learn/scikit-learn`).
- Use the `/search/repositories` endpoint to verify repository names:
  ```
  GET https://api.github.com/search/repositories?q=machine+learning+language:python&per_page=5
  ```

---

### **6. Missing Permissions**

#### **Issue**:
The API returns:
```json
{
  "message": "Resource not accessible by integration"
}
```

#### **Cause**:
- Accessing private repositories without proper permissions.
- Token does not have the necessary scopes.

#### **Solution**:
- Verify that the token has the appropriate scopes (e.g., `repo`, `read:org` for private data).
- If working with private repositories, request access from the repository owner.

---

### **7. Inconsistent Data**

#### **Issue**:
The API response contains missing or unexpected data fields.

#### **Cause**:
- The repository may not have standard files (e.g., no `README.md` or code files).

#### **Solution**:
- Handle missing data gracefully in your code. For example:
  ```python
  if "README.md" not in [item["name"] for item in contents]:
      print("README.md not found.")
  ```
- Check the file structure by using:
  ```
  GET https://api.github.com/repos/{owner}/{repo}/contents
  ```

---

### **8. Network Issues**

#### **Issue**:
Requests fail with errors like:
```plaintext
TimeoutError: The request timed out.
```

#### **Cause**:
- Slow or unstable internet connection.
- API server downtime.

#### **Solution**:
- Retry the request after a short delay:
  ```python
  import time

  for i in range(3):  # Retry 3 times
      response = requests.get(url, headers=HEADERS)
      if response.status_code == 200:
          break
      time.sleep(5)  # Wait 5 seconds before retrying
  ```
- Check GitHub’s status at [GitHub Status](https://www.githubstatus.com/).

---

### **9. Unreadable Error Messages**

#### **Issue**:
Error responses are unclear or difficult to debug.

#### **Solution**:
- Use logging to capture error messages:
  ```python
  import logging

  logging.basicConfig(level=logging.ERROR)
  try:
      response = requests.get(url, headers=HEADERS)
      response.raise_for_status()
  except requests.exceptions.HTTPError as e:
      logging.error(f"HTTP error: {e}")
  ```

---

### **Tips for Debugging**

1. **Use Postman**: Test API calls manually before automating them in Python.
2. **Enable Logging**: Log request details (URLs, headers, payloads) to understand what went wrong.
3. **Check API Documentation**: Refer to [GitHub REST API Docs](https://docs.github.com/rest) for detailed information on endpoints and parameters.

---

This guide ensures smooth handling of potential issues when working with the GitHub API. If you encounter any new challenges, document them and update this guide accordingly.
