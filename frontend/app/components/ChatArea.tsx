import { FormEvent } from "react";
import { Thread } from "../types";

export function ChatArea({
  selectedThread,
  newMessage,
  setNewMessage,
  onSendMessage,
}: {
  selectedThread: Thread | null;
  newMessage: string;
  setNewMessage: React.Dispatch<React.SetStateAction<string>>;
  onSendMessage: (e: FormEvent) => void;
}) {
  return (
    <div className="w-2/3 flex flex-col p-4">
      <div className="flex-grow mb-4 overflow-y-auto">
        {selectedThread ? (
          selectedThread.messages.map((message) => (
            <div
              key={message.id}
              className={`mb-2 p-2 rounded ${
                message.sender === "human"
                  ? "bg-blue-100 ml-36"
                  : "bg-gray-100 mr-36"
              }`}
            >
              {message.content}
            </div>
          ))
        ) : (
          <div className="flex-grow"></div>
        )}
      </div>
      <form onSubmit={onSendMessage} className="flex">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
          className="flex-grow mr-2 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Send
        </button>
      </form>
    </div>
  );
}
