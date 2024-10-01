import { useEffect, useState } from "react";
import { Thread } from "../types";

export const useThreads = (apiUrl: string) => {
	const [threads, setThreads] = useState<Thread[]>([]);

	useEffect(() => {
		fetch(`${apiUrl}/api/threads`)
			.then(res => res.json())
			.then(({ threads }) => setThreads(threads));
	}, [apiUrl]);

	return { threads, setThreads };
};
