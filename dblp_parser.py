#!/usr/bin/env python
# coding: utf-8

# In[17]:


import xml.sax
import csv
import html  # For decoding HTML entities

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self, rel_writer, author_writer, editor_writer, key_features_writer):
        self.CurrentData = ""
        self.current_element = None
        self.rel_writer = rel_writer
        self.author_writer = author_writer
        self.editor_writer = editor_writer
        self.key_features_writer = key_features_writer
        self.authors = []
        self.editors = []
        self.current_rel_entry = None
        self.current_author_orcid = None
        self.current_editor_orcid = None
        self.current_author_name = ""
        self.current_editor_name = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag in ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data"]:
            self.current_element = {
                "type": tag,
                "key": attributes.get("key", ""),
                "mdate": attributes.get("mdate", "")
            }
            self.authors = []
            self.editors = []

            # Process the 'key' attribute to extract 'Key Source' and 'Key Name'
            key_parts = attributes.get("key", "").split("/")
            key_source = key_parts[0] if len(key_parts) > 0 else ""
            key_name = key_parts[1] if len(key_parts) > 1 else ""

            # Write to key features CSV
            self.key_features_writer.writerow({
                'Publication Type': tag,
                'Key': attributes.get("key", ""),
                'Mdate': attributes.get("mdate", ""),
                'Key Source': key_source,
                'Key Name': key_name
            })

        elif tag == "rel":
            # Initialize a new rel entry with its attributes
            self.current_rel_entry = {
                "type": attributes.get("type", ""),
                "uri": attributes.get("uri", ""),
                "label": attributes.get("label", ""),
                "sort": attributes.get("sort", ""),
                "content": ""
            }

        elif tag == "author":
            # Capture ORCID if available
            self.current_author_orcid = attributes.get("orcid", "")
            self.current_author_name = ""  # Reset for each new author

        elif tag == "editor":
            # Capture ORCID if available
            self.current_editor_orcid = attributes.get("orcid", "")
            self.current_editor_name = ""  # Reset for each new editor

    def endElement(self, tag):
        if self.current_element is None:
            return

        if tag == "author":
            # Write author and ORCID to the author CSV table
            author_name = html.unescape(self.current_author_name)  # Decode HTML entities
            self.author_writer.writerow({
                'Publication Type': self.current_element.get('type', ''),
                'Key': self.current_element.get('key', ''),
                'Mdate': self.current_element.get('mdate', ''),
                'Author': author_name,
                'Author ORCID': self.current_author_orcid
            })
            self.current_author_orcid = None  # Reset for next author

        elif tag == "editor":
            # Write editor and ORCID to the editor CSV table
            editor_name = html.unescape(self.current_editor_name)  # Decode HTML entities
            self.editor_writer.writerow({
                'Publication Type': self.current_element.get('type', ''),
                'Key': self.current_element.get('key', ''),
                'Mdate': self.current_element.get('mdate', ''),
                'Editor': editor_name,
                'Editor ORCID': self.current_editor_orcid
            })
            self.current_editor_orcid = None  # Reset for next editor

        elif tag == "rel" and self.current_rel_entry:
            # Write rel entry to the rel CSV table if URI is present
            if self.current_rel_entry['uri']:
                self.rel_writer.writerow({
                    'Publication Type': self.current_element.get('type', ''),
                    'Key': self.current_element.get('key', ''),
                    'Mdate': self.current_element.get('mdate', ''),
                    'Rel URI': self.current_rel_entry['uri'],
                    'Rel Label': self.current_rel_entry['label'],
                    'Rel Sort': self.current_rel_entry['sort']
                })
            self.current_rel_entry = None  # Reset for next rel entry

        self.CurrentData = ""

    def characters(self, content):
        content = content.strip()
        if not self.current_element:
            return

        if self.CurrentData == "author":
            # Accumulate author name content
            self.current_author_name += content
        elif self.CurrentData == "editor":
            # Accumulate editor name content
            self.current_editor_name += content
        elif self.CurrentData == "rel" and self.current_rel_entry is not None:
            # Append content to the current rel entry's content field
            self.current_rel_entry["content"] += content

# Main function to parse the XML and export to separate CSV files
def parse_dblp_xml_to_csv(xml_file, rel_csv, author_csv, editor_csv, key_features_csv):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    with open(rel_csv, mode="w", newline="", encoding="utf-8") as rel_file, \
         open(author_csv, mode="w", newline="", encoding="utf-8") as author_file, \
         open(editor_csv, mode="w", newline="", encoding="utf-8") as editor_file, \
         open(key_features_csv, mode="w", newline="", encoding="utf-8") as key_features_file:

        rel_fieldnames = ['Publication Type', 'Key', 'Mdate', 'Rel URI', 'Rel Label', 'Rel Sort']
        author_fieldnames = ['Publication Type', 'Key', 'Mdate', 'Author', 'Author ORCID']
        editor_fieldnames = ['Publication Type', 'Key', 'Mdate', 'Editor', 'Editor ORCID']
        key_features_fieldnames = ['Publication Type', 'Key', 'Mdate', 'Key Source', 'Key Name']

        rel_writer = csv.DictWriter(rel_file, fieldnames=rel_fieldnames)
        author_writer = csv.DictWriter(author_file, fieldnames=author_fieldnames)
        editor_writer = csv.DictWriter(editor_file, fieldnames=editor_fieldnames)
        key_features_writer = csv.DictWriter(key_features_file, fieldnames=key_features_fieldnames)

        # Write headers for each CSV file
        rel_writer.writeheader()
        author_writer.writeheader()
        editor_writer.writeheader()
        key_features_writer.writeheader()

        # Initialize the handler with the specific CSV writers
        handler = DBLPHandler(rel_writer, author_writer, editor_writer, key_features_writer)
        parser.setContentHandler(handler)

        # Parse the XML file
        with open(xml_file, "r", encoding="utf-8") as file:
            parser.parse(file)

    print(f"Parsing complete. Data exported to {rel_csv}, {author_csv}, {editor_csv}, and {key_features_csv}")

if __name__ == "__main__":
    xml_file_path = r"C:\Users\renal\Downloads\dblp.xml"  # Replace with your actual file path
    rel_csv_path = r"C:\Users\renal\Downloads\dblp_rel.csv"  # Output CSV file for rel entries
    author_csv_path = r"C:\Users\renal\Downloads\dblp_author.csv"  # Output CSV file for authors
    editor_csv_path = r"C:\Users\renal\Downloads\dblp_editor.csv"  # Output CSV file for editors
    key_features_csv_path = r"C:\Users\renal\Downloads\dblp_key_features.csv"  # Output CSV file for key features

    parse_dblp_xml_to_csv(xml_file_path, rel_csv_path, author_csv_path, editor_csv_path, key_features_csv_path)




# In[18]:


import pandas as pd

csv_file_path = r"C:\Users\renal\Downloads\dblp_parsed.csv"  # Replace with your CSV file path

# Load the CSV into a pandas DataFrame
df = pd.read_csv(csv_file_path)


