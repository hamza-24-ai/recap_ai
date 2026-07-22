"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import api from "@/lib/axios"
import type { ActionItem, ActionItemCitation } from "@/types"
import CitationModal from "@/components/CitationModel"

interface ActionItemCardProps {
  item: ActionItem
}

const statusStyles: Record<string, string> = {
  pending: "bg-amber-100 text-amber-700",
  done: "bg-emerald-100 text-emerald-700",
  overdue: "bg-rose-100 text-rose-700",
}

export default function ActionItemCard({ item }: ActionItemCardProps) {
  const [citation, setCitation] = useState<ActionItemCitation | null>(null)
  const [loadingCitation, setLoadingCitation] = useState(false)

  const handleClick = async () => {
    setLoadingCitation(true)
    try {
      const res = await api.get(`/action-items/${item.id}/citation`)
      setCitation(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingCitation(false)
    }
  }

  return (
    <>
      <motion.div
        whileHover={{ y: -2 }}
        onClick={handleClick}
        className="bg-white/70 backdrop-blur-xl border border-white/60 rounded-xl p-4 cursor-pointer hover:shadow-lg hover:shadow-sky-900/5 transition"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-800">
              {item.task_description}
            </p>
            <div className="flex items-center gap-3 mt-1.5">
              {item.assignee_name && (
                <span className="text-xs text-slate-400">
                  {item.assignee_name}
                </span>
              )}
              {item.deadline && (
                <span className="text-xs text-slate-400">
                  Due {new Date(item.deadline).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>

          <span
            className={`text-xs font-medium px-2.5 py-1 rounded-full capitalize whitespace-nowrap ${
              statusStyles[item.status] || "bg-slate-100 text-slate-600"
            }`}
          >
            {loadingCitation ? "..." : item.status}
          </span>
        </div>
      </motion.div>

      {citation && (
        <CitationModal citation={citation} onClose={() => setCitation(null)} />
      )}
    </>
  )
}