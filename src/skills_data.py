"""
Job Search Skills Assessment - Data Layer
Holds category/question definitions and feedback text.
"""

# Detailed feedback for each question based on rating (1-5)
# Structure: {category_id: {question_index: {rating: "feedback text"}}}
DETAILED_FEEDBACK = {
    "skills_abilities": {
        0: {  # I know the skills and qualities employers are looking for
            1: "Start by researching job descriptions in your target field. Make a list of the top 5 skills mentioned repeatedly. Use job boards like Indeed or LinkedIn to analyze at least 10-15 postings.",
            2: "You have some awareness but need to deepen your research. Create a spreadsheet comparing skills across different companies in your industry. Look for patterns and prioritize the most in-demand skills.",
            3: "Good foundation! Now refine your understanding by networking with professionals in your target roles. Ask them what skills they value most. Consider joining industry groups on LinkedIn for insights.",
            4: "Strong knowledge! Stay current by following industry blogs, newsletters, and thought leaders. Update your skills list quarterly to reflect market changes.",
            5: "Excellent! You're well-informed. Share your knowledge by mentoring others or writing about industry trends. This positions you as a thought leader and strengthens your professional brand."
        },
        1: {  # I have developed a list of skills on my CV
            1: "Create your skills inventory immediately. List every skill from past roles, education, and hobbies. Don't filter yet—brainstorm first. Then categorize them as technical, soft, or transferable skills.",
            2: "Build on your initial list by quantifying achievements. For each skill, note a specific example of when you used it successfully. This makes your CV more compelling and interview-ready.",
            3: "Good start! Now work on articulating these skills concisely. Practice your '30-second pitch' for each major skill. Ask a mentor or career counselor to review your CV for clarity and impact.",
            4: "Well-developed! Enhance your CV by adding metrics and outcomes. Instead of 'managed projects,' say 'managed 5+ projects worth £500K, delivering 90% on time.' Numbers speak louder.",
            5: "Outstanding! Your CV clearly showcases your value. Keep it updated monthly. Consider creating different versions tailored to specific job types for maximum impact."
        },
        2: {  # I know job titles and locations
            1: "Research is critical. Use job boards to explore titles related to your skills. Save 20+ job postings and analyze their requirements. Note which locations have the most opportunities.",
            2: "Expand your search. Look beyond obvious titles—similar roles can have different names across industries. Research regional job markets. Some areas may offer better opportunities than others.",
            3: "Solid awareness! Now prioritize. Rank job titles by preference and opportunity volume. Use LinkedIn's job search to see where these roles are concentrated. Consider relocation possibilities.",
            4: "Excellent research! Create alerts for your target titles and locations. Network with professionals in those areas. Understanding the local market gives you a competitive edge in interviews.",
            5: "You're extremely well-prepared! Use your knowledge strategically. Focus on areas with growth potential. Consider less competitive markets where your skills might be in higher demand."
        },
        3: {  # I know my transferable skills
            1: "Start identifying transferable skills immediately. Common ones include communication, problem-solving, teamwork, and time management. List skills you've used across different contexts (work, volunteering, hobbies).",
            2: "You've identified some, but dig deeper. Every role has transferable elements. Analyze past projects: What skills were required? How can they apply to other industries? Create a comprehensive transferable skills list.",
            3: "Good progress! Now practice articulating how your skills transfer. Use the formula: 'In my previous role as [X], I developed [skill], which applies to [target role] because...'",
            4: "Strong understanding! Prepare specific examples showing how you've successfully applied these skills in varied contexts. This demonstrates adaptability—a highly valued trait.",
            5: "Exceptional! You understand the power of transferable skills. Use this in networking and interviews to show versatility. Consider consulting or contract work to leverage this strength."
        },
        4: {  # I have a 60-second commercial prepared
            1: "Create your elevator pitch today. Structure: Who you are + What you do + Key strengths + What you're seeking. Write it out, then practice until it feels natural, not rehearsed.",
            2: "You have something, but it needs refinement. Test it on friends or mentors. Is it clear? Compelling? Under 60 seconds? Record yourself and critique your delivery. Adjust and practice.",
            3: "Good foundation! Now add a 'hook'—something memorable. Maybe a notable achievement or unique combination of skills. Practice different versions for networking events vs. formal interviews.",
            4: "Well-crafted! Ensure you can adapt it for different audiences. The pitch for a recruiter differs from one for a hiring manager. Practice variations and be ready to expand on any point.",
            5: "Outstanding! Your pitch is polished and professional. Use it confidently in every networking opportunity. Consider teaching others how to create their pitches—reinforcing your own mastery."
        },
        5: {  # I'm aware of areas needing improvement
            1: "Self-awareness is crucial for growth. Conduct an honest self-assessment. Ask former colleagues or managers for feedback. Identify 3-5 areas where you could improve and prioritize them.",
            2: "You've identified some gaps, but need an action plan. For each area, research how to improve: online courses, books, practice, mentorship? Set specific, measurable goals with deadlines.",
            3: "Good self-awareness! You've identified gaps and started working on them. Track your progress monthly. Celebrate small wins. Consider finding an accountability partner to keep you motivated.",
            4: "Excellent! You're actively developing your weak areas. Document your improvement journey—it makes great interview material. 'I recognized X was a weakness, so I...' shows initiative and growth mindset.",
            5: "Exemplary self-improvement mindset! You're continuously evolving. Share your learning journey on LinkedIn. Teaching others what you've learned reinforces your own knowledge and builds your professional brand."
        }
    },
    "job_search": {
        0: {  # I know effective/ineffective job search methods
            1: "Learn the facts: networking yields 70% of jobs, while job boards account for only 15-20%. Research the 'hidden job market.' Start by reading job search strategy guides or watching career expert videos.",
            2: "You have basic knowledge but need to go deeper. Understand why some methods work better: direct networking, company websites, LinkedIn outreach. Create a strategy mixing multiple effective approaches.",
            3: "Solid understanding! Now optimize your approach. Spend 70% of time on high-yield activities (networking, targeted applications) and only 30% on job boards. Track what methods generate responses.",
            4: "Excellent knowledge! You're using evidence-based strategies. Share your insights with other job seekers. Teaching others reinforces your expertise and expands your network simultaneously.",
            5: "You're a job search strategist! Your sophisticated understanding gives you a major advantage. Consider writing about or presenting on effective job search methods to establish thought leadership."
        },
        1: {  # I'm willing to devote 6+ hours daily
            1: "Job searching IS a full-time job. Commit to treating it seriously. Create a daily schedule: 2 hours researching, 2 hours applying, 2 hours networking. Consistency beats sporadic intensive effort.",
            2: "Increase your commitment. Six hours daily significantly increases success odds. Block time on your calendar. Treat job search appointments as seriously as you would actual work meetings.",
            3: "Good dedication! Maintain this momentum. Ensure you're using time effectively, not just filling hours. Quality applications beat quantity. Take breaks to avoid burnout.",
            4: "Excellent commitment! You're giving yourself the best chance. Make sure those hours are productive: mix research, applications, networking, and skill development. Track your daily activities.",
            5: "Outstanding dedication! Your commitment will pay off. Ensure you're balancing intensity with self-care. Job searching is exhausting. Schedule downtime to maintain energy and positivity throughout your search."
        },
        2: {  # I know which vacancies are popular
            1: "Start tracking market trends. Use job boards with filtering by 'most applied' or 'trending.' Follow industry news and LinkedIn analytics. Understanding demand helps you position yourself strategically.",
            2: "Build on your awareness by analyzing why certain roles are popular. Is it industry growth? New technology? Seasonal patterns? This insight helps you time applications and identify emerging opportunities.",
            3: "Good market awareness! Now use this knowledge strategically. Apply early to popular positions—competition increases over time. Consider similar but less saturated roles with better odds.",
            4: "Strong market intelligence! You understand demand patterns. Use this to negotiate timing and compensation. Knowing a role is in-demand strengthens your position in salary discussions.",
            5: "Exceptional market knowledge! You're ahead of trends. Consider roles before they become saturated. Your timing and positioning give you a significant competitive advantage. Share insights to network effectively."
        },
        3: {  # I know how to use the internet for job search
            1: "Master online job search fundamentals. Start with major boards (Indeed, LinkedIn, Glassdoor). Learn advanced search features: Boolean operators, location filters, salary ranges. Take free online tutorials.",
            2: "Expand beyond basics. Research company career pages, industry-specific job boards, Google for Jobs. Learn to set up job alerts. Explore lesser-known resources like company reviews and salary comparison sites.",
            3: "Solid internet skills! Now optimize. Use LinkedIn to research hiring managers. Check company social media for culture insights. Set up RSS feeds or Google Alerts for targeted opportunities.",
            4: "Excellent online research skills! You're using multiple channels effectively. Teach others your methods. Deepen your knowledge of advanced LinkedIn features like Boolean search and connection strategies.",
            5: "You're an expert digital job searcher! Your comprehensive approach maximizes opportunities. Consider creating content about online job search strategies—establishing yourself as a resource attracts opportunities organically."
        },
        4: {  # I know at least three job search sites
            1: "Immediately register on Indeed, LinkedIn, and Glassdoor. Complete your profiles fully—partial profiles reduce recruiter contact. Upload your CV and set up job alerts for your target roles.",
            2: "Good start! Add niche sites specific to your industry: Dice (tech), AngelList (startups), MediaBistro (media), etc. Different sites attract different employers. Diversify your presence.",
            3: "You're using multiple sites—excellent! Now optimize each profile for keywords. Ensure consistency across platforms. Regularly update and engage (comment, share) to increase visibility to recruiters.",
            4: "Strong multi-platform presence! Leverage each site's unique features: LinkedIn for networking, Indeed for volume, Glassdoor for company research. Check all daily for new opportunities.",
            5: "Exceptional coverage! Your comprehensive presence across multiple platforms maximizes recruiter discovery. You're leveraging passive job search effectively. Continue maintaining and updating these profiles for ongoing visibility."
        },
        5: {  # I know what services help with employment
            1: "Research available support immediately. Government services (JobCentre Plus), career coaching, professional associations, alumni networks, and nonprofit job programs. Many offer free resume reviews and interview prep.",
            2: "You know some resources but explore further. Look into: recruitment agencies, professional mentoring programs, industry networking events, online courses (LinkedIn Learning, Coursera), and local workshops.",
            3: "Good awareness of available help! Now actively use these services. Attend workshops, connect with recruiters, join professional groups. Don't go alone—leveraging support dramatically improves outcomes.",
            4: "Excellent! You're making good use of support services. Maximize value by being prepared: bring specific questions, follow up on advice, and stay engaged with programs offering ongoing support.",
            5: "You're leveraging all available resources brilliantly! Your strategic use of support services accelerates your search. Consider giving back by volunteering with job seeker programs once you're employed."
        }
    },
    "job_applications": {
        0: {  # I know how to complete applications completely
            1: "Learn proper application procedures. Read instructions carefully every time. Create a checklist: all fields filled, documents attached, questions answered fully. Practice with 2-3 applications before submitting real ones.",
            2: "You understand basics but make errors. Slow down. Use a systematic approach: read the entire application first, gather all needed info, then complete it. Never rush—incomplete applications are often automatically rejected.",
            3: "Good competency! Ensure you're tailoring each application. Generic submissions stand out negatively. Reference the specific role and company in your answers. Show you've done research.",
            4: "Excellent application skills! You're thorough and accurate. Continue this precision. Consider creating templates for common questions, but always customize. Your attention to detail shows professionalism.",
            5: "Outstanding! Your applications are complete, accurate, and compelling. This professionalism sets you apart. Share your process with others. Teaching reinforces your expertise and builds your network."
        },
        1: {  # I review applications before submitting
            1: "Make this a non-negotiable habit. After completing an application, take a 15-minute break, then review with fresh eyes. Check for typos, incomplete fields, and attached documents. Mistakes cost opportunities.",
            2: "You sometimes review but be more consistent. Create a checklist: spelling, grammar, all fields complete, documents attached, consistency with CV, customization for this role. Check every box before submitting.",
            3: "Good practice! Enhance by reading aloud—this catches errors your eyes miss. Better yet, use text-to-speech tools. Consider having someone else review critical applications.",
            4: "Excellent attention to detail! Your review process catches errors others miss. This professionalism reflects well on you. Continue this practice—it consistently improves application quality.",
            5: "Exemplary! Your thorough review process ensures polished applications. Your professionalism shows in every submission. This habit serves you throughout your career, not just in job searching."
        },
        2: {  # I know what to bring to interviews
            1: "Research and prepare immediately. Standard items: multiple CV copies, reference list, portfolio/work samples if relevant, notepad and pen, questions for interviewer, company research notes. Create a professional folder.",
            2: "You have basics but refine your approach. Add: prepared examples of your work, certificates/qualifications, business cards if you have them. Organize everything the night before. Arrive over-prepared.",
            3: "Good preparation! Consider role-specific additions: designers bring portfolios, teachers bring lesson plans, salespeople bring sales records. Tailor what you bring to demonstrate relevant competencies.",
            4: "Excellent! You're thoroughly prepared. Ensure everything is organized professionally—appearance matters. Your preparation level impresses interviewers before you even speak.",
            5: "Outstanding preparation! You arrive fully equipped for any question or request. Your professionalism sets the tone immediately. This habit demonstrates organizational skills and seriousness about the opportunity."
        },
        3: {  # I know how to apply online with email attachments
            1: "Master this essential skill now. Learn proper file naming: 'FirstName_LastName_CV.pdf' not 'resume.doc'. Convert to PDF. Keep file sizes reasonable. Practice sending test emails to yourself first.",
            2: "You understand basics but refine your technique. Write professional email text—don't just attach files to a blank email. Craft a brief, compelling message. Always include a subject line that references the position.",
            3: "Solid online application skills! Now optimize: personalize each email, reference the job posting, highlight 1-2 key qualifications. Ensure your email signature is professional with contact details.",
            4: "Excellent email application skills! Your professionalism shows in every detail. Continue this standard. Follow up appropriately if you haven't heard back within the stated timeframe.",
            5: "Perfect! Your email applications are polished and professional. You understand proper etiquette, formatting, and follow-up. This digital professionalism makes strong first impressions consistently."
        },
        4: {  # I know how to log job search activities
            1: "Start tracking immediately. Create a spreadsheet: columns for company, position, date applied, contact person, follow-up dates, status. This prevents duplicates and enables follow-ups. Templates are available online.",
            2: "You track somewhat but improve your system. Add: where you found the job, customization notes, interview dates/outcomes, next steps. Comprehensive records help you learn what works and ensure timely follow-ups.",
            3: "Good tracking system! Now use it strategically. Analyze patterns: which sources yield interviews? What application types succeed? Review weekly to optimize your approach and ensure no follow-ups are missed.",
            4: "Excellent tracking! Your organized records enable strategic decisions. You know what's working and can adjust accordingly. Your system ensures professional follow-up timing and prevents awkward duplicate applications.",
            5: "Exemplary record-keeping! Your systematic approach maximizes efficiency and prevents errors. You can report your search activities professionally if required. This organizational skill impresses throughout your career."
        },
        5: {  # I can explain gaps in my CV
            1: "Prepare explanations immediately. Gaps aren't necessarily negative. Focus on what you did: care responsibilities, skill development, health recovery, travel, volunteering. Be honest but positive. Practice your explanation.",
            2: "You have some explanation but strengthen it. Frame gaps positively: 'I took time to...' not 'I was unemployed.' Highlight any skills gained. If possible, show productive use of time: courses, volunteering, freelancing.",
            3: "Good framing! Ensure consistency—your application and interview explanations should match. Practice concise delivery (30 seconds max), then smoothly transition to your qualifications. Don't dwell on gaps.",
            4: "Excellent gap explanation! You're honest, concise, and positive. You've turned potential negatives into demonstrations of resilience or growth. Your confidence in addressing this shows maturity.",
            5: "Perfect handling of CV gaps! Your honest, positive explanations demonstrate integrity and growth mindset. You've effectively neutralized potential concerns, allowing interviewers to focus on your qualifications and potential."
        },
        6: {  # I can highlight employer's needs in applications
            1: "Learn to analyze job postings. Highlight key requirements. In your application, explicitly address each: 'You require X. I offer Y, demonstrated by Z.' Mirror their language. Show you understand their needs.",
            2: "You somewhat address their needs but be more explicit. Use the job description as a checklist. Create a two-column table: their requirement | your match. Include this thinking in your cover letter.",
            3: "Good job matching! Now enhance by researching beyond the job ad. Study the company's challenges, goals, and culture. Address how you'll contribute to their specific situation, not just meet generic requirements.",
            4: "Excellent needs alignment! You demonstrate clear understanding of employer priorities. Your applications show research and genuine interest. This strategic approach significantly increases interview invitations.",
            5: "Outstanding! You perfectly align your qualifications with employer needs. Your research-driven, customized applications demonstrate high emotional intelligence and strategic thinking. You're positioning yourself as the solution they need."
        }
    },
    "effective_cvs": {
        0: {  # I have a current, effective CV ready
            1: "Create or update your CV immediately. Use a clean, professional template. Essential sections: contact info, professional summary, work experience (reverse chronological), education, skills. Print 5 copies on quality white paper.",
            2: "Your CV exists but needs work. Ensure it's no more than 2 pages. Remove outdated info (graduation dates >15 years ago). Update contact details. Proofread thoroughly. Get it professionally printed on quality paper.",
            3: "Good CV foundation! Now optimize: use action verbs, quantify achievements, tailor your professional summary. Ensure consistent formatting. Save as PDF. Keep a 'master' version and customize copies for specific applications.",
            4: "Excellent CV! It's current, professional, and ready to send. Continue updating after every significant achievement. Maintain both digital and printed copies. Your preparation shows professionalism and confidence.",
            5: "Perfect! Your CV is polished, current, and compelling. You're always opportunity-ready. This level of preparation is exceptional. Your CV likely requires only minor customization for specific applications."
        },
        1: {  # I've had 3+ people review my CV
            1: "Get feedback immediately. Ask colleagues, mentors, career counselors, or professional recruiters to review. Different perspectives catch different issues. Accept criticism graciously—it improves your CV.",
            2: "You've had some review but seek more diverse feedback. Include someone in your target industry, a recruiter, and a professional writer if possible. Fresh eyes catch errors you've become blind to.",
            3: "Good validation! Ensure reviewers represent different perspectives: industry insider, recruiter, grammar expert. Synthesize their feedback thoughtfully. Not all advice is equal—prioritize industry insider insights.",
            4: "Excellent peer review process! You've incorporated diverse feedback effectively. Your CV has been tested and refined. Continue this practice when making significant updates—multiple perspectives prevent blind spots.",
            5: "Exemplary approach! Your CV has been thoroughly vetted by qualified reviewers. You've synthesized feedback wisely, maintaining your authentic voice while optimizing impact. This collaborative approach ensures professional quality."
        },
        2: {  # I know what employers look for in CVs
            1: "Research this critical knowledge. Employers scan for: relevant experience, quantified achievements, skills matching job description, clear formatting, no errors. Read articles by recruiters. Study successful CV examples in your field.",
            2: "You have general ideas but deepen your knowledge. Understand that recruiters spend 6-7 seconds on initial scan. What catches their eye? Keywords matching job description, measurable results, progressive responsibility, clean layout.",
            3: "Solid understanding! Now apply it consistently. Ensure your CV leads with strengths, uses industry keywords, quantifies achievements (percentages, amounts, numbers), and shows career progression. Make your value immediately obvious.",
            4: "Excellent knowledge! You understand recruiter psychology and CV scanning technology (ATS). Your CV is optimized for both. Continue staying current—hiring practices evolve. What worked 5 years ago may not work today.",
            5: "Expert level! You understand precisely how modern hiring works: ATS systems, recruiter scanning patterns, hiring manager priorities. Your sophisticated knowledge ensures your CV performs optimally at every stage."
        },
        3: {  # I know how to upload a CV to a website
            1: "Learn this essential skill immediately. Practice on major job sites. Typical process: Create account > Go to profile/settings > Upload CV > Browse files > Select your PDF > Upload. Test on Indeed and LinkedIn today.",
            2: "You've done it but may struggle with variations. Practice on multiple platforms. Understand common issues: file size limits, acceptable formats (PDF usually best), how to replace existing CVs. Save files properly named.",
            3: "Good technical competency! Now optimize: some sites parse CV data into profile fields—verify accuracy after upload. Understand when to use upload vs. paste vs. manual entry. Each method has advantages.",
            4: "Excellent upload skills! You navigate different platforms confidently. You understand file formatting, size requirements, and profile optimization. Your technical fluency streamlines your application process significantly.",
            5: "Perfect mastery! You efficiently upload and optimize CVs across all platforms. You understand how to maximize visibility through proper formatting and keyword optimization. Your technical skills remove barriers to applying widely."
        },
        4: {  # My CV is on 2+ job search websites
            1: "Post your CV immediately on Indeed and LinkedIn at minimum. Complete profiles fully—partial profiles reduce recruiter contact. Upload your best CV. Set up job alerts. Check daily for recruiter messages.",
            2: "You're on some sites but expand your presence. Add your CV to: Reed, Totaljobs, CV-Library, Glassdoor, and industry-specific sites. More visibility means more recruiter contacts and opportunities.",
            3: "Good multi-platform presence! Ensure profiles are consistent and complete. Refresh your CV monthly (update the date)—this bumps you in search results. Respond promptly to all recruiter contacts.",
            4: "Excellent visibility! Your CV is widely available to recruiters. Maintain these profiles actively: update regularly, respond quickly, keep profiles public and searchable. Your broad presence maximizes opportunities.",
            5: "Outstanding reach! Your comprehensive presence across multiple platforms maximizes recruiter discovery. You're leveraging passive job search effectively. Continue maintaining and updating these profiles for ongoing visibility."
        },
        5: {  # I know how to adapt my CV to different jobs
            1: "Learn CV customization immediately. It's essential. For each application, adjust your professional summary to mirror job requirements. Reorder skills to match priorities. Highlight relevant experience. Create a master CV to customize from.",
            2: "You understand the concept but improve execution. Use the job description as a template. Mirror their language exactly. If they say 'stakeholder engagement,' use that phrase (not 'client relationships'). Matching keywords matters for ATS.",
            3: "Good customization practice! Enhance by creating 2-3 base versions for different role types, then fine-tune. Save each version with the company name. This speeds customization while ensuring each CV is targeted.",
            4: "Excellent CV adaptation skills! You understand that generic CVs underperform dramatically. Your tailored approach demonstrates genuine interest and significantly increases interview rates. Continue this strategic practice.",
            5: "Masterful CV customization! You skillfully adapt while maintaining consistency and truth. You understand the balance: enough customization to show fit, without creating tracking problems or inconsistencies. This expertise maximizes success."
        },
        6: {  # I have an effective, tailorable cover letter
            1: "Create a cover letter template immediately. Structure: Address hiring manager by name if possible, opening hook, 2-3 paragraphs matching your skills to their needs, confident closing. Save as template to customize.",
            2: "You have something but strengthen it. Research strong cover letter examples in your field. Ensure yours tells a story, doesn't just repeat your CV. Show personality while remaining professional. Proofread ruthlessly.",
            3: "Good foundation! Now master customization. Each letter should reference the specific company and role. Research the company's recent news or challenges. Show how you'll contribute to their specific situation.",
            4: "Excellent cover letter! You've mastered the balance: professional yet personable, comprehensive yet concise, confident yet not arrogant. Your tailored approach shows genuine interest and research. Continue this standard.",
            5: "Perfect! Your cover letters are compelling, well-researched, and persuasively demonstrate fit. You understand they're not CV summaries but opportunities to show personality, passion, and research. Your letters open doors."
        }
    },
    "interview_skills": {
        0: {  # I know how to research companies thoroughly
            1: "Develop research skills immediately. Minimum: visit company website (especially 'About' and 'News'), read recent press releases, check LinkedIn company page, Google recent news, review Glassdoor. Take notes. Prepare questions.",
            2: "You do basic research but go deeper. Study: financial reports (if public), competitors, industry challenges, key executives' backgrounds, company culture indicators. Understand their business model and market position.",
            3: "Good research habits! Now synthesize information strategically. How does your background address their challenges? What questions demonstrate your research? Prepare to discuss industry trends affecting them specifically.",
            4: "Excellent research depth! You understand not just what they do but how they're positioned in their market. You can discuss their strategy intelligently. This knowledge level impresses interviewers and informs your questions.",
            5: "Outstanding! Your research is comprehensive and strategic. You understand their business, culture, challenges, and opportunities. This knowledge allows you to position yourself as a solution and ask insightful questions."
        },
        1: {  # I'm willing to ask questions in interviews
            1: "Overcome this hesitation immediately. Prepare 5-7 questions beforehand. Asking questions shows interest and intelligence. It's your opportunity to assess fit. Write them down and bring them. Not asking questions signals disinterest.",
            2: "You'll ask some but increase confidence. Good questions: 'What does success look like in this role?' 'What challenges might I face initially?' 'How would you describe the team culture?' Practice delivering them confidently.",
            3: "Good willingness! Ensure questions are substantive, not answerable via website research. Ask about growth, challenges, team dynamics, next steps. Balance: don't interview them aggressively, but show intelligent curiosity.",
            4: "Excellent! You understand interviews are two-way conversations. Your thoughtful questions demonstrate research, intelligence, and genuine interest. Continue this approach—it shows confidence and professionalism.",
            5: "Perfect! Your strategic questions demonstrate deep research and critical thinking. You're assessing fit as much as they are. This confidence level sets you apart and often converts interviewers into advocates."
        },
        2: {  # I'm prepared to give examples (STAR method)
            1: "Learn the STAR method immediately: Situation, Task, Action, Result. Prepare 5-7 stories covering common competencies: leadership, problem-solving, teamwork, conflict resolution, achievement. Write them out. Practice delivery.",
            2: "You understand STAR but need more preparation. For each past role, identify 3-4 significant achievements. Convert them to STAR format. Practice until delivery feels natural, not rehearsed. Quantify results wherever possible.",
            3: "Good STAR preparation! Ensure diversity in your examples—different contexts, skills, and outcomes. Avoid reusing the same story. Practice concise delivery (90 seconds max). Focus on your specific actions and measurable results.",
            4: "Excellent example preparation! Your STAR stories are polished, varied, and results-focused. You can smoothly adapt them to different questions. This preparation level gives you confidence and demonstrates professionalism.",
            5: "Outstanding! Your comprehensive STAR examples demonstrate your value compellingly. You can address virtually any behavioral question with a relevant, well-structured example. This preparation typically wins interviews."
        },
        3: {  # I know what employers expect in interviews
            1: "Research interview expectations immediately. Employers assess: skills match, cultural fit, communication ability, professionalism, enthusiasm, and problem-solving. Understand that fit matters as much as qualifications. Study common interview questions.",
            2: "You have general knowledge but deepen understanding. Different industries/roles have different expectations. Research your specific field. Understand the difference between phone screens, first interviews, and final rounds. Prepare accordingly.",
            3: "Solid understanding! Employers expect you to: demonstrate relevant competencies, show genuine interest, ask intelligent questions, communicate clearly, fit culturally. Ensure you're hitting all these points consistently.",
            4: "Excellent knowledge! You understand multi-dimensional assessment: technical skills, soft skills, motivation, and fit. You prepare accordingly. This comprehensive understanding helps you perform consistently well across different interview styles.",
            5: "Expert level! You understand sophisticated assessment techniques interviewers use. You know how to demonstrate competencies through examples, show cultural fit naturally, and build rapport. Your advanced knowledge consistently succeeds."
        },
        4: {  # I can answer tough interview questions
            1: "Prepare immediately for difficult questions. Common tough ones: 'Why did you leave?' 'What's your weakness?' 'Why this role?' 'Describe a failure.' Research answers online. Write yours out. Practice until confident.",
            2: "You can answer some but broaden preparation. Practice: salary expectations, gap explanations, 'Where do you see yourself in 5 years?', 'Why should we hire you?' Be honest but strategic. Never speak negatively about past employers.",
            3: "Good preparation! Ensure answers are concise (60-90 seconds), honest, and position you positively. For weaknesses, show self-awareness and improvement actions. For failures, focus on learning. Practice with a friend.",
            4: "Excellent! You handle difficult questions with poise and honesty. Your answers demonstrate self-awareness, resilience, and growth mindset. You can turn potentially negative questions into opportunities to showcase strengths.",
            5: "Outstanding! You welcome tough questions as opportunities to demonstrate emotional intelligence and authenticity. Your thoughtful, honest answers build trust. You've mastered the balance between honesty and strategic positioning."
        },
        5: {  # I know how to write Thank You letters
            1: "Learn this important etiquette. Send within 24 hours after interview. Email is fine. Structure: Thank them, reference specific discussion point, reiterate your interest and fit, mention next steps. Keep it brief (3-4 paragraphs).",
            2: "You understand basics but refine your approach. Personalize each letter with specific conversation details. Address each interviewer individually if you met multiple people. Proofread carefully—errors here are especially damaging.",
            3: "Good practice! Ensure thank you notes add value: clarify a point from interview, provide additional relevant information, demonstrate continued interest. Make it more than just 'thanks'—reinforce your fit.",
            4: "Excellent thank you letter skills! Your thoughtful, timely notes reinforce positive impressions and keep you top-of-mind. You understand this is another opportunity to demonstrate professionalism and interest.",
            5: "Perfect! Your strategic thank you letters strengthen candidacy by providing additional value while expressing gratitude. They're professional, personalized, and timely. This attention to detail often influences close hiring decisions."
        },
        6: {  # I know how to dress appropriately
            1: "Research dress codes immediately. General rule: dress one level above the company's daily standard. When in doubt, err on formal side. For most interviews: business professional (suit). Research the specific company culture beforehand.",
            2: "You have general ideas but be more strategic. Industry matters: finance/law = very formal, tech startup = smart casual may be acceptable. Check company photos on social media. Plan outfit a week ahead. Ensure everything fits, is clean, pressed.",
            3: "Good awareness! Now perfect the details: shoes polished, minimal jewelry, neat hair, subtle cologne/perfume, portfolio/bag professional. Your appearance should help them envision you in the role. Avoid anything distracting.",
            4: "Excellent presentation skills! You understand your appearance creates immediate impressions about professionalism and judgment. You dress appropriately for company culture while maintaining high standards. This awareness shows emotional intelligence.",
            5: "Impeccable! Your polished, appropriate presentation demonstrates exceptional professionalism and cultural awareness. You understand the psychological impact of appearance without being superficial. This attention to detail impresses consistently."
        },
        7: {  # I'll arrive 10 minutes early
            1: "Make this non-negotiable. Plan to arrive 15 minutes early (wait in car/cafe if too early). Account for traffic, parking, finding the office, security check-in. Test the route beforehand if possible. Late arrival often ends candidacy immediately.",
            2: "You intend to but sometimes cut it close. Build in more buffer. Aim for 20 minutes early, plan to enter 10 minutes early. Arriving stressed from rushing shows. Arriving calmly early lets you compose yourself and review notes.",
            3: "Good punctuality! Arriving early shows respect and reliability. Use the time to: observe company culture, review your notes, use restroom, calm nerves. If you're very early, wait nearby rather than arriving 30+ minutes early.",
            4: "Excellent time management! You're consistently early, composed, and prepared. This reliability is noticed and appreciated. It demonstrates respect and organizational skills. Continue this professional standard always.",
            5: "Perfect! Your consistent early arrival demonstrates exceptional professionalism and respect. You're never rushed or flustered. This reliability tells employers you'll bring the same professional standards to the job."
        }
    },
    "job_readiness": {
        0: {  # I'm enthusiastic about job searching
            1: "Build positive mindset immediately. Job searching is challenging—attitude matters enormously. Start each day with positive affirmations. Celebrate small wins. Connect with other job seekers for support. Treat rejection as redirection, not failure.",
            2: "Your enthusiasm varies—understandable but improvable. Create structure: daily goals, regular schedule, rewards for milestones. Exercise, maintain routines, stay connected socially. Protect your mental health. Low energy reduces application quality.",
            3: "Good energy level! Maintain it by: celebrating progress, taking breaks, mixing search activities (research, networking, applications), staying physically active. Enthusiasm is attractive to employers—project it in applications and interviews.",
            4: "Excellent positive energy! Your enthusiasm shows in applications and interviews—this is attractive to employers. Continue self-care practices that maintain this energy. Your optimism often becomes self-fulfilling.",
            5: "Outstanding enthusiasm! Your positive energy is infectious and significantly impacts how employers perceive you. Your genuine excitement about opportunities comes through clearly. This attitude is a major competitive advantage."
        },
        1: {  # I can present my abilities positively
            1: "Develop confident self-presentation immediately. List 10 achievements. Practice stating them proudly without apologizing or minimizing. Record yourself. Watch for confident body language and vocal tone. Fake confidence until it becomes real.",
            2: "You can somewhat advocate for yourself but strengthen this crucial skill. Practice your '60-second commercial' daily. Ask friends what you do well—others often see strengths you miss. Own your accomplishments without arrogance.",
            3: "Good self-presentation! Continue building confidence. Prepare specific examples of your impact. Practice the difference between confidence (stating facts about your achievements) and arrogance (putting others down). Employers want confident people.",
            4: "Excellent self-advocacy! You present your abilities confidently and compellingly without arrogance. You can discuss achievements naturally in conversation. This skill is essential for interviews and networking. Continue this authentic confidence.",
            5: "Outstanding! You present your abilities with perfect balance: confident yet humble, comprehensive yet concise. Your genuine pride in your work without arrogance is highly attractive to employers. This mastery significantly enhances hiring success."
        },
        2: {  # I know realistic salary expectations
            1: "Research immediately. Use Glassdoor, PayScale, Reed, LinkedIn Salary. Check multiple sources. Consider: your experience level, location, company size, industry. Be prepared to discuss range, not single number. Know your minimum (walk-away point).",
            2: "You have rough ideas but need precise data. Research your specific role in your specific location. Understand total compensation: salary, benefits, bonuses, pension. Know what factors justify higher end of range (your specific skills/experience).",
            3: "Good salary knowledge! Now prepare negotiation strategy. Practice stating your range confidently. Understand when to discuss salary (ideally after they're interested). Know your value but remain flexible. Research the specific company's pay reputation.",
            4: "Excellent salary awareness! You know your market value and can justify it with data. You're prepared to negotiate strategically. This knowledge prevents underselling yourself or pricing yourself out. Continue staying current on market rates.",
            5: "Perfect market knowledge! You understand nuanced factors affecting compensation: company stage, location, total package, negotiation leverage timing. This sophisticated understanding positions you to negotiate optimal packages confidently."
        },
        3: {  # I'm prepared to accept a job tomorrow
            1: "Get ready immediately. Ensure you: have professional clothes ready, arrangements for childcare/transport if needed, can start on short notice, have references prepared, resolved any contractual obligations. Being truly ready projects confidence.",
            2: "You're mostly ready but finalize details. Check notice period at current job (if applicable), ensure references are current and have agreed, have first-week logistics planned (transport, clothing). Remove barriers to saying 'yes' immediately.",
            3: "Good readiness! Ensure absolutely no logistical barriers exist. Resolve any potential issues now: transportation, childcare, work permits, professional wardrobe. When you say you're ready, mean it completely. This shows seriousness.",
            4: "Excellent preparedness! You can genuinely accept an offer immediately. This demonstrates serious intent and removes employer concerns about your commitment. Your readiness often accelerates hiring decisions in your favor.",
            5: "Perfect readiness! You're completely prepared to start immediately with zero barriers. This exceptional readiness demonstrates professionalism and serious commitment. It can be the deciding factor when employers are choosing between candidates."
        }
    }
}


# Category-level feedback based on overall category status
CATEGORY_FEEDBACK = {
    'skills_abilities': {
        'good': "Excellent! You have a strong understanding of your skills and how to present them. Keep your skills list updated as you gain new experiences.",
        'acceptable': "You have a reasonable grasp of your skills. Consider creating a comprehensive skills inventory and practice articulating them in different contexts.",
        'needs_improvement': "Focus on identifying your core skills. Try: List 5 achievements, then identify the skills you used. Update your CV to highlight these clearly."
    },
    'job_search': {
        'good': "Great job search strategy! You're using effective methods and dedicating proper time. Continue to track which methods work best for you.",
        'acceptable': "Your search strategy is developing. Ensure you're dedicating at least 6 hours daily to active job searching when unemployed.",
        'needs_improvement': "Strengthen your search approach. Action: Research the top 5 job sites in your field. Set up daily job alerts. Block out dedicated search time each day."
    },
    'job_applications': {
        'good': "Excellent application skills! You're thorough and professional. Keep this high standard for every application you submit.",
        'acceptable': "Your applications are generally solid. Double-check each one before submitting, and ensure you're highlighting the employer's specific needs.",
        'needs_improvement': "Improve your applications. Try: Use a checklist for each application. Have someone review your next 3 applications before sending. Practice explaining CV gaps positively."
    },
    'effective_cvs': {
        'good': "Your CV strategy is strong! Keep your CV updated regularly and continue tailoring it for each role.",
        'acceptable': "Your CV approach is reasonable. Get feedback from 2-3 trusted people. Practice adapting your CV for different job types.",
        'needs_improvement': "Your CV needs work. Action: Get your CV professionally reviewed. Research what employers in your field want to see. Create 2-3 versions for different role types."
    },
    'interview_skills': {
        'good': "Excellent interview preparation! You're well-prepared and professional. Continue researching each company thoroughly and preparing examples.",
        'acceptable': "Your interview skills are developing. Practice the STAR method for answering questions. Prepare 3-5 questions to ask in every interview.",
        'needs_improvement': "Build your interview confidence. Try: Research 10 common interview questions and write answers. Practice with a friend. Record yourself answering questions."
    },
    'job_readiness': {
        'good': "You're highly motivated and ready! This positive mindset will serve you well. Maintain this enthusiasm throughout your search.",
        'acceptable': "Your readiness is moderate. Clarify your ideal role and salary range. Ensure all your materials are ready to go at any moment.",
        'needs_improvement': "Boost your readiness. Action: Define your must-haves vs. nice-to-haves in a role. Research realistic salary ranges. Prepare a 30/60/90 day plan for starting a new job."
    }
}


# Assessment categories with questions and scoring thresholds
CATEGORIES = {
    "skills_abilities": {
        "title": "Skills and abilities analysis",
        "questions": [
            "I know the skills and qualities employers are looking for in the type of work I want.",
            "I have developed a list of the skills that I have to offer an employer, I can explain them clearly and they are on my CV.",
            "I know the titles of the jobs that fit my skills and knowledge and where the jobs are located.",
            "I know which of my job skills are transferable to other types of jobs.",
            "I have prepared a brief, high impact '60 second commercial' to sell myself to employers.",
            "I am fully aware of the areas in which I need to improve my skills and am working on these areas of improvement."
        ],
        "good_threshold": 24,
        "needs_improvement_threshold": 18
    },
    "job_search": {
        "title": "Job search strategies",
        "questions": [
            "I know what the most effective and least effective job search methods are",
            "I would be willing to devote at least SIX hours a day to my job search and applications",
            "I know which vacancies are popular at the moment",
            "I know how to use the internet to explore the labour market and search for vacancies",
            "I know at least three job search sites",
            "I know what services are available to help with gaining employment"
        ],
        "good_threshold": 22,
        "needs_improvement_threshold": 18
    },
    "job_applications": {
        "title": "Applying for jobs",
        "questions": [
            "I know how to complete an application completely and accurately",
            "After completing an application, I even go back and look at the application one last time to make sure it is complete",
            "I know exactly what I'd need to bring to an interview",
            "I know how to apply online for jobs using email attachments",
            "I know how to log my job search activities",
            "I know how to give complete and accurate reasons for gaps in my CV",
            "I can highlight the employer's needs on my application"
        ],
        "good_threshold": 25,
        "needs_improvement_threshold": 21
    },
    "effective_cvs": {
        "title": "Effective CVs",
        "questions": [
            "I have a current, effective CV. It's printed on white paper and is ready to send to any employer",
            "I have had at least 3 people, whom I trust, to read and evaluate my CV",
            "I know what employers look for in a CV",
            "I know how to upload a CV to a web site",
            "I have my CV posted on at least two job search websites",
            "I know how to adapt my CV to different jobs",
            "I have an effective cover letter written and can (or will) tailor it for each job"
        ],
        "good_threshold": 25,
        "needs_improvement_threshold": 21
    },
    "interview_skills": {
        "title": "Interview skills",
        "questions": [
            "I know how to research companies thoroughly before I go to an interview",
            "I am willing to ask questions in an interview",
            "I am prepared to give examples of how I've handled situations in the past",
            "I know what employers expect in an interview",
            "I can answer the toughest questions an employer may ask in the interview",
            "I know how to write a Thank You letter after the interview",
            "I know how to dress appropriately for an interview",
            "I will arrive at least 10 minutes prior to the start time of the interview"
        ],
        "good_threshold": 35,
        "needs_improvement_threshold": 30
    },
    "job_readiness": {
        "title": "Job readiness",
        "questions": [
            "I feel that I'm ready to get a great job! I'm very enthusiastic about job searching",
            "I have a firm knowledge of my abilities and am prepared to present them to an employer in a very positive manner",
            "I realistically know the salary that is correct for the job for which I am applying",
            "I am prepared today to accept a job tomorrow if offered"
        ],
        "good_threshold": 20,
        "needs_improvement_threshold": 18
    }
}

