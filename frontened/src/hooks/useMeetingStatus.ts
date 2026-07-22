"use client"

import { useEffect, useState } from "react"

export function useMeetingStatus(meetingId: number | null) {
  const [status, setStatus] = useState<string | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    if (!meetingId) return

    const ws = new WebSocket(`ws://localhost:8000/ws/meeting-status/${meetingId}`)

    // Cleanup ke waqt agar socket abhi bhi CONNECTING hai (React StrictMode dev
    // mein effect do dafa mount/unmount karta hai), to seedha close() karne se
    // "closed before established" warning aati hai. Isliye flag laga kar handle
    // karte hain: agar unmount pehle ho gaya to open hote hi close kar do.
    let cancelled = false

    ws.onopen = () => {
      if (cancelled) {
        ws.close()
        return
      }
      setIsConnected(true)
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setStatus(data.status)
    }

    ws.onclose = () => {
      setIsConnected(false)
    }

    ws.onerror = (err) => {
      console.error("WebSocket error:", err)
    }

    // Cleanup — jab component unmount ho ya meetingId change ho, connection band karo.
    // Sirf tab close karo jab handshake mukammal ho chuka ho; warna open hone ka
    // intezaar onopen handler karega (cancelled flag ke zariye).
    return () => {
      cancelled = true
      if (ws.readyState === WebSocket.OPEN) {
        ws.close()
      }
    }
  }, [meetingId])

  return { status, isConnected }
}