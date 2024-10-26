#!/usr/bin/env python
# coding: utf-8

# In[17]:


import xml.sax
import csv

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.current_element = None  # Initialize as None, will be a dict when processing a publication
        self.publications = []
        self.author = ""
        self.editor = ""

    # Called when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag in ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www"]:
            # Initialize a new dictionary for the current publication with default values
            self.current_element = {
                "type": tag,
                "key": attributes.get("key", ""),
                "mdate": attributes.get("mdate", ""),
                "publtype": attributes.get("publtype", ""),
                "cdate": attributes.get("cdate", ""),
                "authors": [],
                "editors": [],
                "title": "",
                "booktitle": "",
                "pages": "",
                "year": "",
                "address": "",
                "journal": "",
                "volume": "",
                "number": "",
                "month": "",
                "url": "",
                "ee": "",
                "cdrom": "",
                "cite": "",
                "publisher": "",
                "note": "",
                "crossref": "",
                "isbn": "",
                "series": "",
                "school": "",
                "chapter": "",
                "publnr": "",
                "stream": "",
                "rel": ""
            }

    # Called when an element ends
    def endElement(self, tag):
        if self.CurrentData == "author":
            if self.current_element and self.author:  # Ensure author is not None or empty
                self.current_element["authors"].append(self.author)
            self.author = ""  # Reset after adding

        elif self.CurrentData == "editor":
            if self.current_element and self.editor:  # Ensure editor is not None or empty
                self.current_element["editors"].append(self.editor)
            self.editor = ""  # Reset after adding

        elif self.CurrentData and self.current_element and self.CurrentData in self.current_element:
            # Safely set the value to avoid None issues
            self.current_element[self.CurrentData] = getattr(self, self.CurrentData, "").strip()

        # Store the current publication when it ends
        if tag in ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www"]:
            if self.current_element:
                self.publications.append(self.current_element)
            self.current_element = None

        self.CurrentData = ""

    # Called when characters between elements are found
    def characters(self, content):
        content = content.strip()
        if self.CurrentData == "author":
            self.author = content
        elif self.CurrentData == "editor":
            self.editor = content
        elif self.CurrentData and self.current_element and self.CurrentData in self.current_element:
            setattr(self, self.CurrentData, content)

# Main function to parse the XML and export to CSV with additional metadata fields
def parse_dblp_xml_to_csv(xml_file, csv_file):
    # Create a SAX parser
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # Create the handler
    handler = DBLPHandler()
    parser.setContentHandler(handler)

    # Open and parse the XML file
    with open(xml_file, "r", encoding="utf-8") as file:
        parser.parse(file)

    # Write results to CSV
    with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            'Publication Type', 'Key', 'Mdate', 'Publtype', 'Cdate', 'Authors', 'Editors', 'Title', 'Booktitle', 
            'Pages', 'Year', 'Address', 'Journal', 'Volume', 'Number', 'Month', 'URL', 'EE', 'CDROM', 'Cite', 
            'Publisher', 'Note', 'Crossref', 'ISBN', 'Series', 'School', 'Chapter', 'Publnr', 'Stream', 'Rel'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Write the publication details
        for pub in handler.publications:
            # Use the get() method and provide default values to avoid NoneType errors
            writer.writerow({
                'Publication Type': pub.get('type', ''),
                'Key': pub.get('key', ''),
                'Mdate': pub.get('mdate', ''),
                'Publtype': pub.get('publtype', ''),
                'Cdate': pub.get('cdate', ''),
                'Authors': ", ".join(pub.get('authors', [])) if pub.get('authors') else '',  # Safe join for authors
                'Editors': ", ".join(pub.get('editors', [])) if pub.get('editors') else '',  # Safe join for editors
                'Title': pub.get('title', ''),
                'Booktitle': pub.get('booktitle', ''),
                'Pages': pub.get('pages', ''),
                'Year': pub.get('year', ''),
                'Address': pub.get('address', ''),
                'Journal': pub.get('journal', ''),
                'Volume': pub.get('volume', ''),
                'Number': pub.get('number', ''),
                'Month': pub.get('month', ''),
                'URL': pub.get('url', ''),
                'EE': pub.get('ee', ''),
                'CDROM': pub.get('cdrom', ''),
                'Cite': pub.get('cite', ''),
                'Publisher': pub.get('publisher', ''),
                'Note': pub.get('note', ''),
                'Crossref': pub.get('crossref', ''),
                'ISBN': pub.get('isbn', ''),
                'Series': pub.get('series', ''),
                'School': pub.get('school', ''),
                'Chapter': pub.get('chapter', ''),
                'Publnr': pub.get('publnr', ''),
                'Stream': pub.get('stream', ''),
                'Rel': pub.get('rel', '')
            })

#Change path address
if __name__ == "__main__":
    xml_file_path = r"C:\Users\renal\Downloads\dblp.xml"  # Replace with your actual file path
    csv_file_path = r"C:\Users\renal\Downloads\dblp_parsed.csv"  # Output CSV file path
    parse_dblp_xml_to_csv(xml_file_path, csv_file_path)

    print(f"Parsing complete. Data exported to {csv_file_path}")


# In[18]:


import pandas as pd

csv_file_path = r"C:\Users\renal\Downloads\dblp_parsed.csv"  # Replace with your CSV file path

# Load the CSV into a pandas DataFrame
df = pd.read_csv(csv_file_path)


