export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

export interface Project {
  id: number;
  name: string;
  created_at: string;
}

export interface Meeting {
  id: number;
  project_id: number;
  title: string;
  file_url: string | null;
  status: "processing" | "done";
  uploaded_at: string;
}

export interface Decision {
  id: number;
  meeting_id: number;
  decision_text: string;
  created_at: string;
}

export interface ActionItem {
  id: number;
  meeting_id: number;
  assignee_name: string | null;
  task_description: string;
  deadline: string | null;
  status: "pending" | "done" | "overdue";
  source_snippet: string | null;
  last_checked_meeting_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface ActionItemCitation {
  id: number;
  task_description: string;
  assignee_name: string | null;
  source_snippet: string | null;
  meeting_id: number;
  meeting_title: string;
  meeting_uploaded_at: string;
  file_url: string | null;
}