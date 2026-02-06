from django.core.management.base import BaseCommand
from core.models import Job, Company
from authentication.models import User
import json


class Command(BaseCommand):
    help = 'Seed the database with sample jobs'

    def handle(self, *args, **kwargs):
        jobs_data = [
            {
                "title": "Senior Frontend Engineer",
                "company": "TechFlow Systems",
                "location": "San Francisco, CA (Remote)",
                "type": "Full-time",
                "experience_level": "Senior",
                "salary_range": "$140k - $180k",
                "description": "We are looking for an experienced React developer to lead our dashboard team.",
                "requirements": ["React", "TypeScript", "Redux", "CSS3", "Git"],
                "benefits": ["Remote work", "Health insurance", "401k"]
            },
            {
                "title": "Backend Python Developer",
                "company": "DataMinds AI",
                "location": "New York, NY",
                "type": "Full-time",
                "experience_level": "Mid-Level",
                "salary_range": "$120k - $150k",
                "description": "Join our AI team to build robust APIs using FastAPI and Python.",
                "requirements": ["Python", "FastAPI", "SQL", "Docker", "AWS"],
                "benefits": ["Stock options", "Gym stipend", "Catered lunch"]
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupX",
                "location": "Austin, TX",
                "type": "Contract",
                "experience_level": "Entry-Level",
                "salary_range": "$80k - $100k",
                "description": "Early stage startup looking for a generalist to build our MVP.",
                "requirements": ["JavaScript", "Node.js", "React", "MongoDB"],
                "benefits": ["Flexible hours", "Learning budget"]
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudScale",
                "location": "Remote",
                "type": "Full-time",
                "experience_level": "Senior",
                "salary_range": "$150k - $200k",
                "description": "Manage our Kubernetes clusters and CI/CD pipelines.",
                "requirements": ["Kubernetes", "Terraform", "AWS", "CI/CD", "Python"],
                "benefits": ["Unlimited PTO", "Home office stipend"]
            },
            {
                "title": "Machine Learning Engineer",
                "company": "Visionary AI",
                "location": "Seattle, WA",
                "type": "Full-time",
                "experience_level": "Senior",
                "salary_range": "$170k - $220k",
                "description": "Build computer vision models for autonomous vehicles.",
                "requirements": ["Python", "PyTorch", "TensorFlow", "C++", "Computer Vision"],
                "benefits": ["Relocation assistance", "Bonus"]
            },
            {
                "title": "Product Designer",
                "company": "Creative Solutions",
                "location": "Los Angeles, CA",
                "type": "Full-time",
                "experience_level": "Mid-Level",
                "salary_range": "$110k - $140k",
                "description": "Design intuitive user interfaces for our crypto wallet app.",
                "requirements": ["Figma", "UI/UX", "Prototyping", "User Research"],
                "benefits": ["Crypto bonus", "Health"]
            },
            {
                "title": "Go Backend Engineer",
                "company": "FastPay",
                "location": "Chicago, IL",
                "type": "Full-time",
                "experience_level": "Senior",
                "salary_range": "$160k - $190k",
                "description": "High performance payment processing systems.",
                "requirements": ["Go", "Microservices", "gRPC", "PostgreSQL"],
                "benefits": ["401k match", "Dental"]
            },
            {
                "title": "Junior Web Developer",
                "company": "Local Agency",
                "location": "Miami, FL",
                "type": "Full-time",
                "experience_level": "Junior",
                "salary_range": "$60k - $80k",
                "description": "Maintain client websites and build landing pages.",
                "requirements": ["HTML", "CSS", "JavaScript", "WordPress"],
                "benefits": ["Mentorship", "Chill culture"]
            },
            {
                "title": "Data Scientist",
                "company": "HealthAnalytica",
                "location": "Boston, MA",
                "type": "Full-time",
                "experience_level": "PhD",
                "salary_range": "$180k - $250k",
                "description": "Analyze clinical trial data to improve patient outcomes.",
                "requirements": ["Python", "R", "Statistics", "Machine Learning"],
                "benefits": ["Research budget", "Conference travel"]
            },
            {
                "title": "React Native Developer",
                "company": "MobileFirst",
                "location": "Remote",
                "type": "Contract",
                "experience_level": "Mid-Level",
                "salary_range": "$60/hr",
                "description": "Help us ship our iOS and Android app before Q4.",
                "requirements": ["React Native", "Redux", "Mobile Development"],
                "benefits": []
            }
        ]

        # Get or create a recruiter user
        recruiter, created = User.objects.get_or_create(
            email='recruiter@seed.com',
            defaults={
                'username': 'recruiter@seed.com',
                'first_name': 'Seed',
                'last_name': 'Recruiter',
                'role': 'recruiter'
            }
        )
        if created:
            recruiter.set_password('password123')
            recruiter.save()
            self.stdout.write(self.style.SUCCESS('Created seed recruiter user'))

        # Create candidate user 'ppp'
        candidate, created = User.objects.get_or_create(
            email='mrparsa00@gmail.com',
            defaults={
                'username': 'mrparsa00@gmail.com',
                'first_name': 'ppp',
                'role': 'candidate'
            }
        )
        if created:
            candidate.set_password('password123')
            candidate.save()
            self.stdout.write(self.style.SUCCESS("Created candidate 'ppp'"))

        # Create another test candidate
        candidate2, created = User.objects.get_or_create(
            email='candidate@test.com',
            defaults={
                'username': 'candidate@test.com',
                'first_name': 'Test',
                'last_name': 'Candidate',
                'role': 'candidate'
            }
        )
        if created:
            candidate2.set_password('password123')
            candidate2.save()
            self.stdout.write(self.style.SUCCESS('Created test candidate user'))

        jobs_created = 0
        for job_data in jobs_data:
            # Get or create company
            company, _ = Company.objects.get_or_create(
                name=job_data['company'],
                defaults={
                    'user': recruiter,
                    'location': job_data['location']
                }
            )

            # Create job
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                company=company,
                defaults={
                    'location': job_data['location'],
                    'type': job_data['type'],
                    'experience_level': job_data['experience_level'],
                    'salary_range': job_data['salary_range'],
                    'description': job_data['description'],
                    'requirements': job_data['requirements'],
                    'benefits': job_data['benefits']
                }
            )

            if created:
                jobs_created += 1
                self.stdout.write(f"Created job: {job.title} at {company.name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {jobs_created} jobs!'))
