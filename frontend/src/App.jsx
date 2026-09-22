import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const defaultMessages = [
  { role: 'assistant', content: 'Upload a document, template, or presentation and tell me what you need created or revised.' },
];

function App() {
  const [token, setToken] = useState('');
  const [user, setUser] = useState({ email: 'demo@example.com', username: 'Demo User' });
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [messages, setMessages] = useState(defaultMessages);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedArtifacts, setUploadedArtifacts] = useState([]);

  const authHeaders = useMemo(() => ({
    Authorization: `Bearer ${token}`,
  }), [token]);

  useEffect(() => {
    const ensureDemoLogin = async () => {
      try {
        const response = await axios.post(`${API_BASE}/auth/register`, {
          email: 'demo@example.com',
          username: 'Demo User',
          password: 'demo1234',
        });
        setToken(response.data.access_token);
      } catch (error) {
        try {
          const response = await axios.post(`${API_BASE}/auth/login`, {
            email: 'demo@example.com',
            password: 'demo1234',
          });
          setToken(response.data.access_token);
        } catch {
          console.error('Login unavailable; backend may not be running yet.');
        }
      }
    };

    ensureDemoLogin();
  }, []);

  const fetchConversations = async () => {
    if (!token) return;
    try {
      const response = await axios.get(`${API_BASE}/conversations`, { headers: authHeaders });
      setConversations(response.data);
      if (!activeConversationId && response.data.length) {
        setActiveConversationId(response.data[0].id);
      }
    } catch (error) {
      console.error('Unable to load conversations', error);
    }
  };

  const fetchArtifacts = async () => {
    if (!token || !activeConversationId) {
      setUploadedArtifacts([]);
      return;
    }
    try {
      const response = await axios.get(`${API_BASE}/artifacts`, {
        params: { conversation_id: activeConversationId },
        headers: authHeaders,
      });
      setUploadedArtifacts(response.data);
    } catch (error) {
      setUploadedArtifacts([]);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, [token]);

  useEffect(() => {
    fetchArtifacts();
  }, [token, activeConversationId]);

  const handleCreateConversation = async () => {
    if (!token) return;
    try {
      const response = await axios.post(
        `${API_BASE}/conversations`,
        { title: `Conversation ${conversations.length + 1}` },
        { headers: authHeaders },
      );
      setActiveConversationId(response.data.id);
      setMessages(defaultMessages);
      fetchConversations();
    } catch (error) {
      console.error('Conversation creation failed', error);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || !token) return;
    const messageText = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: messageText }]);
    setLoading(true);

    try {
      const response = await axios.post(
        `${API_BASE}/chat`,
        { message: messageText, conversation_id: activeConversationId },
        { headers: authHeaders },
      );
      setMessages((prev) => [...prev, { role: 'assistant', content: response.data.assistant_reply, cited_sources: response.data.citations }]);
      fetchConversations();
    } catch (error) {
      console.error('Chat failed', error);
      setMessages((prev) => [...prev, { role: 'assistant', content: 'The assistant is unavailable right now. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file || !activeConversationId || !token) return;
    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      await axios.post(`${API_BASE}/upload?conversation_id=${activeConversationId}`, formData, {
        headers: { ...authHeaders, 'Content-Type': 'multipart/form-data' },
      });
      await fetchArtifacts();
      setMessages((prev) => [...prev, { role: 'assistant', content: `Uploaded ${file.name}. The file is now visible in this conversation and ready for analysis.` }]);
    } catch (error) {
      console.error('Upload failed', error);
      setMessages((prev) => [...prev, { role: 'assistant', content: `Upload failed for ${file.name}.` }]);
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6">
        <aside className="w-80 rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-2xl shadow-slate-950/20">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-cyan-400">Workspace</p>
              <h1 className="mt-2 text-2xl font-semibold">AI Studio</h1>
            </div>
            <button
              className="rounded-lg bg-cyan-500 px-3 py-2 text-sm font-medium text-slate-950 hover:bg-cyan-400"
              onClick={handleCreateConversation}
            >
              + New
            </button>
          </div>

          <div className="space-y-3">
            {conversations.length ? conversations.map((conversation) => (
              <button
                key={conversation.id}
                className={`w-full rounded-xl border px-3 py-3 text-left transition ${
                  activeConversationId === conversation.id
                    ? 'border-cyan-500 bg-cyan-500/10 text-white'
                    : 'border-slate-700 bg-slate-950/60 text-slate-300 hover:border-slate-600'
                }`}
                onClick={() => setActiveConversationId(conversation.id)}
              >
                <div className="font-medium">{conversation.title}</div>
                <div className="mt-1 text-xs text-slate-400">{new Date(conversation.updated_at).toLocaleString()}</div>
              </button>
            )) : (
              <div className="rounded-xl border border-dashed border-slate-700 p-4 text-sm text-slate-400">
                No conversations yet.
              </div>
            )}
          </div>
        </aside>

        <main className="flex-1 rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-2xl shadow-slate-950/20">
          <div className="mb-5 flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-violet-400">Document & PPT Agent</p>
              <h2 className="mt-1 text-xl font-semibold">Multi-Agent AI Chatbot</h2>
            </div>
            <label className="cursor-pointer rounded-xl border border-slate-700 bg-slate-950 px-4 py-2 text-sm font-medium text-slate-200 hover:border-cyan-500">
              {uploading ? 'Uploading...' : 'Upload files'}
              <input type="file" className="hidden" onChange={handleFileUpload} />
            </label>
          </div>

          <div className="mb-5 rounded-xl border border-slate-800 bg-slate-950/70 p-4 text-sm text-slate-300">
            <div className="mb-2 font-medium text-cyan-300">Uploaded files</div>
            {uploadedArtifacts.length ? (
              <div className="space-y-2">
                {uploadedArtifacts.map((artifact) => (
                  <div key={artifact.id} className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium text-slate-100">{artifact.name}</span>
                      <span className="rounded bg-cyan-500/15 px-2 py-1 text-[10px] uppercase tracking-wide text-cyan-300">
                        {artifact.artifact_type}
                      </span>
                    </div>
                    <div className="mt-1 text-xs text-slate-400">v{artifact.version || '1'} • {artifact.status}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-slate-400">No files uploaded yet.</div>
            )}
          </div>

          <div className="space-y-4 rounded-xl border border-slate-800 bg-slate-950/60 p-4">
            {messages.map((msg, index) => (
              <div
                key={`${msg.role}-${index}`}
                className={`max-w-3xl rounded-2xl px-4 py-3 ${
                  msg.role === 'user' ? 'ml-auto bg-cyan-500 text-slate-950' : 'bg-slate-800 text-slate-100'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>
                {msg.cited_sources && msg.cited_sources.length > 0 && (
                  <div className="mt-2 text-xs opacity-75">
                    Sources: {msg.cited_sources.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-5 flex gap-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              rows={3}
              placeholder="Ask for a proposal, research trends, or revise a generated artifact..."
              className="flex-1 resize-none rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none ring-0 placeholder:text-slate-500 focus:border-cyan-500"
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !token}
              className="rounded-2xl bg-violet-500 px-5 py-3 font-medium text-white hover:bg-violet-400 disabled:cursor-not-allowed disabled:bg-slate-700"
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
