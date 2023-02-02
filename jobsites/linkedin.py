from bs4 import BeautifulSoup as bs
import datetime
import requests
import logging
logger = logging.getLogger(__name__)

class LinkedInScrap:
    def __init__(self,existing_jobs):
        self.existing_jobs = existing_jobs
    
    def check_exising_jobs(self,jobid):
        if jobid in self.existing_jobs:
            raise Exception(f"Job with ID '{jobid}' already exists,skipping...")
    
    @staticmethod
    def cleanupcriteria(df_json):
        result = {}
        for d in df_json:
            result.update(d)
        return result
    
    def external_link(self, job_link):
        """this function will return the external link if the job has been posted.


        Args:
            job_link (string): link to job to be scrapped.

        Returns:
            _type_: exact link redirect
        """
        resp = requests.get(job_link)
        soup = bs(resp.text, "html.parser")
        apply_btn_link = (
            soup.find(class_="sign-up-modal__direct-apply-on-company-site")
            .find("a")
            .get("href")
        )
        apply_btn_link = requests.get(apply_btn_link).url
        return apply_btn_link

    def searchlinkedinjobs(self, start=0):
        """this function will return the search result linkedin job search


        Args:
            start (int, optional): . Defaults to 0.

        Returns:
            response:
        """
        params = {
            # "keywords": "",
            "location": "Kenya",
            # "geoId": "100710459",
            # "trk": "public_jobs_jobs-search-bar_search-submit",
            "start": start,
        }
        response = requests.get(
            "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search",
            params=params,
        )
        return response
    
    
    def jobdetails_info(self, job_api_details):
        
        resp = requests.get(job_api_details)
        jobdesc = bs(resp.text, "html.parser")
        job_desc_details = jobdesc.find(
            class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5"
        )
        job_desc_details = str(job_desc_details).\
            replace('show-more-less-html__markup show-more-less-html__markup--clamp-after-5','job-desc').\
                replace("<p><br/></p>","")
        
        jobcriterialist = [
            {
                i.find(class_="description__job-criteria-subheader")
                .text.strip(): i.find(class_="description__job-criteria-subheader")
                .find_next_sibling()
                .text.strip()
            }
            for i in jobdesc.find(
                "ul", class_="description__job-criteria-list"
            ).find_all("li")
        ]
        jobcriterialist = LinkedInScrap.cleanupcriteria(jobcriterialist)

        out = {"jobcriterialist": jobcriterialist, "job_desc_details": job_desc_details}
        return out

    def jobdetails(self, listings):
        try:
            job_title = listings.find(class_="base-search-card__title").text.strip()
            company = listings.find(class_="base-search-card__subtitle").text.strip()
            # location     = listings.find(class_ = 'job-search-card__location').text.strip()
            job_link = listings.find(class_="base-card__full-link")
            if job_link:
                job_link = job_link.get("href")
                jobid = job_link.split("?")[0].split("-")[-1]
                self.check_exising_jobs(jobid)
            
                job_api_details = (
                    f"https://ke.linkedin.com/jobs-guest/jobs/api/jobPosting/{jobid}"
                )
                # get link to application
                print("Getting application details")
                application_link = self.external_link(job_link)
                logger.debug("Getting Job details")
                details = self.jobdetails_info(job_api_details)
            company_link = listings.find(class_="hidden-nested-link")
            if company_link:
                company_link = company_link.get("href")
            company_logo = (
                listings.find("div", class_="search-entity-media")
                .find("img")
                .get("data-delayed-url")
            )
            location = listings.find(class_="job-search-card__location").text.strip()
            posting_time = listings.time.get("datetime")
            res = {
                "job_title": job_title,
                "company": company,
                "job_link": job_link,
                "job_id": jobid,
                "application_link": application_link,
                "job_api_details": job_api_details,
                "company_logo": company_logo,
                "location": location,
                "posting_time": posting_time,
                "crawl_time": str(datetime.datetime.now()),
                # "url": response.url,
                "details": details,
            }
            
            return res
        except Exception as e:
            print(e)

    def main(self,end):
        start = 0
        jd = []
        while True:
            logger.debug("getting links")
            response = self.searchlinkedinjobs(start)
            soup = bs(response.text, 'html.parser').find_all("li")
            logger.debug("Parsing getting links")
            for i in range(len(soup)):
                print(f'{i} of {len(soup)}')
                new_jd = self.jobdetails(soup[i])
                jd.append(new_jd)
            start = start + 2
            logger.debug('current start', start,end = "\r")
            if start >= end:
                break  
        return jd
