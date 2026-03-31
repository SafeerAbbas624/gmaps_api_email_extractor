"""
Email Message Variations - 15 different messages for development services
Each message has the same context but different wording to avoid spam detection
"""

import random

# 15 different message variations (plain text + HTML)
EMAIL_MESSAGES = [
    {
        "subject": "Full-Stack Developer Available for Projects - Python, Flutter, Next.js & Node.js",
        "plain": """Hello,

I'm Safeer Abbas, a full-stack developer specializing in Python, Flutter, Next.js, and Node.js development.

I noticed your company and wanted to reach out about potential collaboration opportunities. I offer professional development services including:

- Web Application Development (Next.js, React, Node.js)
- Mobile App Development (Flutter - iOS & Android)
- Python Automation & Web Scraping Solutions
- Custom CRM & Business Management Systems
- API Development & Integration
- Data Analytics & Dashboard Development

With a strong portfolio of completed projects, I deliver reliable, scalable solutions on time and within budget.

Would you be interested in discussing how I can help with your development needs?

Portfolio: https://github.com/SafeerAbbas624

Best regards,
Safeer Abbas
Full-Stack Developer""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I'm <strong>Safeer Abbas</strong>, a full-stack developer specializing in Python, Flutter, Next.js, and Node.js development.</p><p>I noticed your company and wanted to reach out about potential collaboration opportunities. I offer professional development services including:</p><ul><li>Web Application Development (Next.js, React, Node.js)</li><li>Mobile App Development (Flutter - iOS & Android)</li><li>Python Automation & Web Scraping Solutions</li><li>Custom CRM & Business Management Systems</li><li>API Development & Integration</li><li>Data Analytics & Dashboard Development</li></ul><p>With a strong portfolio of completed projects, I deliver reliable, scalable solutions on time and within budget.</p><p>Would you be interested in discussing how I can help with your development needs?</p><p>Portfolio: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Best regards,<br><strong>Safeer Abbas</strong><br>Full-Stack Developer</p></body></html>"""
    },
    {
        "subject": "Looking to Partner? Expert Developer in Python, Flutter & Next.js",
        "plain": """Hi there,

My name is Safeer Abbas, and I'm a software developer with expertise in Python, Flutter, Next.js, and Node.js.

I work with businesses like yours to build custom software solutions that solve real problems. My services include:

- Custom Web Applications
- Cross-Platform Mobile Apps (Flutter)
- Automation Tools & Scrapers
- CRM Systems & Dashboards
- API Development & Third-Party Integrations

I've successfully delivered projects for startups, agencies, and established companies. I'm looking for new partnerships and would love to discuss how I could support your development needs.

Check out my work: https://github.com/SafeerAbbas624

Let me know if you'd like to chat!

Regards,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi there,</p><p>My name is <strong>Safeer Abbas</strong>, and I'm a software developer with expertise in Python, Flutter, Next.js, and Node.js.</p><p>I work with businesses like yours to build custom software solutions that solve real problems. My services include:</p><ul><li>Custom Web Applications</li><li>Cross-Platform Mobile Apps (Flutter)</li><li>Automation Tools & Scrapers</li><li>CRM Systems & Dashboards</li><li>API Development & Third-Party Integrations</li></ul><p>I've successfully delivered projects for startups, agencies, and established companies. I'm looking for new partnerships and would love to discuss how I could support your development needs.</p><p>Check out my work: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Let me know if you'd like to chat!</p><p>Regards,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Need a Developer? I Specialize in Web Apps, Mobile Apps & Automation",
        "plain": """Hello,

I'm reaching out because I believe my development skills could be valuable to your team.

I'm Safeer Abbas, a full-stack developer with experience in:

- Python (automation, scraping, data analysis)
- Flutter (cross-platform mobile apps)
- Next.js/React (modern web applications)
- Node.js (backend APIs and services)

Whether you need a one-time project completed or ongoing development support, I'm available and ready to help.

My recent work includes CRM systems, lead management platforms, and various automation tools. You can see examples at: https://github.com/SafeerAbbas624

Would you be open to a brief call to discuss your current or upcoming projects?

Best,
Safeer Abbas
Full-Stack Developer""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I'm reaching out because I believe my development skills could be valuable to your team.</p><p>I'm <strong>Safeer Abbas</strong>, a full-stack developer with experience in:</p><ul><li>Python (automation, scraping, data analysis)</li><li>Flutter (cross-platform mobile apps)</li><li>Next.js/React (modern web applications)</li><li>Node.js (backend APIs and services)</li></ul><p>Whether you need a one-time project completed or ongoing development support, I'm available and ready to help.</p><p>My recent work includes CRM systems, lead management platforms, and various automation tools. You can see examples at: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Would you be open to a brief call to discuss your current or upcoming projects?</p><p>Best,<br><strong>Safeer Abbas</strong><br>Full-Stack Developer</p></body></html>"""
    },
    {
        "subject": "Freelance Developer Available - Web, Mobile & Automation Expertise",
        "plain": """Hi,

Are you looking for a reliable developer for your next project?

I'm Safeer Abbas, a freelance full-stack developer offering:

- Web Development: Next.js, React, Node.js, TypeScript
- Mobile Development: Flutter for iOS and Android
- Automation: Python scripts, web scrapers, data pipelines
- Business Tools: Custom CRMs, dashboards, and analytics

I pride myself on clear communication, meeting deadlines, and delivering quality code.

I'm currently taking on new projects and would love to discuss how I can help your business.

Portfolio: https://github.com/SafeerAbbas624

Looking forward to connecting,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi,</p><p>Are you looking for a reliable developer for your next project?</p><p>I'm <strong>Safeer Abbas</strong>, a freelance full-stack developer offering:</p><ul><li>Web Development: Next.js, React, Node.js, TypeScript</li><li>Mobile Development: Flutter for iOS and Android</li><li>Automation: Python scripts, web scrapers, data pipelines</li><li>Business Tools: Custom CRMs, dashboards, and analytics</li></ul><p>I pride myself on clear communication, meeting deadlines, and delivering quality code.</p><p>I'm currently taking on new projects and would love to discuss how I can help your business.</p><p>Portfolio: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Looking forward to connecting,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Custom Software Development Services - Let's Build Something Great",
        "plain": """Hello,

I came across your company and thought my services might be a good fit for your development needs.

I'm Safeer Abbas, a software developer specializing in:

- Building scalable web applications with Next.js and React
- Creating cross-platform mobile apps using Flutter
- Developing automation solutions with Python
- Designing custom business management systems

I work with both startups and established companies, providing everything from MVP development to full-scale applications.

If you have any upcoming projects or need additional development resources, I'd be happy to discuss how I can help.

See my work: https://github.com/SafeerAbbas624

Cheers,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I came across your company and thought my services might be a good fit for your development needs.</p><p>I'm <strong>Safeer Abbas</strong>, a software developer specializing in:</p><ul><li>Building scalable web applications with Next.js and React</li><li>Creating cross-platform mobile apps using Flutter</li><li>Developing automation solutions with Python</li><li>Designing custom business management systems</li></ul><p>I work with both startups and established companies, providing everything from MVP development to full-scale applications.</p><p>If you have any upcoming projects or need additional development resources, I'd be happy to discuss how I can help.</p><p>See my work: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Cheers,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Experienced Developer Ready to Help with Your Projects",
        "plain": """Hello,

I'm Safeer Abbas, a professional developer with years of experience building web and mobile applications.

My core competencies include:

- Full-stack web development (Next.js, React, Node.js)
- Mobile app development (Flutter)
- Python automation and data solutions
- Custom business software and CRMs

I'm reaching out to see if you might need development support for any current or future projects. I work well with teams and can adapt to your workflows and requirements.

Take a look at my portfolio: https://github.com/SafeerAbbas624

I'd welcome the opportunity to discuss how I can contribute to your success.

Best regards,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I'm <strong>Safeer Abbas</strong>, a professional developer with years of experience building web and mobile applications.</p><p>My core competencies include:</p><ul><li>Full-stack web development (Next.js, React, Node.js)</li><li>Mobile app development (Flutter)</li><li>Python automation and data solutions</li><li>Custom business software and CRMs</li></ul><p>I'm reaching out to see if you might need development support for any current or future projects. I work well with teams and can adapt to your workflows and requirements.</p><p>Take a look at my portfolio: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>I'd welcome the opportunity to discuss how I can contribute to your success.</p><p>Best regards,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Web & Mobile Developer Seeking New Collaboration Opportunities",
        "plain": """Hi,

I hope this email finds you well. I'm Safeer Abbas, a software developer looking for new project opportunities.

I specialize in:

- Next.js and React web applications
- Flutter mobile apps (iOS & Android)
- Python-based automation and scraping
- Node.js backend development
- Custom CRM and management systems

I've worked with agencies, startups, and businesses across various industries. I'm flexible with engagement models - whether you need project-based work, retainer arrangements, or white-label services.

Portfolio: https://github.com/SafeerAbbas624

Would you be interested in learning more about how we could work together?

Thanks,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi,</p><p>I hope this email finds you well. I'm <strong>Safeer Abbas</strong>, a software developer looking for new project opportunities.</p><p>I specialize in:</p><ul><li>Next.js and React web applications</li><li>Flutter mobile apps (iOS & Android)</li><li>Python-based automation and scraping</li><li>Node.js backend development</li><li>Custom CRM and management systems</li></ul><p>I've worked with agencies, startups, and businesses across various industries. I'm flexible with engagement models - whether you need project-based work, retainer arrangements, or white-label services.</p><p>Portfolio: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Would you be interested in learning more about how we could work together?</p><p>Thanks,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Developer for Hire - Python, Flutter, Next.js Specialist",
        "plain": """Hello,

My name is Safeer Abbas and I'm a full-stack developer available for new projects.

What I bring to the table:

- Strong experience with Python, Flutter, Next.js, and Node.js
- Track record of delivering projects on time and within budget
- Clear communication and professional work ethic
- Ability to work independently or as part of your team

Recent projects include CRM systems, lead management platforms, web scrapers, and mobile applications.

I'm currently available for both short-term projects and long-term engagements.

View my work: https://github.com/SafeerAbbas624

Would love to hear about your development needs.

Best,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>My name is <strong>Safeer Abbas</strong> and I'm a full-stack developer available for new projects.</p><p>What I bring to the table:</p><ul><li>Strong experience with Python, Flutter, Next.js, and Node.js</li><li>Track record of delivering projects on time and within budget</li><li>Clear communication and professional work ethic</li><li>Ability to work independently or as part of your team</li></ul><p>Recent projects include CRM systems, lead management platforms, web scrapers, and mobile applications.</p><p>I'm currently available for both short-term projects and long-term engagements.</p><p>View my work: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Would love to hear about your development needs.</p><p>Best,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Need Development Help? I'm Here to Assist",
        "plain": """Hi there,

I noticed your company and wanted to introduce myself. I'm Safeer Abbas, a software developer specializing in building digital products.

My expertise includes:

- Web apps with Next.js, React, and TypeScript
- Mobile apps with Flutter
- Automation tools with Python
- Backend services with Node.js
- Data analytics and visualization

I enjoy tackling challenging projects and finding efficient solutions. Whether you're looking to build something new or enhance existing systems, I can help.

Check out my GitHub: https://github.com/SafeerAbbas624

Feel free to reach out if you'd like to discuss potential collaboration.

Regards,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi there,</p><p>I noticed your company and wanted to introduce myself. I'm <strong>Safeer Abbas</strong>, a software developer specializing in building digital products.</p><p>My expertise includes:</p><ul><li>Web apps with Next.js, React, and TypeScript</li><li>Mobile apps with Flutter</li><li>Automation tools with Python</li><li>Backend services with Node.js</li><li>Data analytics and visualization</li></ul><p>I enjoy tackling challenging projects and finding efficient solutions. Whether you're looking to build something new or enhance existing systems, I can help.</p><p>Check out my GitHub: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Feel free to reach out if you'd like to discuss potential collaboration.</p><p>Regards,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Professional Developer Services - Python, Flutter & Web Technologies",
        "plain": """Hello,

I'm Safeer Abbas, offering professional software development services.

I help businesses with:

- Custom web application development
- Cross-platform mobile app development
- Business process automation
- Data extraction and analysis tools
- API development and integration

My approach is straightforward: understand your requirements, deliver quality work, and maintain clear communication throughout the project.

I'm open to various collaboration models including fixed-price projects, hourly arrangements, or ongoing retainers.

See examples of my work: https://github.com/SafeerAbbas624

Let me know if you have any projects where I could be of help.

Best regards,
Safeer Abbas
Full-Stack Developer""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I'm <strong>Safeer Abbas</strong>, offering professional software development services.</p><p>I help businesses with:</p><ul><li>Custom web application development</li><li>Cross-platform mobile app development</li><li>Business process automation</li><li>Data extraction and analysis tools</li><li>API development and integration</li></ul><p>My approach is straightforward: understand your requirements, deliver quality work, and maintain clear communication throughout the project.</p><p>I'm open to various collaboration models including fixed-price projects, hourly arrangements, or ongoing retainers.</p><p>See examples of my work: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Let me know if you have any projects where I could be of help.</p><p>Best regards,<br><strong>Safeer Abbas</strong><br>Full-Stack Developer</p></body></html>"""
    },
    {
        "subject": "Expand Your Development Capacity - Experienced Full-Stack Developer",
        "plain": """Hi,

Do you ever find yourself needing extra development capacity? I might be able to help.

I'm Safeer Abbas, a full-stack developer with expertise in:

- Modern web frameworks (Next.js, React, Node.js)
- Mobile development (Flutter for iOS/Android)
- Python automation and scripting
- Database design and optimization
- Third-party API integrations

I've helped companies of all sizes deliver their projects successfully. I can work as an extension of your existing team or handle projects independently.

GitHub: https://github.com/SafeerAbbas624

Would you be open to a quick conversation about your development needs?

Thanks,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi,</p><p>Do you ever find yourself needing extra development capacity? I might be able to help.</p><p>I'm <strong>Safeer Abbas</strong>, a full-stack developer with expertise in:</p><ul><li>Modern web frameworks (Next.js, React, Node.js)</li><li>Mobile development (Flutter for iOS/Android)</li><li>Python automation and scripting</li><li>Database design and optimization</li><li>Third-party API integrations</li></ul><p>I've helped companies of all sizes deliver their projects successfully. I can work as an extension of your existing team or handle projects independently.</p><p>GitHub: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>Would you be open to a quick conversation about your development needs?</p><p>Thanks,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Your Next Developer? Expertise in Web, Mobile & Automation",
        "plain": """Hello,

I'm exploring new opportunities to work with forward-thinking companies, and I thought I'd reach out.

I'm Safeer Abbas, a developer with a strong background in:

- Building responsive web applications
- Developing cross-platform mobile apps
- Creating automation solutions that save time
- Integrating systems and APIs
- Analyzing and visualizing data

My goal is always to deliver solutions that actually solve problems and add value to your business.

Feel free to check out my recent work: https://github.com/SafeerAbbas624

If you're looking for development support, I'd love to chat.

Best,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I'm exploring new opportunities to work with forward-thinking companies, and I thought I'd reach out.</p><p>I'm <strong>Safeer Abbas</strong>, a developer with a strong background in:</p><ul><li>Building responsive web applications</li><li>Developing cross-platform mobile apps</li><li>Creating automation solutions that save time</li><li>Integrating systems and APIs</li><li>Analyzing and visualizing data</li></ul><p>My goal is always to deliver solutions that actually solve problems and add value to your business.</p><p>Feel free to check out my recent work: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>If you're looking for development support, I'd love to chat.</p><p>Best,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Reliable Developer for Your Web & Mobile Projects",
        "plain": """Hi,

I wanted to briefly introduce myself and my services.

I'm Safeer Abbas, a software developer focused on delivering practical, working solutions. My tech stack includes:

- Frontend: Next.js, React, TypeScript
- Mobile: Flutter (iOS & Android)
- Backend: Node.js, Python
- Automation: Web scraping, data processing, task automation

I value reliability and clear communication. When I commit to a project, I see it through.

Take a look at some of my projects: https://github.com/SafeerAbbas624

If you have development needs, let's connect and discuss how I can help.

Regards,
Safeer Abbas
Software Developer""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi,</p><p>I wanted to briefly introduce myself and my services.</p><p>I'm <strong>Safeer Abbas</strong>, a software developer focused on delivering practical, working solutions. My tech stack includes:</p><ul><li>Frontend: Next.js, React, TypeScript</li><li>Mobile: Flutter (iOS & Android)</li><li>Backend: Node.js, Python</li><li>Automation: Web scraping, data processing, task automation</li></ul><p>I value reliability and clear communication. When I commit to a project, I see it through.</p><p>Take a look at some of my projects: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>If you have development needs, let's connect and discuss how I can help.</p><p>Regards,<br><strong>Safeer Abbas</strong><br>Software Developer</p></body></html>"""
    },
    {
        "subject": "Software Development Partnership Opportunity",
        "plain": """Hello,

I'm writing to introduce myself as a potential development partner for your business.

My name is Safeer Abbas, and I offer comprehensive software development services:

- Custom web application development
- Mobile app development with Flutter
- Python-based automation and tools
- API development and system integration
- Data dashboards and analytics

I've completed numerous projects across different industries and am always looking to build new, lasting professional relationships.

View my portfolio: https://github.com/SafeerAbbas624

I'd appreciate the opportunity to discuss any upcoming projects or ongoing development needs you might have.

Thank you for your time,
Safeer Abbas""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hello,</p><p>I'm writing to introduce myself as a potential development partner for your business.</p><p>My name is <strong>Safeer Abbas</strong>, and I offer comprehensive software development services:</p><ul><li>Custom web application development</li><li>Mobile app development with Flutter</li><li>Python-based automation and tools</li><li>API development and system integration</li><li>Data dashboards and analytics</li></ul><p>I've completed numerous projects across different industries and am always looking to build new, lasting professional relationships.</p><p>View my portfolio: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>I'd appreciate the opportunity to discuss any upcoming projects or ongoing development needs you might have.</p><p>Thank you for your time,<br><strong>Safeer Abbas</strong></p></body></html>"""
    },
    {
        "subject": "Available for Development Projects - Full-Stack Expertise",
        "plain": """Hi there,

I hope you're having a great day. I'm Safeer Abbas, a full-stack developer reaching out about potential project opportunities.

My skills cover:

- Web Development: Next.js, React, Node.js, TypeScript
- Mobile Development: Flutter for cross-platform apps
- Automation: Python scripts, scrapers, and bots
- Business Tools: CRMs, dashboards, admin panels

I work with businesses to transform ideas into functional software. From MVPs to full-scale applications, I can handle the entire development lifecycle.

See my work here: https://github.com/SafeerAbbas624

If you have any projects in mind, I'd be happy to discuss how I could contribute.

Best regards,
Safeer Abbas
Full-Stack Developer""",
        "html": """<html><body style="font-family: Arial, sans-serif; color: #333;"><p>Hi there,</p><p>I hope you're having a great day. I'm <strong>Safeer Abbas</strong>, a full-stack developer reaching out about potential project opportunities.</p><p>My skills cover:</p><ul><li>Web Development: Next.js, React, Node.js, TypeScript</li><li>Mobile Development: Flutter for cross-platform apps</li><li>Automation: Python scripts, scrapers, and bots</li><li>Business Tools: CRMs, dashboards, admin panels</li></ul><p>I work with businesses to transform ideas into functional software. From MVPs to full-scale applications, I can handle the entire development lifecycle.</p><p>See my work here: <a href="https://github.com/SafeerAbbas624">https://github.com/SafeerAbbas624</a></p><p>If you have any projects in mind, I'd be happy to discuss how I could contribute.</p><p>Best regards,<br><strong>Safeer Abbas</strong><br>Full-Stack Developer</p></body></html>"""
    },
]

def get_random_message():
    """Return a random message from the list"""
    return random.choice(EMAIL_MESSAGES)

