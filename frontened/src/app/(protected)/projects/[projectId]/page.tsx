"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { motion, AnimatePresence } from "framer-motion"
import api from "@/lib/axios"
import type { ActionItem } from "@/types"
import UploadForm from "@/components/UploadForm"
import ProcessingLoader from "@/components/ProcessingLoader"
import ActionItemCard from "@/components/ActionItemCard"

export default function ProjectDetailPage() {
  const params = useParams()
  const projectId = Number(params.projectId)

//   const [meetings, setMeetings] = useState<Meeting[]>([])
  const [actionItems, setActionItems] = useState<ActionItem[]>([])
  const [loading, setLoading] = useState(true)
  const [processingMeetingId, setProcessingMeetingId] = useState<number | null>(null)
  const [statusFilter, setStatusFilter] = useState<string>("all")

  useEffect(() => {
    const fetchData = async () => {
    try {
      const [actionItemsRes] = await Promise.all([
        api.get(`/action-items/project/${projectId}`),
      ])
      setActionItems(actionItemsRes.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }
    fetchData()
  }, [projectId])



  const handleUploadStart = (meetingId: number) => {
    setProcessingMeetingId(meetingId)
  }

  const handleProcessingComplete = () => {
    setProcessingMeetingId(null)
    const fetchData = async () => {
    try {
      const [actionItemsRes] = await Promise.all([
        api.get(`/action-items/project/${projectId}`),
      ])
      setActionItems(actionItemsRes.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }
    fetchData()   // naye decisions/action items refresh karo
  }

  const filteredItems =
    statusFilter === "all"
      ? actionItems
      : actionItems.filter((item) => item.status === statusFilter)

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-2xl font-semibold text-slate-800 tracking-tight mb-8">
        Project Overview
      </h1>

      {/* Upload Section */}
      <div className="mb-8">
        <UploadForm projectId={projectId} onUploadStart={handleUploadStart} />
      </div>

      {/* Processing Loader — sirf jab koi meeting process ho rahi ho */}
      <AnimatePresence>
        {processingMeetingId && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-8"
          >
            <ProcessingLoader
              meetingId={processingMeetingId}
              onComplete={handleProcessingComplete}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Action Items Section */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-medium text-slate-800">Action Items</h2>

        {/* Status filter */}
        <div className="flex gap-2">
          {["all", "pending", "done", "overdue"].map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition ${
                statusFilter === s
                  ? "bg-sky-500 text-white"
                  : "bg-white/60 text-slate-500 hover:bg-white"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="text-slate-500">Loading...</p>
      ) : filteredItems.length === 0 ? (
        <div className="bg-white/60 backdrop-blur-xl border border-white/60 rounded-2xl p-10 text-center">
          <p className="text-slate-600 font-medium">No action items yet</p>
          <p className="text-slate-400 text-sm mt-1">
            Upload a transcript to get started.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredItems.map((item) => (
            <ActionItemCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  )
}