from typing import Dict, Any

STUDENT_PRESET = {
    "company_name": None,
    "organization_name": None,
    "industry": "AI engineering and advanced physics",
    "target_audience": "internship recruiters, academic mentors, and project collaborators",
    "brand_tone": "Clear, professional, and confident",
    "user_profile": {
        "name": "IIT Roorkee BSMS Physics student",
        "role": "AI Engineering aspirant",
        "specialization": "AI engineering with physics foundations",
        "objective": "Build a strong internship pipeline, master AI skills, and launch impactful projects",
        "preferred_tone": "Professional but approachable",
        "about": "A student combining physics intuition with practical AI engineering." 
    },
    "active_departments": [
        {
            "name": "task_execution",
            "focus_areas": ["Prioritize daily work", "Turn goals into tasks", "Track completion"],
            "skills": ["task_planning", "daily_scheduler", "priority_manager"],
            "allowed_tools": ["todo_manager", "calendar"]
        },
        {
            "name": "communication",
            "focus_areas": ["Draft outreach emails", "Rewrite messages", "Write follow-up templates"],
            "skills": ["email_drafting", "message_editing", "follow_up_writer"],
            "allowed_tools": ["email_composer", "email_sender"]
        },
        {
            "name": "profile_manager",
            "focus_areas": ["Optimize LinkedIn", "Polish resume/portfolio", "Monitor online presence"],
            "skills": ["profile_review", "resume_tailoring", "portfolio_updating"],
            "allowed_tools": ["profile_audit"]
        },
        {
            "name": "research",
            "focus_areas": ["Find study resources", "Summarize papers", "Build roadmaps"],
            "skills": ["resource_curator", "topic_explainer", "roadmap_builder"],
            "allowed_tools": ["document_summarizer"]
        },
        {
            "name": "opportunity_scout",
            "focus_areas": ["Discover internships", "Filter by fit", "Track deadlines"],
            "skills": ["opportunity_finding", "deadline_monitoring", "company_filtering"],
            "allowed_tools": ["web_search"]
        },
        {
            "name": "application_optimizer",
            "focus_areas": ["Tailor resumes", "Write cover letters", "Align strengths with roles"],
            "skills": ["resume_customization", "cover_letter_writer", "skill_alignment"],
            "allowed_tools": ["resume_editor"]
        },
        {
            "name": "cold_email_composer",
            "focus_areas": ["Write outreach sequences", "Personalize recruiter messages", "Create follow-up plans"],
            "skills": ["cold_outreach", "email_subject_generation", "follow_up_sequence"],
            "allowed_tools": ["email_composer", "email_sender"]
        },
        {
            "name": "learning_roadmap_architect",
            "focus_areas": ["Create study plans", "Map prerequisites", "Segment mastery goals"],
            "skills": ["roadmap_planning", "milestone_setting", "skill_gap_analysis"],
            "allowed_tools": ["calendar"]
        },
        {
            "name": "project_idea_generator",
            "focus_areas": ["Generate portfolio projects", "Match ideas to internships", "Recommend tool stacks"],
            "skills": ["project_ideation", "project_scoping", "technology_selection"],
            "allowed_tools": ["idea_bank"]
        },
        {
            "name": "progress_dashboard_creator",
            "focus_areas": ["Track progress", "Visualize goals", "Report blockers"],
            "skills": ["progress_tracking", "status_reporting", "blocker_analysis"],
            "allowed_tools": ["dashboard"]
        },
        {
            "name": "networking_strategist",
            "focus_areas": ["Plan outreach to mentors", "Identify events", "Track connections"],
            "skills": ["network_mapping", "relationship_planning", "event_sourcing"],
            "allowed_tools": ["contact_manager"]
        },
        {
            "name": "portfolio_builder",
            "focus_areas": ["Curate projects", "Write project stories", "Optimize GitHub"],
            "skills": ["portfolio_curation", "project_storytelling", "repo_cleanup"],
            "allowed_tools": []
        },
        {
            "name": "feedback_synthesizer",
            "focus_areas": ["Summarize feedback", "Identify improvement patterns", "Suggest next steps"],
            "skills": ["feedback_analysis", "iteration_planning", "response_improvement"],
            "allowed_tools": []
        },
        {
            "name": "general_support",
            "focus_areas": ["Tackle any request", "Coordinate multiple tasks", "Provide fast real-world assistance"],
            "skills": ["problem_solving", "general_assistant", "execution_management"],
            "allowed_tools": ["web_search", "email_sender", "todo_manager", "calendar", "document_summarizer", "profile_audit"]
        }
    ]
}

FOUNDER_PRESET = {
    "company_name": "My Startup",
    "organization_name": "Founders Co.",
    "industry": "AI product development",
    "target_audience": "investors, early customers, and partners",
    "brand_tone": "Confident, visionary, and concise",
    "user_profile": {
        "name": "Startup founder",
        "role": "Founder",
        "specialization": "AI products and go-to-market execution",
        "objective": "Build traction, raise funding, and execute product milestones",
        "preferred_tone": "Clear, ambitious, and business-focused",
        "about": "A founder building a strong AI startup with rapid execution." 
    },
    "active_departments": [
        {
            "name": "task_execution",
            "focus_areas": ["Prioritize product work", "Coordinate sprints", "Track OKRs"],
            "skills": ["task_planning", "priority_manager", "meeting_preparation"],
            "allowed_tools": ["todo_manager", "calendar"]
        },
        {
            "name": "communication",
            "focus_areas": ["Draft investor emails", "Write partner outreach", "Prepare updates"],
            "skills": ["email_drafting", "message_editing", "follow_up_writer"],
            "allowed_tools": ["email_composer"]
        },
        {
            "name": "profile_manager",
            "focus_areas": ["Polish founder profile", "Optimize pitch deck messaging", "Monitor founder reputation"],
            "skills": ["profile_review", "deck_polishing", "personal_branding"],
            "allowed_tools": ["profile_audit"]
        },
        {
            "name": "opportunity_scout",
            "focus_areas": ["Find partnership leads", "Find investor events", "Track funding programs"],
            "skills": ["opportunity_finding", "deadline_monitoring", "company_filtering"],
            "allowed_tools": ["opportunity_tracker"]
        },
        {
            "name": "application_optimizer",
            "focus_areas": ["Tailor investor updates", "Optimize outreach materials", "Refine messaging"],
            "skills": ["pitch_refinement", "story_alignment", "content_customization"],
            "allowed_tools": ["deck_editor"]
        },
        {
            "name": "marketing_planner",
            "focus_areas": ["Build content campaigns", "Target launch audiences", "Create growth plans"],
            "skills": ["campaign_planning", "audience_analysis", "brand_communication"],
            "allowed_tools": []
        },
        {
            "name": "general_support",
            "focus_areas": ["Tackle any request", "Coordinate multiple tasks", "Provide fast real-world assistance"],
            "skills": ["problem_solving", "general_assistant", "execution_management"],
            "allowed_tools": ["web_search", "email_sender", "todo_manager", "calendar", "document_summarizer", "profile_audit"]
        }
    ]
}

CREATOR_PRESET = {
    "company_name": "Creator Brand",
    "organization_name": "Creative Studio",
    "industry": "Content creation and audience growth",
    "target_audience": "viewers, followers, and brand partners",
    "brand_tone": "Engaging, polished, and authentic",
    "user_profile": {
        "name": "Content creator",
        "role": "Creator",
        "specialization": "AI education and technology storytelling",
        "objective": "Grow an audience, publish consistent content, and attract opportunities",
        "preferred_tone": "Friendly, energetic, and credible",
        "about": "A creator building a loyal audience with AI and technology content." 
    },
    "active_departments": [
        {
            "name": "task_execution",
            "focus_areas": ["Plan content workflows", "Schedule production", "Track deadlines"],
            "skills": ["task_planning", "calendar_management", "content_scheduling"],
            "allowed_tools": ["todo_manager", "calendar"]
        },
        {
            "name": "communication",
            "focus_areas": ["Draft brand emails", "Write collaboration outreach", "Compose creator updates"],
            "skills": ["email_drafting", "message_editing", "audience_communication"],
            "allowed_tools": ["email_composer"]
        },
        {
            "name": "profile_manager",
            "focus_areas": ["Optimize creator profile", "Polish portfolio", "Monitor audience channels"],
            "skills": ["profile_review", "portfolio_updating", "channel_audit"],
            "allowed_tools": ["profile_audit"]
        },
        {
            "name": "content_planner",
            "focus_areas": ["Plan series ideas", "Map content themes", "Generate topic pipelines"],
            "skills": ["content_ideation", "series_planning", "topic_research"],
            "allowed_tools": ["content_calendar"]
        },
        {
            "name": "audience_growth",
            "focus_areas": ["Suggest growth tactics", "Optimize engagement", "Track follower goals"],
            "skills": ["growth_strategy", "engagement_planning", "audience_analysis"],
            "allowed_tools": ["analytics_dashboard"]
        },
        {
            "name": "portfolio_builder",
            "focus_areas": ["Curate creative work", "Write campaign case studies", "Create media kits"],
            "skills": ["portfolio_curation", "case_study_writing", "media_kit_builder"],
            "allowed_tools": []
        },
        {
            "name": "general_support",
            "focus_areas": ["Tackle any request", "Coordinate multiple tasks", "Provide fast real-world assistance"],
            "skills": ["problem_solving", "general_assistant", "execution_management"],
            "allowed_tools": ["web_search", "email_sender", "todo_manager", "calendar", "document_summarizer", "profile_audit"]
        }
    ]
}

PRESETS: Dict[str, Dict[str, Any]] = {
    "student": STUDENT_PRESET,
    "founder": FOUNDER_PRESET,
    "creator": CREATOR_PRESET
}

# A lightweight personal preset for non-professional, consented messages.
PERSONAL_PRESET = {
    "company_name": None,
    "organization_name": None,
    "industry": "personal",
    "target_audience": "friends and contacts",
    "brand_tone": "Casual and warm",
    "user_profile": {
        "name": "Personal User",
        "role": "Individual",
        "specialization": "Personal communications",
        "objective": "Send friendly, personal messages",
        "preferred_tone": "Casual",
        "about": "Personal messaging preset for trusted contacts." 
    },
    "active_departments": [
        {
            "name": "communication",
            "focus_areas": ["Write personal messages", "Send greetings", "Share informal notes"],
            "skills": ["personal_outreach", "message_writing", "friendly_tone"],
            "allowed_tools": ["email_sender", "email_composer", "contact_manager"]
        }
    ]
}

# Add personal preset to mapping
PRESETS["personal"] = PERSONAL_PRESET


def get_preset(name: str) -> Dict[str, Any]:
    return PRESETS.get(name.lower(), STUDENT_PRESET)
