#Resume Parser
Brendan J. Herger
hergertarian.com
13herger@gmail.com

##Usage
This is a pretty simple script that will pull text for PDF files, gather contact informaiton, 
and check for the presence/count of a few keywords.

From the root directory of this GitHub repo, you can run the following command:

`python -m code --data_path /path/to/folder/with/resumes/`

##Future work, Limitations
Right now, this code can only parse PDFs. Eventually I'd like to add support for websites, raw 
text, etc.

Also, because this package uses glob.glob, resuems must be in the same folder, and end in .pdf
(lowercase). Eventually I should make this more robust...