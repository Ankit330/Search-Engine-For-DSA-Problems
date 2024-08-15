import requests

documents = []
vocab = {}
inverted_index = {}
codeforces_urls = []

# Read lines from LeetCode index file
with open("Leetcode/index.txt", "r", encoding="utf8") as f:
    lines = f.readlines()

# Preprocess the index lines in documents
def preprocess_index(document_text):
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

# Preprocess the text lines in documents
def preprocess_text(document_text):
    text = ""
    for LINE in document_text:
        text += " " + LINE.strip()
    text = text.split("Example 1:")[0]
    terms = [term.lower() for term in text.strip().split()]
    return terms

# Fetch and preprocess Codeforces problems
def fetch_codeforces_problems():
    url = "https://codeforces.com/api/problemset.problems?tags=implementation"
    response = requests.get(url)
    data = response.json()
    problems = data['result']['problems']
    return problems

def preprocess_codeforces_problem(problem):
    name = problem['name'].lower().split()
    tags = problem['tags']
    return name + tags

# Process LeetCode problems
for index, line in enumerate(lines):
    tokens_index = preprocess_index(line)
    line_index_filepath = f"Leetcode/Qdata/{index + 1}/{index + 1}.txt"
    try:
        with open(line_index_filepath, "r", encoding="utf8") as f:
            doc_text = f.readlines()
            tokens_doc_text = preprocess_text(doc_text)
        tokens = tokens_index + tokens_doc_text
        documents.append(tokens)
        tokens = set(tokens)
        for token in tokens:
            if token not in vocab:
                vocab[token] = 1
            else:
                vocab[token] += 1
    except FileNotFoundError:
        print(f"File {line_index_filepath} not found.")

# Fetch and process Codeforces problems
codeforces_problems = fetch_codeforces_problems()
for problem in codeforces_problems:
    tokens = preprocess_codeforces_problem(problem)
    documents.append(tokens)
    tokens = set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1
    # Generate URL for Codeforces problems
    url = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
    codeforces_urls.append(url)

# Sort the vocab according to the frequency in decreasing order
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

# Save the vocab in text file
with open("tf-idf/vocab.txt", "w", encoding="utf-8") as file:
    for key in vocab.keys():
        file.write(key + "\n")

# Save the idf values of vocab in text file
with open("tf-idf/idf-values.txt", "w", encoding="utf-8") as file:
    for key in vocab.keys():
        file.write(str(vocab[key]) + "\n")

# Save all the documents in a text file
with open("tf-idf/documents.txt", "w", encoding="utf-8") as file:
    for document in documents:
        file.write(" ".join(document) + "\n")

# Create the inverted index
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# Save the inverted index in text file
with open("tf-idf/inverted-index.txt", "w", encoding="utf-8") as file:
    for key in inverted_index.keys():
        file.write(key + "\n")
        file.write(" ".join([str(doc_id) for doc_id in inverted_index[key]]) + "\n")

# Save Codeforces problem URLs
with open("codeforces_urls.txt", "w", encoding="utf-8") as file:
    for url in codeforces_urls:
        file.write(url + "\n")

print("Number of documents: ", len(documents))
print("Size of vocab: ", len(vocab))
print("Sample document: ", documents[1])
