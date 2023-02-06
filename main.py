import pandas as pd
from googledrive.drivetools import DriveTools
from jobsites.linkedin import LinkedInScrap
from blogspot.postingengine import *
from blogspot.utils import cleanuplabel,cleanupindustry,createjoblevels


credsfile = "googledrive/searchconsole-364317-ee5fb100ebef.json"
gd = DriveTools(credsfile, workbook="WebResults")
existing_jobs = gd.get_existing_jobs(2)



# jobs = LinkedInScrap(existing_jobs)
# joblisting = jobs.main(end=1000)
# top50 = list(filter(None, joblisting))

# gd.write_df(pd.json_normalize(top50),2)

# posting functionality
jobs_to_post = gd.get_existing_jobs(2,full=True)
jbs = pd.DataFrame(jobs_to_post)
jbs = jbs[jbs.posted == "FALSE"].to_dict("records")
drive_handler, blog_handler = get_blogger_service_obj(credfile)

def preparepostdf(jobrecord):
    post_data  = post_body(
            company_logo= jobrecord["company_logo"],
            company= jobrecord["company"],
            location= jobrecord["location"],
            posting_time=jobrecord["posting_time"],
            details=jobrecord["details.job_desc_details"],
            application_link=jobrecord["application_link"],
            )
    post_meta = {
            'job_id':jobrecord["job_id"],
            'job_function' : jobrecord['details.jobcriterialist.Job function'],
            'job_industry' : jobrecord['details.jobcriterialist.Industries'],
            'job_seniority' : jobrecord['details.jobcriterialist.Seniority level'],
            'employment_type' : jobrecord['details.jobcriterialist.Employment type'],
            'job_title' : jobrecord['job_title']}
    return post_data,post_meta

for pst in jbs:
    try:   
        post_data,post_meta = preparepostdf(pst)
        print(f"publishing post {post_meta['job_title']}",end="\r")  
        # # labels generate
        job_functions_label = ['Other' if len(label) == 0 else label for label in set(cleanuplabel(label) for label in post_meta["job_function"].split(" ")) if label != 'Other']
        job_industry_labels = ['Other' if len(label) == 0 else label for label in set(cleanupindustry(label) for label in post_meta["job_industry"].split(" ")) if label != 'Other']
        # createjoblevels
        levels = createjoblevels(
            label = job_functions_label,
            seniority=post_meta['job_seniority'],
            employment_type = post_meta['employment_type'],
            industry = job_industry_labels)
        
        body_content = {
            "title": f'{post_meta["job_title"]} - {post_data["companyname"]}',
            "content": prep_post_template("./blogspot/", "post_template.html", post_data),
            "labels": levels,
            "publish": True,
        }
        postdetail = create_blog_post(BLOG_ID, blog_handler, body_content, isDraft=False) 
        update_publish_status(gd.gs.get_worksheet(2), post_meta["job_id"], True)
    except Exception as e:
        print(f"Error creating blog {e}")


# print(pst)
# 
