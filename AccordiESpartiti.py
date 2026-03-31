#!/usr/bin/env python
# coding: utf-8

# In[7]:


import re
import os
from markdown_pdf import MarkdownPdf, Section
os.makedirs('output',exist_ok = True)


# In[8]:


# txt parser
url_list = []
with open('canzoni.txt') as f:
    lines = f.readlines()
    columns = []
    i = 1
    for line in lines:
        line = line.strip() # remove leading/trailing white spaces

        url_list.append(line) # append line to list


# In[9]:


#url = "https://www.accordiespartiti.it/accordi/internazionali/imagine-dragons/demons/"
trasposizione = 0

for url in url_list:

    # parsing the url to find if is international 
    if url[40:54] == 'internazionali':
        international = True
    else:
        international = False

    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # keep visible for debugging
        page = await browser.new_page()
        await page.goto(url)

        await page.wait_for_selector("#pitchDown")

        # Dismiss the cookie banner first
        try:
            # Try clicking an "Accept" or "Agree" button — inspect the popup to find the right selector
            await page.click("#ez-accept-all", timeout=5000)
        except:
            # If no accept button found, just force-remove the overlay from the DOM
            await page.evaluate("document.getElementById('ez-cmpv2-container').remove()")

        # Dismiss video popup if it appears
        try:
            await page.click(".close-popup.popup-x", timeout=3000)
        except:
            pass  # No popup, continue normally
        # Now click the pitch buttons

        if trasposizione > 0:
            for i in range(trasposizione):
                await page.click("#pitchUp") 

        if trasposizione < 0:
            for i in range(trasposizione):
                await page.click("#pitchUp")

        await page.wait_for_timeout(500)

        span_value = await page.inner_text("#output")
        #print("Output: applied transpose", span_value)

        post_title = await page.inner_text("#post-title")
        post_artist = await page.inner_text("#category-name")
        post_content = await page.inner_text(".post-content")
        #print(post_content)

        await browser.close()

    if not international:
        lookup_left_string = post_title+": ACCORDI"
        left = post_content.find(lookup_left_string)
        post_content_parsed_left = post_content[left+102:]
        #print(post_content_parsed_left)



        lookup_right_string = "10+ Trucchi per memorizzare le note sulla Chitarra."
        right = post_content_parsed_left.find(lookup_right_string)
        #print(right)
        if left == -1 or right == -1:
            print("⚠️ Boundary not found — check your lookup strings")
        post_content_parsed = post_content_parsed_left[:right]

    else:
        lookup_left_string = post_title+": CHORDS"
        left = post_content.find(lookup_left_string)
        post_content_parsed_left = post_content[left+102:]

        lookup_right_string = "10+ Trucchi per memorizzare le note sulla Chitarra."
        right = post_content_parsed_left.find(lookup_right_string)

        if left == -1 or right == -1:
            print("⚠️ Boundary not found — check your lookup strings")
        post_content_parsed = post_content_parsed_left[:right]

    # convert content into list
    content_list = post_content_parsed.split('\n')

    ## make the markdown correctly
    # pdf setup
    # Build the full markdown string first
    if trasposizione == 0:
        span_value = '_original'
    else: 
        span_value = '_' + span_value


    content_md = f"## {post_title} - {post_artist}\n\nTranspose: {span_value}\n\n"

    # chords
    for list_element in content_list:
        content_md += f"```\n{list_element}\n```\n\n"

    # Single section = no page breaks
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(content_md, toc=False))
    pdf.save(f"output/{post_artist}_{post_title}{span_value}.pdf")


# In[27]:


files = sorted([f for f in os.listdir('output')])

print(f'pdf files found: {len(files)}')
for idx in range(len(files)):
    files[idx] = 'output/' + files[idx]
    print(files[idx])


# In[28]:


from pypdf import PdfWriter

merger = PdfWriter()

for pdf in files:
    merger.append(pdf)

with open("accordi.pdf", "wb") as f:
    merger.write(f)


# In[ ]:




