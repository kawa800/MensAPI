import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	try {
		const res = await fetch('http://localhost:8000/api/week/current');
		const dishes = await res.json();
		return { dishes };
	} catch(error) {
		console.log("error:", error)
	}
};
