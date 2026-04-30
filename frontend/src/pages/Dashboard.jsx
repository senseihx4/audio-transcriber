import { useState, useEffect, useRef } from 'react'
import api from '../api'

// ─── Upload Card ─────────────────────────────────────────────
function UploadCard({ onDone }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef()

  async function handleUpload(e) {
    e.preventDefault()
    if (!file) return
    setError('')
    setLoading(true)
    try {
      const form = new FormData()
      form.append('audio_file', file)
      await api.post('/audio/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      setFile(null)
      inputRef.current.value = ''
      onDone()
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
      <h2 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>
        Upload Audio
      </h2>

      <form onSubmit={handleUpload} className="space-y-4">
        <label
          onClick={() => inputRef.current.click()}
          className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-700 hover:border-violet-500 rounded-xl cursor-pointer transition"
        >
          {file ? (
            <div className="text-center px-4">
              <svg className="w-8 h-8 text-violet-400 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
              </svg>
              <p className="text-sm text-gray-300 font-medium truncate max-w-xs">{file.name}</p>
              <p className="text-xs text-gray-500 mt-0.5">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          ) : (
            <div className="text-center">
              <svg className="w-8 h-8 text-gray-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p className="text-sm text-gray-400">Click to select audio file</p>
              <p className="text-xs text-gray-600 mt-1">MP3, WAV, M4A, FLAC…</p>
            </div>
          )}
        </label>
        <input
          ref={inputRef}
          type="file"
          accept="audio/*"
          className="hidden"
          onChange={(e) => setFile(e.target.files[0])}
        />

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={!file || loading}
          className="w-full bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-lg text-sm transition"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Transcribing…
            </span>
          ) : 'Upload & Transcribe'}
        </button>
      </form>
    </div>
  )
}

// ─── Record Card ─────────────────────────────────────────────
function RecordCard({ onDone }) {
  const [seconds, setSeconds] = useState(5)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleRecord() {
    setError('')
    setLoading(true)
    try {
      await api.post('/audio/record/', { seconds })
      onDone()
    } catch (err) {
      setError(err.response?.data?.detail || 'Recording failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
      <h2 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
        Record Audio
      </h2>

      <p className="text-gray-400 text-sm mb-5">
        Record directly from your microphone. The server will capture audio for the specified duration and transcribe it.
      </p>

      <div className="mb-5">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Duration: <span className="text-violet-400 font-semibold">{seconds}s</span>
        </label>
        <input
          type="range"
          min={1}
          max={60}
          value={seconds}
          onChange={(e) => setSeconds(Number(e.target.value))}
          className="w-full accent-violet-500"
        />
        <div className="flex justify-between text-xs text-gray-600 mt-1">
          <span>1s</span><span>60s</span>
        </div>
      </div>

      {error && <p className="text-red-400 text-sm mb-3">{error}</p>}

      <button
        onClick={handleRecord}
        disabled={loading}
        className="w-full bg-red-600 hover:bg-red-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-lg text-sm transition flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
            </svg>
            Recording {seconds}s…
          </>
        ) : (
          <>
            <span className="w-2 h-2 rounded-full bg-white" />
            Start Recording
          </>
        )}
      </button>
    </div>
  )
}

// ─── Transcription Item ───────────────────────────────────────
function TranscriptionItem({ item }) {
  const [expanded, setExpanded] = useState(false)
  const isLong = item.text && item.text.length > 200

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-8 h-8 rounded-lg bg-violet-500/20 flex items-center justify-center shrink-0">
            <svg className="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
          </div>
          <span className="text-xs text-gray-500 truncate">#{item.id}</span>
        </div>
        {isLong && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-violet-400 hover:text-violet-300 shrink-0"
          >
            {expanded ? 'Show less' : 'Show more'}
          </button>
        )}
      </div>

      <div className="mt-3">
        {item.text ? (
          <p className="text-gray-200 text-sm leading-relaxed">
            {isLong && !expanded ? item.text.slice(0, 200) + '…' : item.text}
          </p>
        ) : (
          <p className="text-gray-600 text-sm italic">No transcription available</p>
        )}
      </div>

      {(item.audio_file || item.record_audiofile) && (
        <div className="mt-3 pt-3 border-t border-gray-800">
          <audio
            controls
            src={item.audio_file || item.record_audiofile}
            className="w-full h-8"
            style={{ height: '32px' }}
          />
        </div>
      )}
    </div>
  )
}

// ─── Dashboard ────────────────────────────────────────────────
export default function Dashboard() {
  const [transcriptions, setTranscriptions] = useState([])
  const [loadingList, setLoadingList] = useState(true)
  const [listError, setListError] = useState('')

  async function fetchTranscriptions() {
    setLoadingList(true)
    setListError('')
    try {
      const { data } = await api.get('/audio/')
      setTranscriptions(data)
    } catch {
      setListError('Could not load transcriptions')
    } finally {
      setLoadingList(false)
    }
  }

  useEffect(() => { fetchTranscriptions() }, [])

  return (
    <div className="min-h-screen bg-gray-950 px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400 text-sm mb-8">Upload or record audio to get AI transcriptions</p>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <UploadCard onDone={fetchTranscriptions} />
          <RecordCard onDone={fetchTranscriptions} />
        </div>

        {/* Transcriptions List */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-white font-semibold text-lg">Transcriptions</h2>
            <button
              onClick={fetchTranscriptions}
              className="text-xs text-gray-400 hover:text-white flex items-center gap-1 transition"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh
            </button>
          </div>

          {loadingList ? (
            <div className="flex items-center justify-center py-16">
              <svg className="animate-spin w-6 h-6 text-violet-500" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
            </div>
          ) : listError ? (
            <div className="text-center py-12 text-red-400 text-sm">{listError}</div>
          ) : transcriptions.length === 0 ? (
            <div className="text-center py-16 border border-dashed border-gray-800 rounded-2xl">
              <svg className="w-10 h-10 text-gray-700 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p className="text-gray-600 text-sm">No transcriptions yet</p>
              <p className="text-gray-700 text-xs mt-1">Upload or record audio above to get started</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {[...transcriptions].reverse().map((item) => (
                <TranscriptionItem key={item.id} item={item} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
