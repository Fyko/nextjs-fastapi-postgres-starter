import { useEffect, useState } from "react";
import { User } from "../types";

export const useUser = (apiUrl: string) => {
	const [user, setUser] = useState<User | undefined>();
  
	useEffect(() => {
	  fetch(`${apiUrl}/api/users/me`)
		.then(res => res.json())
		.then(setUser);
	}, [apiUrl]);
  
	return { user };
  };
