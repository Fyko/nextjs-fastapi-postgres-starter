import { Thread, Message } from "../types";

export const useMessages = (apiUrl: string) => {
	const createThread = async (): Promise<Thread> => {
		const res = await fetch(`${apiUrl}/api/thread`, {
			method: "POST",
			headers: { "Content-Type": "application/json" }
		});
		return res.json();
	};

	const createMessage = async (thread: Thread, content: string): Promise<Message> => {
		const res = await fetch(`${apiUrl}/api/threads/${thread.id}/messages`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ content })
		});
		return res.json();
	};

	return { createThread, createMessage };
};
