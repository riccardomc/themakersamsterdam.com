from bs4 import BeautifulSoup
import argparse
import tempfile
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

with open(args.filename) as html_doc:
    soup = BeautifulSoup(html_doc, "html.parser")

imgs = soup.find_all("img", src=True)
for img in imgs:
    img["class"] = "lazy"
    img["data-src"] = img["src"]
    del img["src"]

yall_script = soup.find_all("script", src="/static/yall.min.js")

if not yall_script:
    script_tag_1 = soup.new_tag("script", src="/static/yall.min.js")
    script_tag_2 = soup.new_tag("script")
    script_tag_2.string = """document.addEventListener("DOMContentLoaded", yall);"""
    soup.head.append(script_tag_1)
    soup.head.append(script_tag_2)

temp_file = tempfile.NamedTemporaryFile(mode="w", delete=True)
temp_file.write(soup.prettify())
temp_file.flush()
shutil.copy2(temp_file.name, args.filename)
temp_file.close()
