"use client"

import { motion } from "framer-motion"
import type { ActionItemCitation } from "@/types"

interface CitationModalProps {
  citation: ActionItemCitation
  onClose: () => void
}

export default function CitationModal({ citation, onClose }: CitationModalProps) {
  return (
    <div
      className="fixed inset-0 bg-slate-900/30 backdrop-blur-sm flex items-center justify-center z-50 px-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-2xl p-6 w-full max-w-lg shadow-xl max-h-[80vh] overflow-y-auto"
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-800">Source</h2>
            <p className="text-xs text-slate-400 mt-0.5">
              {citation.meeting_title} —{" "}
              {new Date(citation.meeting_uploaded_at).toLocaleDateString()}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition text-xl leading-none"
          >
            ×
          </button>
        </div>

        <div className="mb-4">
          <p className="text-sm font-medium text-slate-600 mb-1">Task</p>
          <p className="text-sm text-slate-800">{citation.task_description}</p>
          {citation.assignee_name && (
            <p className="text-xs text-slate-400 mt-1">
              Assigned to {citation.assignee_name}
            </p>
          )}
        </div>

        {citation.source_snippet && (
          <div className="mb-4">
            <p className="text-sm font-medium text-slate-600 mb-1.5">
              Extracted from transcript
            </p>
            <blockquote className="bg-sky-50 border-l-4 border-sky-400 rounded-r-lg px-4 py-3 text-sm text-slate-700 italic">
              {citation.source_snippet}
            </blockquote>
          </div>
        )}

        {citation.file_url && (
          <a
            href={citation.file_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block text-sm text-sky-600 font-medium hover:underline"
          >
            View original file →
          </a>
        )}
      </motion.div>
    </div>
  )
}