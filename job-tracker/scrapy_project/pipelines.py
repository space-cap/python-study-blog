from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models import JobPosting

class DatabasePipeline:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            job_posting = JobPosting(
                company_name=item.get('company_name'),
                job_title=item.get('job_title'),
                start_date=item.get('start_date'),
                end_date=item.get('end_date'),
                applicant_count=item.get('applicant_count', 0),
                requirements=item.get('requirements'),
                preferred_qualifications=item.get('preferred_qualifications'),
                location=item.get('location'),
                source_url=item.get('source_url')
            )
            session.add(job_posting)
            session.commit()
            spider.logger.info(f"Job posting saved: {item.get('job_title')}")
        except Exception as e:
            session.rollback()
            spider.logger.error(f"Error saving item: {e}")
        finally:
            session.close()
        
        return item