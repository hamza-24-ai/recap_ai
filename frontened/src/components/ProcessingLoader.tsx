"use client"

import { motion, AnimatePresence } from "framer-motion"
import { useMeetingStatus } from "@/hooks/useMeetingStatus"
import { statusLabels } from "@/utils/statusLabels"
import { useEffect } from "react"

interface ProcessingLoaderProps {
  meetingId: number
  onComplete: () => void
}

export default function ProcessingLoader({ meetingId, onComplete }: ProcessingLoaderProps) {
  const { status, isConnected } = useMeetingStatus(meetingId)

  // Jab "done" (ya "error") status aaye, parent ko batao processing complete ho gayi.
  // NOTE: dependency array mein [status] zaroori hai — warna ye effect sirf mount par
  // ek dafa chalta (jab status abhi null hai) aur "done" kabhi detect nahi hota.
  useEffect(() => {
    if (status === "done" || status === "error") {
      const timer = setTimeout(onComplete, 800)   // thora delay taake "Done!" dikh sake pehle
      return () => clearTimeout(timer)
    }
  }, [status, onComplete])

  const displayText = status ? statusLabels[status] || status : "Connecting..."

  return (
    <div className="bg-white/70 backdrop-blur-xl border border-white/60 rounded-2xl p-8 flex flex-col items-center justify-center gap-4">
      {/* Animated spinner */}
      <div className="relative w-12 h-12">
        <motion.div
          className="absolute inset-0 rounded-full border-2 border-sky-200"
        />
        <motion.div
          className="absolute inset-0 rounded-full border-2 border-transparent border-t-sky-500"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
      </div>

      {/* Status text with fade transition */}
      <AnimatePresence mode="wait">
        <motion.p
          key={displayText}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          transition={{ duration: 0.3 }}
          className="text-sm font-medium text-slate-600"
        >
          {displayText}
        </motion.p>
      </AnimatePresence>

      {!isConnected && (
        <p className="text-xs text-slate-400">Connecting to server...</p>
      )}
    </div>
  )
}