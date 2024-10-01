import { Thread } from "../types";

export function Sidebar({
  threads,
  selectedThread,
  onThreadSelect,
}: {
  threads: Thread[];
  selectedThread: Thread | null;
  onThreadSelect: (thread: Thread | null) => void;
}) {
  return (
    <div className="w-1/3 border-r border-gray-200 p-4">
      <h2 className="text-lg font-semibold mb-4">Threads</h2>
      <div className="h-[520px] overflow-y-auto">
        {threads.length ? (
          <div
            className={`p-2 mb-2 rounded cursor-pointer border-b border-gray-200 hover:bg-gray-100 ${
              selectedThread === null ? "bg-blue-100" : ""
            }`}
            onClick={() => onThreadSelect(null)}
          >
            New Thread
          </div>
        ) : null}
        {threads.map((thread) => (
          <div
            key={thread.id}
            className={`p-2 mb-2 rounded cursor-pointer ${
              selectedThread?.id === thread.id
                ? "bg-blue-100"
                : "hover:bg-gray-100"
            }`}
            onClick={() => onThreadSelect(thread)}
          >
            {thread.title || `Thread ${thread.id}`}
          </div>
        ))}
      </div>
    </div>
  );
}
