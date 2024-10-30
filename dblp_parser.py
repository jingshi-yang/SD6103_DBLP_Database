#!/usr/bin/env python
# coding: utf-8

# In[17]:


import xml.sax
import csv

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self, csv_writer):
        self.CurrentData = ""
        self.current_element = None
        self.csv_writer = csv_writer
        self.authors = []
        self.editors = []
        self.ee_links = []
        self.rel_entries = []
        self.current_rel_entry = None  # Track the current rel entry

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag in ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data"]:
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
                "ee": [],
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
                "rels": []  # Collect all rel entries
            }
            self.authors = []
            self.editors = []
            self.ee_links = []
            self.rel_entries = []

        elif tag == "rel":
            # Initialize a new rel entry with its attributes
            self.current_rel_entry = {
                "type": attributes.get("type", ""),
                "uri": attributes.get("uri", ""),
                "label": attributes.get("label", ""),
                "sort": attributes.get("sort", ""),
                "content": ""  # Initialize content as an empty string
            }

    def endElement(self, tag):
        if self.current_element is None:
            return

        if tag == "author":
            self.authors.append(self.CurrentData)
        elif tag == "editor":
            self.editors.append(self.CurrentData)
        elif tag == "ee":
            self.ee_links.append(self.CurrentData)
        elif tag == "rel" and self.current_rel_entry:
            # Finalize and append the rel entry content
            rel_info = (
                f"type: {self.current_rel_entry['type']}, "
                f"uri: {self.current_rel_entry['uri']}, "
                f"label: {self.current_rel_entry['label']}, "
                f"sort: {self.current_rel_entry['sort']}, "
                f"content: {self.current_rel_entry['content']}"
            )
            self.current_element["rels"].append(rel_info)
            self.current_rel_entry = None  # Reset the current rel entry

        if tag in ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data"]:
            # Write each publication to CSV, including all rel entries
            self.csv_writer.writerow({
                'Publication Type': self.current_element.get('type', ''),
                'Key': self.current_element.get('key', ''),
                'Mdate': self.current_element.get('mdate', ''),
                'Publtype': self.current_element.get('publtype', ''),
                'Cdate': self.current_element.get('cdate', ''),
                'Authors': ", ".join(self.authors),
                'Editors': ", ".join(self.editors),
                'Title': self.current_element.get('title', ''),
                'Booktitle': self.current_element.get('booktitle', ''),
                'Pages': self.current_element.get('pages', ''),
                'Year': self.current_element.get('year', ''),
                'Address': self.current_element.get('address', ''),
                'Journal': self.current_element.get('journal', ''),
                'Volume': self.current_element.get('volume', ''),
                'Number': self.current_element.get('number', ''),
                'Month': self.current_element.get('month', ''),
                'URL': self.current_element.get('url', ''),
                'EE': "; ".join(self.ee_links),
                'CDROM': self.current_element.get('cdrom', ''),
                'Cite': self.current_element.get('cite', ''),
                'Publisher': self.current_element.get('publisher', ''),
                'Note': self.current_element.get('note', ''),
                'Crossref': self.current_element.get('crossref', ''),
                'ISBN': self.current_element.get('isbn', ''),
                'Series': self.current_element.get('series', ''),
                'School': self.current_element.get('school', ''),
                'Chapter': self.current_element.get('chapter', ''),
                'Publnr': self.current_element.get('publnr', ''),
                'Stream': self.current_element.get('stream', ''),
                'Rel Entries': " | ".join(self.current_element["rels"])  # Store all rels in a single column, separated by " | "
            })
            self.current_element = None
            self.authors = []
            self.editors = []
            self.rel_entries = []

        self.CurrentData = ""

    def characters(self, content):
        content = content.strip()
        if not self.current_element:
            return

        if self.CurrentData == "author":
            self.authors.append(content)
        elif self.CurrentData == "editor":
            self.editors.append(content)
        elif self.CurrentData == "ee":
            self.ee_links.append(content)
        elif self.CurrentData == "rel" and self.current_rel_entry is not None:
            # Append content to the current rel entry's content field
            self.current_rel_entry["content"] += content
        elif self.CurrentData in self.current_element:
            self.current_element[self.CurrentData] += content

# Main function to parse the XML and export to CSV
def parse_dblp_xml_to_csv(xml_file, csv_file):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            'Publication Type', 'Key', 'Mdate', 'Publtype', 'Cdate', 'Authors', 'Editors', 'Title', 'Booktitle', 
            'Pages', 'Year', 'Address', 'Journal', 'Volume', 'Number', 'Month', 'URL', 'EE', 'CDROM', 'Cite', 
            'Publisher', 'Note', 'Crossref', 'ISBN', 'Series', 'School', 'Chapter', 'Publnr', 'Stream', 
            'Rel Entries'  # Column to capture all rel elements
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        handler = DBLPHandler(writer)
        parser.setContentHandler(handler)

        with open(xml_file, "r", encoding="utf-8") as file:
            parser.parse(file)

    print(f"Parsing complete. Data exported to {csv_file}")

if __name__ == "__main__":
    xml_file_path = r"C:\Users\renal\Downloads\dblp.xml"  # Replace with your actual file path
    csv_file_path = r"C:\Users\renal\Downloads\dblp.csv"  # Output CSV file path
    parse_dblp_xml_to_csv(xml_file_path, csv_file_path)

    print(f"Parsing complete. Data exported to {csv_file_path}")



# In[18]:


import pandas as pd

csv_file_path = r"C:\Users\renal\Downloads\dblp_parsed.csv"  # Replace with your CSV file path

# Load the CSV into a pandas DataFrame
df = pd.read_csv(csv_file_path)


