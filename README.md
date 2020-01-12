**Smart XML Analyzer**

The script find html element difference between original file and updated html files 
by specific element. 

Before run script, create local virtual environment and install necessary libraries:

     python3 -m venv .env
     source .env/bin/activate
     pip install -r requirements.txt

How to run script: 
    
    python analyze.py -of=PATH_TO_ORIGINAL_FILE -sf=PATH_TO_SAMPLE_FILE


Arguments:

    original_path - original HTML file to find the element with attribute id=<original_html_element_id> 
    sample_path - path to HTML file to search a similar element
    target_element - an optional, default - "make-everything-ok-button"


Output example: 

    Original file path: /Users/user1/PycharmProjects/SmartXMLAnalyzer/samples/sample-0-origin.html
    Sample file path: /Users/alexkravchuk/PycharmProjects/SmartXMLAnalyzer/samples/sample-4-the-mash.html
    Target element: make-everything-ok-button
    Path to the element: html > body > div > div > div > div > div > div > a
