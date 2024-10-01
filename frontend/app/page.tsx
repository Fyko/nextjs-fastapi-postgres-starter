"use client";
import { create } from "domain";
import React, { FormEvent, useEffect, useState } from "react";
import { Message, Thread, User } from "./types";
import { Sidebar } from "./components/Sidebar";
import { ChatArea } from "./components/ChatArea";
import { useUser } from "./hooks/useUser";
import { useThreads } from "./hooks/useThreads";
import { useMessages } from "./hooks/useMessages";

const apiUrl = process.env.NEXT_PUBLIC_API_URL!;

async function createThread(): Promise<Thread> {
  const res = await fetch(`${apiUrl}/api/thread`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  return res.json();
}

async function createMessage(thread: Thread, content: string): Promise<Message> {
  const res = await fetch(`${apiUrl}/api/threads/${thread.id}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content: content,
    }),
  });

  return res.json();
}

const createHumanMessage = (thread: Thread, content: string): Message => 
  ({
    id: 0,
    thread_id: thread.id,
    sender: "human",
    content: content,
    created_at: new Date().toISOString(),
  });

export default function Home() {
  const { user } = useUser(apiUrl);
  const { threads, setThreads } = useThreads(apiUrl);
  const { createThread, createMessage } = useMessages(apiUrl);
  const [selectedThread, setSelectedThread] = useState<Thread | null>(null);
  const [newMessage, setNewMessage] = useState("");

  const updateThreadsState = (updatedThread: Thread, message: Message) => {
    setThreads(prevThreads => prevThreads.map(t => t.id === updatedThread.id ? {
      ...updatedThread,
      messages: [...updatedThread.messages, message],
    } : t));

    setSelectedThread(prevSelectedThread => prevSelectedThread ? {
      ...prevSelectedThread,
      messages: [...prevSelectedThread.messages, message],
    } : prevSelectedThread);
  };

  const handleSendMessage = async (e: FormEvent) => {
    e.preventDefault();
    const trimmed = newMessage.trim();
    setNewMessage("");

    if (!trimmed) return;

    // there is an existing thread
    if (selectedThread) {
      const humanMessage = createHumanMessage(selectedThread, trimmed);
      const updatedThread = { ...selectedThread, messages: [...selectedThread.messages, humanMessage] };
      
      setSelectedThread(updatedThread);
      const message = await createMessage(updatedThread, trimmed);
      updateThreadsState(updatedThread, message);
    } else {
      // create a new thread
      const thread = await createThread();
      const humanMessage = createHumanMessage(thread, trimmed);
      const updatedThread = { ...thread, messages: [humanMessage] };
      
      setSelectedThread(updatedThread);
      setThreads([updatedThread, ...threads]);
      const message = await createMessage(thread, trimmed);
      updateThreadsState(updatedThread, message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-4xl flex text-black">
        <Sidebar threads={threads} selectedThread={selectedThread} onThreadSelect={setSelectedThread} />
        <ChatArea selectedThread={selectedThread} newMessage={newMessage} setNewMessage={setNewMessage} onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
}
