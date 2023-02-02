import pandas as pd
from googledrive.drivetools import DriveTools
from jobsites.linkedin import LinkedInScrap
from blogspot.postingengine import *
from blogspot.utils import cleanuplabel,cleanupindustry,createjoblevels

credsfile = "googledrive/searchconsole-364317-ee5fb100ebef.json"
gd = DriveTools(credsfile, workbook="WebResults")
existing_jobs = gd.get_existing_jobs(2)

jobs = LinkedInScrap(existing_jobs)
joblisting = jobs.main(end=200)
top50 = list(filter(None, joblisting))

drive_handler, blog_handler = get_blogger_service_obj(credfile)

for pst in range(len(top50)):
    try:
        print(f"publishing post {pst}")
        post_data_blog = post_ = post_body(
            company_logo=top50[pst]["company_logo"],
            company=top50[pst]["company"],
            location=top50[pst]["location"],
            posting_time=top50[pst]["posting_time"],
            details=top50[pst]["details"]["job_desc_details"],
            application_link=top50[pst]["application_link"],
        )
       
        joblisting_blog = joblisting[pst]
        # labels generate
        job_functions_label = ['Other' if len(label) == 0 else label for label in set(cleanuplabel(label) for label in joblisting_blog['details']['jobcriterialist']['Job function'].split(" ")) if label != 'Other']
        job_industry_labels = ['Other' if len(label) == 0 else label for label in set(cleanupindustry(label) for label in joblisting_blog['details']['jobcriterialist']['Industries'].split(" ")) if label != 'Other']
        employment_type = joblisting_blog['details']['jobcriterialist']['Employment type']
        # createjoblevels
        levels = createjoblevels(
            label = job_functions_label,
            seniority=joblisting_blog['details']['jobcriterialist']['Seniority level'],
            employment_type = joblisting_blog['details']['jobcriterialist']['Employment type'],
            industry = job_industry_labels)
        
        body_content = {
            "title": f'{joblisting_blog["job_title"]} - {joblisting_blog["company"]}',
            "content": prep_post_template("./blogspot/", "post_template.html", post_data_blog),
            "labels": levels,
            "publish": True,
        }
        out = create_blog_post(BLOG_ID, blog_handler, body_content, isDraft=False)
        # save the jobs scrapped
        gd.write_df(pd.json_normalize(top50),2)
    except Exception as e:
        print(e)


# print(pst)
# 
