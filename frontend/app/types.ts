export type User = {
	id: string;
	name: string;
};

export type Thread = {
	id: number;
	title: string;
	user_id: number;
	messages: Message[];
};

export type Message = {
	id: number;
	thread_id: number;
	sender: "human" | "system";
	content: string;
	created_at: string;

	thread?: Thread;
};
